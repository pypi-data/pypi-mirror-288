"""
A module that gets the default logger of the application.
"""

import logging
from functools import lru_cache
from logging import getLogger

from uvicorn.logging import DefaultFormatter

from settings import settings


@lru_cache
def get_logger():
    """gets the default logger of the application"""

    logger = getLogger(settings.logger_name)
    logger.setLevel(logging.INFO if settings.production else logging.DEBUG)
    if logger.parent is not None:
        handlers = [handler.__class__ for handler in logger.parent.handlers]
        if logging.StreamHandler not in handlers:
            logger.addHandler(logging.StreamHandler())
            logger.handlers[0].setFormatter(
                DefaultFormatter(fmt="%(levelprefix)s %(message)s")
            )
    return logger
