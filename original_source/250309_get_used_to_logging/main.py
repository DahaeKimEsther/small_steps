# https://docs.python.org/ko/3.8/howto/logging-cookbook.html

import logging
import logging.config
import calculate
import os
from datetime import datetime

logging_parent_path = os.path.dirname(os.path.abspath(__file__))
logfile_name = f"logfile_{datetime.strftime(datetime.now(), '%Y%m%d')}.log"
logging.config.fileConfig(fname=os.path.join(logging_parent_path, 'logger.conf'),
                          defaults={"logfilename": logfile_name})

# logger 사용
logging.info("creating an instance of calculation.calculation, called 'calc'")
calc = calculate.calculation()

logging.info('setting a,b for calc.divide()')
a = 10
b = 0

logging.info('executing calc.divide()')
result = calc.divide(a, b)
logging.info(f"getting result of cal.divide: {a} / {b} = {result}")