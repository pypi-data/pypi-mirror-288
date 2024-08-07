"""
A module that sets up and provides the default logger for the application.
"""

import logging
from functools import lru_cache
from logging import StreamHandler, getLogger

from uvicorn.logging import DefaultFormatter

from qena_core.settings import settings


@lru_cache
def get_logger():
    """Get the default logger of the application."""

    logger = getLogger(settings.logger_name)
    logger.setLevel(logging.INFO if settings.production else logging.DEBUG)

    # Ensure the logger has a StreamHandler with DefaultFormatter
    if logger.parent:
        handlers = [handler.__class__ for handler in logger.parent.handlers]
        if StreamHandler not in handlers:
            stream_handler = StreamHandler()
            stream_handler.setFormatter(
                DefaultFormatter(fmt="%(levelprefix)s %(message)s")
            )
            logger.addHandler(stream_handler)

    return logger
