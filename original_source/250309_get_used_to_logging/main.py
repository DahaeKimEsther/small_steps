import logging
import calculate

#main 로거
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# calculate 로거
calc_logger = logging.getLogger('calculate')
calc_logger.setLevel(logging.DEBUG)

# Handler에 formatter 포함
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# 각 logger들에 handler 적용
logger.addHandler(ch)

# logger 사용
a = 10
b = 0
try: 
    result = calculate.divide(a, b)
    logger.info(f"{a} / {b} = {result}")
except Exception as e:
    logger.error(e)