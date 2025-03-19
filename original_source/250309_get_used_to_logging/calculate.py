import logging
import logging.config
logging.config.fileConfig("C:/Users/dahae/workspace/projects/small_steps/original_source/250309_get_used_to_logging/logger.conf")
logger = logging.getLogger(__name__)
logger.info('set calculation.py')

class calculation:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"creating an instance of {__name__}.{self.__class__.__name__}")
    
    def sum(self, a:int, b:int):
        self.logger.info("executing: sum()")
        return a + b
    
    def substract(self, a:int, b:int):
        self.logger.info("executing: substract()")
        return a - b
    
    def multiply(self, a:int, b:int):
        self.logger.info("executing: multiply()")
        return a * b
    
    def divide(self, a:int, b:int):
        self.logger.info("executing: divide()")
        try:
            result = a / b
            return result
        except Exception as e:
            self.logger.error(f"getting error in divide() - {e}", exc_info=True)