import sys
import logging

from .service.ProcessScheduler import ProcessScheduler
from .util.LogHandler import LogHandler

def main():
    logging.basicConfig(level=LogHandler.LEVEL, format=LogHandler.FORMAT)

    verifyArgumentExists()
    ProcessScheduler(sys.argv[1]).loop()

def verifyArgumentExists():
    if len(sys.argv) < 2:
        logging.error("Missing CLI argument: Configuration File Path")
        logging.error("")
        logging.error("USAGE:")
        logging.error("    $> python -m process_boss c:\\Users\\kristof\\config.yaml")
        logging.error("")
        sys.exit(1)
    
if __name__ == '__main__':
    main()
