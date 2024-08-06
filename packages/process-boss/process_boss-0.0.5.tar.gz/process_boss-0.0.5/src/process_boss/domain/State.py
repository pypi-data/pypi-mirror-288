import json
from .state.Process import Process

class State:

    def __init__(self):
        self.processIdToProcessStateDict = {}

    def get(self, processId):
        if not processId in self.processIdToProcessStateDict: 
            return False
        
        return self.processIdToProcessStateDict[ processId ]

    def set(self, processConfig, startDatetime, future): 
        self.processIdToProcessStateDict[ processConfig.id ] = Process(
            processConfig, startDatetime, future
        )

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'State': {p : self.processIdToProcessStateDict[p].toDict() for p in self.processIdToProcessStateDict}
        }
