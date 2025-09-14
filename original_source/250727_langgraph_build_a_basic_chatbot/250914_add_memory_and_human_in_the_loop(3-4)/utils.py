import logging
import sys


class LoggingTool:
    """
    from utils import LoggingTool
    logger = LoggingTool.get_logger(__name__)
    logger.debug(f"messages")
    """
    @staticmethod
    def get_logger(name: str = None):
        logger = logging.getLogger(name)
        if not logger.handlers:  # 중복 핸들러 방지
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)-8s - [%(filename)s : %(funcName)s() : %(lineno)d] - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
        return logger