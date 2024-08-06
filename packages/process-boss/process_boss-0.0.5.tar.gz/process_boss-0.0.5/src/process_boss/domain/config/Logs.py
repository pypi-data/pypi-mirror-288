import json
import logging
from pathlib import Path

class Logs:
    def __init__(self, config):
        logging.debug(f"config={config}")

        self.enabled = self.initEnabled(config)
        self.schedulerLogDir = self.initSchedulerLogDir(config)
        self.processLogDir = self.initProcessLogDir(config)

    def initEnabled(self, config):
        enabled = False

        if type(config) is not dict or 'enabled' not in config:
            return enabled
        
        enabled = config['enabled']

        if type(enabled) is not bool:
            errorMessage = f"Invalid configuration for \"enabled\": Boolean value required: \"{enabled}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return enabled

    def initSchedulerLogDir(self, config):
        schedulerLogDir = ""

        if type(config) is not dict or 'schedulerLogDir' not in config:
            return schedulerLogDir
        
        schedulerLogDir = config['schedulerLogDir']

        if type(schedulerLogDir) is not str or not Path(schedulerLogDir).is_dir():
            errorMessage = f"Invalid configuration for \"schedulerLogDir\": Valid directory path required: \"{schedulerLogDir}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return schedulerLogDir

    def initProcessLogDir(self, config):
        processLogDir = ""

        if type(config) is not dict or 'processLogDir' not in config:
            return processLogDir
        
        processLogDir = config['processLogDir']

        if type(processLogDir) is not str or not Path(processLogDir).is_dir():
            errorMessage = f"Invalid configuration for \"processLogDir\": Valid directory path required: \"{processLogDir}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return processLogDir

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Logs': {
                'enabled': self.enabled, 
                'schedulerLogDir': self.schedulerLogDir, 
                'processLogDir': self.processLogDir
            }
        }
