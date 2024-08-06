import json
import logging
from .processes.Process import Process

class Processes:
    def __init__(self, config):
        logging.debug(f"config={config}")

        self.processes = self.initProcesses(config)

    def initProcesses(self, config):
        processes = []

        if type(config) is not list or len(config) == 0:
            errorMessage = f"Invalid configuration for \"processes.*\": You have to define at least one process!"
            logging.error(errorMessage)
            raise Exception(errorMessage)
        
        for c in config:
            processes.append( Process(c) )

        return processes

    def __iter__(self):
        self.i = -1
        return self
    
    def __next__(self):
        self.i += 1
        if self.i < len(self.processes):
            return self.processes[ self.i ]
        else:
            raise StopIteration

    def __str__(self):
        return json.dumps( self.toDict() )

    def toDict(self):
        return {
            'Processes': [ p.toDict() for p in self.processes ]
        }
