import logging
import logging.config
import os
from datetime import datetime

logging_parent_path = os.path.dirname(os.path.abspath(__file__))
logfile_name = f"logfile_{datetime.strftime(datetime.now(), '%Y%m%d')}.log"
logging.config.fileConfig(fname=os.path.join(logging_parent_path, 'logger.conf'),
                          defaults={"logfilename": logfile_name})
logging.info('set calculation.py')

class calculation:
    def __init__(self):
        logging.info(f"creating an instance of {__name__}.{self.__class__.__name__}")
    
    def sum(self, a:int, b:int):
        logging.info("executing: sum()")
        return a + b
    
    def substract(self, a:int, b:int):
        logging.info("executing: substract()")
        return a - b
    
    def multiply(self, a:int, b:int):
        logging.info("executing: multiply()")
        return a * b
    
    def divide(self, a:int, b:int):
        logging.info("executing: divide()")
        try:
            result = a / b
            return result
        except Exception as e:
            logging.error(f"getting error in divide() - {e}", exc_info=True)