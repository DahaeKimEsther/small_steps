import logging

logger = logging.getLogger('main.calculation')
logger.propagate = True 

class calculation:
    def __init__(self):
        self.logger = logging.getLogger('main.calculation.calculation')
        self.logger.info("creating an instance of calculation.calculation")
    
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
            logger.error(f"getting error in divide() - {e}")