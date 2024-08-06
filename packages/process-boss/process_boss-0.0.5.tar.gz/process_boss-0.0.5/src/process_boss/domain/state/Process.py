import json

class Process:

    def __init__(self, processConfig, startDatetime, future):
        self.processConfig = processConfig
        self.startDatetime = startDatetime
        self.future = future

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'ProcessConfig': self.processConfig.toDict(), 
            'startDatetime': str(self.startDatetime),
            'future': str(self.future),
        }
