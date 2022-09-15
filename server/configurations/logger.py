import logging

from flask import g

LOGGER_NAME = "server"


class UsernameFilter(logging.Filter):
    def filter(self, record):
        record.username = LOGGER_NAME if "username" not in g else g.username
        return True


def factory_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    logger.addFilter(UsernameFilter())
    return logger


def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    return logger


