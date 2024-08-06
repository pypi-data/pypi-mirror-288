import json
import logging
from .scheduler.Loop import Loop

class Scheduler:
    def __init__(self, config):
        logging.debug(f"config={config}")

        self.maxWorkers = self.initMaxWorkers(config)
        self.loop = self.initLoop(config)

    def initMaxWorkers(self, config):
        maxWorkers = 10

        if type(config) is not dict or 'maxWorkers' not in config:
            return maxWorkers
        
        maxWorkers = config['maxWorkers']

        if type(maxWorkers) is not int or maxWorkers <= 0:
            errorMessage = f"Invalid configuration for \"maxWorkers\": Positive integer required: \"{maxWorkers}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return maxWorkers

    def initLoop(self, config):
        configLoop = None
        if type(config) is dict and 'loop' in config:
            configLoop = config['loop']

        return Loop(configLoop)

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Scheduler': {
                'maxWorkers': self.maxWorkers, 
                'loop': self.loop.toDict()
            }
        }
