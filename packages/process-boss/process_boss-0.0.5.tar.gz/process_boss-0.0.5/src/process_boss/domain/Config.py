import json
import logging
from .config.Scheduler import Scheduler
from .config.Logs import Logs
from .config.Processes import Processes

class Config:
    def __init__(self, config):
        logging.debug(f"config={config}")

        self.scheduler = self.initScheduler(config)
        self.logs = self.initLogs(config)
        self.processes = self.initProcesses(config)

    def initScheduler(self, config):
        configScheduler = None
        if type(config) is dict and 'scheduler' in config:
            configScheduler = config['scheduler']

        return Scheduler(configScheduler)
        
    def initLogs(self, config):
        configLogs = None
        if type(config) is dict and 'logs' in config:
            configLogs = config['logs']

        return Logs(configLogs)
        
    def initProcesses(self, config):
        configProcesses = None
        if type(config) is dict and 'processes' in config:
            configProcesses = config['processes']

        return Processes(configProcesses)
    
    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Config': {
                'scheduler': self.scheduler.toDict(), 
                'logs': self.logs.toDict(),
                'processes': self.processes.toDict()
            }
        }
