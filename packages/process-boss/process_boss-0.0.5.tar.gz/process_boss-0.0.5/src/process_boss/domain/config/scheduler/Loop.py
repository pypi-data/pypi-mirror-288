import json
import logging

class Loop:
    def __init__(self, config):
        logging.debug(f"config={config}")
        
        self.restartSeconds = self.initRestartSeconds(config)
        self.runOnce = self.initRunOnce(config)

    def initRestartSeconds(self, config):
        restartSeconds = 15

        if type(config) is not dict or 'restartSeconds' not in config:
            return restartSeconds
        
        restartSeconds = config['restartSeconds']

        if type(restartSeconds) is not int or restartSeconds < 0:
            errorMessage = f"Invalid configuration for \"restartSeconds\": Non-negative integer required: \"{restartSeconds}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return restartSeconds

    def initRunOnce(self, config):
        runOnce = False

        if type(config) is not dict or 'runOnce' not in config:
            return runOnce
        
        runOnce = config['runOnce']

        if type(runOnce) is not bool:
            errorMessage = f"Invalid configuration for \"runOnce\": Boolean value required: \"{runOnce}\""
            logging.error(errorMessage)
            raise Exception(errorMessage)

        return runOnce

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Loop': {
                'restartSeconds': self.restartSeconds, 
                'runOnce': self.runOnce
            }
        }
