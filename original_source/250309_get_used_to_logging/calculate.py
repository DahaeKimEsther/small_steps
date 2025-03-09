import logging

logger = logging.getLogger(__name__)
logger.propagate = True 

class calculate:
    
    def sum(self, a:int, b:int):
        return a + b
    
    def substract(self, a:int, b:int):
        return a - b
    
    def multiply(self, a:int, b:int):
        return a * b
    
    def divide(self, a:int, b:int):
        try:
            result = a / b
            logger.debug(f"divide: {a} / {b} = {result}")
            return result
        except ZeroDivisionError:
            logger.error("division by zero")
            raise