import json
import logging

class Process:
    def __init__(self, config):
        logging.debug(f"config={config}")
        
        self.id = self.initId(config)
        self.cron = self.initCron(config)
        self.command = self.initCommand(config)
        self.runAtStartup = self.initRunAtStartup(config)

    def initId(self, config):
        if (type(config) is not dict or 
            'id' not in config or 
            type(config['id']) is not str or 
            len(config['id']) == 0
        ):
            errorMessage = f'Invalid configuration for "id": Non-empty string required: "{config}"'
            logging.error(errorMessage)
            raise Exception(errorMessage)
        
        return config['id']
    
    def initCron(self, config):
        if (type(config) is not dict or 
            'cron' not in config or 
            type(config['cron']) is not str or 
            len(config['cron']) == 0
        ):
            errorMessage = f'Invalid configuration for "cron": Non-empty string required: "{config}"'
            logging.error(errorMessage)
            raise Exception(errorMessage)
        
        return config['cron']

    def initCommand(self, config):
        if (type(config) is not dict or
            'command' not in config or 
            type(config['command']) is not str or 
            len(config['command']) == 0
        ):
            errorMessage = f'Invalid configuration for "command": Non-empty string required: "{config}"'
            logging.error(errorMessage)
            raise Exception(errorMessage)
        
        return config['command']
    
    def initRunAtStartup(self, config):
        runAtStartup = False

        if type(config) is not dict or 'runAtStartup' not in config:
            return runAtStartup

        runAtStartup = config['runAtStartup']

        if type(runAtStartup) is not bool:
            errorMessage = f'Invalid configuration for "runAtStartup": Boolean value required: "{config}"'
            logging.error(errorMessage)
            raise Exception(errorMessage)
        
        return runAtStartup

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Process': {
                'id': self.id,
                'cron': self.cron,
                'command': self.command,
                'runAtStartup': self.runAtStartup
            }
        }
