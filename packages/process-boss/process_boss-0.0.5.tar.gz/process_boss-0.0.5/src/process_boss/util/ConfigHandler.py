import logging

from .FileHandler import FileHandler
from ..domain.Config import Config

class ConfigHandler:
    
    def __init__(self):
        self.fileHandler = FileHandler()

    def read(self, filePath):
        logging.debug(f"filePath={filePath}")

        yamlConfig = self.fileHandler.readConfig(filePath) 
        logging.debug(f"YAML config: {yamlConfig}")

        config = Config(yamlConfig)
        logging.debug(f"Config created: {config}")

        return config
