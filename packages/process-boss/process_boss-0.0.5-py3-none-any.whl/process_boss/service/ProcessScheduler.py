import sys
import time
import pytz
import logging
import shlex
from subprocess import Popen, PIPE, STDOUT
from croniter import croniter
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from ..util.ConfigHandler import ConfigHandler 
from ..util.LogHandler import LogHandler 
from ..domain.State import State

class ProcessScheduler:

    def __init__(self, configPath):
        logging.info(f"Using configuration file: \"{configPath}\"")

        self.startupDatetime = datetime.now(pytz.timezone('Europe/London'))
        self.configPath = configPath
        self.configHandler = ConfigHandler()
        self.logHandler = LogHandler()
        self.state = State()

    def loop(self):
        while(True):
            logging.info("Starting new loop")
            logging.debug(self.state)

            config = self.configHandler.read(self.configPath)
            self.runAll(config)
            self.sleep(config.scheduler.loop.restartSeconds)
            
            if config.scheduler.loop.runOnce:
                self.waitAll()
                break

    def runAll(self, config):
        logging.debug(f"config={config}")

        with ThreadPoolExecutor(max_workers=config.scheduler.maxWorkers) as executor:
            for processConfig in iter(config.processes):
                slog = self.logHandler.createSchedulerLogger(processConfig, config.logs)
                slog.info(f"[{processConfig.id}] processConfig={processConfig}")

                processRegistered = self.state.get(processConfig.id) != False
                processFinished = processRegistered and self.state.get(processConfig.id).future.done()
                slog.debug(f"[{processConfig.id}] processRegistered={processRegistered}, processFinished={processFinished}")

                if processRegistered:
                    if not processFinished:
                        slog.info(f"[{processConfig.id}] Process is still running. Skipping...")
                        continue
                    else:
                        nextRunBaseDate = self.state.get(processConfig.id).startDatetime
                        slog.info(f"[{processConfig.id}] Process ran before: {nextRunBaseDate}")
                else:
                    nextRunBaseDate = self.startupDatetime
                    slog.info(f"[{processConfig.id}] Process has not run before")

                slog.debug(f"[{processConfig.id}] nextRunBaseDate={nextRunBaseDate}")

                nextRunTimestamp = croniter(processConfig.cron, nextRunBaseDate).get_next() 
                nowDatetime = datetime.now(pytz.timezone('Europe/London'))
                nowTimestamp = nowDatetime.timestamp()
                isScheduledToRun = nextRunTimestamp < nowTimestamp
                slog.debug(f"[{processConfig.id}] isScheduledToRun={isScheduledToRun}, processConfig.runAtStartup={processConfig.runAtStartup}")

                if (isScheduledToRun or (not processRegistered and processConfig.runAtStartup)):
                    slog.info(f"[{processConfig.id}] Process is scheduled to run NOW: {datetime.fromtimestamp(nowTimestamp)}")
                    future = executor.submit(self.run, processConfig, config.logs, nowDatetime)
                    self.state.set( processConfig, nowDatetime, future )
                else:
                    slog.info(f"[{processConfig.id}] Process is scheduled to run on: {datetime.fromtimestamp(nextRunTimestamp)}")

    def run(self, processConfig, configLogs, nowDatetime):
        plog = self.logHandler.createProcessLogger(processConfig, configLogs, nowDatetime)
        plog.debug(f"processConfig={processConfig}, configLogs={configLogs}, nowDatetime={nowDatetime}")

        try:
            with Popen(
                shlex.split(processConfig.command),
                stdout=PIPE,
                stderr=STDOUT
            ) as p:
                for line in iter(p.stdout.readline, b""):
                    plog.info(f"[{processConfig.id}] ... {line.decode(sys.stdout.encoding).rstrip()}")
                    
        except Exception as e:
            plog.error(f"[{processConfig.id}] ... {e}")

    def sleep(self, loopRestartSeconds):
        logging.info(f"Sleeping for: {loopRestartSeconds} seconds")

        time.sleep(loopRestartSeconds)

    def waitAll(self):
        for processId in self.state.processIdToProcessStateDict:
            processState = self.state.processIdToProcessStateDict[ processId ]
            while not processState.future.done():
                self.sleep(1)
            
