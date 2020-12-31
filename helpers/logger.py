"""Wrapper for the logger"""
import logging
from os.path import join
from os import getenv
from logging.handlers import RotatingFileHandler


class Logger:
    """check if URL was in the DB and content was not changed"""

    @staticmethod
    def initial(name):
        logger = logging.getLogger(name)
        log_level = getenv('LOG_LEVEL', 'DEBUG')
        logger.setLevel(log_level)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Roll over after 2MB and keep backup logs app.log.1, app.log.2, etc
        file_handler = RotatingFileHandler(join("logs", "app.log"), maxBytes=2000000, backupCount=5)
        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger
