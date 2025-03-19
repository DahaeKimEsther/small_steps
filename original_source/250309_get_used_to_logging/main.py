# https://docs.python.org/ko/3.8/howto/logging-cookbook.html

import logging
import logging.config
import calculate
logging.config.fileConfig('C:/Users/dahae/workspace/projects/small_steps/original_source/250309_get_used_to_logging/logger.conf')

# logger 사용
logging.info("creating an instance of calculation.calculation, called 'calc'")
calc = calculate.calculation()

logging.info('setting a,b for calc.divide()')
a = 10
b = 0

logging.info('executing calc.divide()')
result = calc.divide(a, b)
logging.info(f"getting result of cal.divide: {a} / {b} = {result}")