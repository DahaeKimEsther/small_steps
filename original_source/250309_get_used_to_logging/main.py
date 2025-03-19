# https://docs.python.org/ko/3.8/howto/logging-cookbook.html

import logging
import logging.config
import calculate
logging.config.fileConfig('C:/Users/dahae/workspace/projects/small_steps/original_source/250309_get_used_to_logging/logger.conf')
logger = logging.getLogger(__name__)

# #logging.config 없을 경우
# #main 로거
# main_logger = logging.getLogger('main')
# main_logger.setLevel(logging.DEBUG)

# # Handler에 formatter 포함
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)

# # handler 적용
# main_logger.addHandler(ch)

# logger 사용
logger.info("creating an instance of calculation.calculation, called 'calc'")
calc = calculate.calculation()

logger.info('setting a,b for calc.divide()')
a = 10
b = 0

logger.info('executing calc.divide()')
result = calc.divide(a, b)
logger.info(f"getting result of cal.divide: {a} / {b} = {result}")