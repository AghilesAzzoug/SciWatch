import logging
from datetime import datetime
from functools import wraps
from logging import FileHandler, Formatter, Logger
from pathlib import Path
from typing import Callable, Literal

import coloredlogs
import verboselogs

from sci_watch.core.settings import settings


_FORMAT = "[%(levelname)s] [%(process)d] [%(thread)d] [%(filename)d] %(asctime)s.%(msecs)04d %(name)s %(message)s"

def get_logger(
    logger_name: str,
    level: Literal[
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"
    ] = settings.log_level,
) -> Logger:
    """
    Logger getter function.

    Parameters
    ----------
    logger_name: str
        Should be name of the file importing the logger

    level: str
        Minimum level of logging

    Returns
    -------
    Logger:
        A ready to use logger object
    """
    verboselogs.install()
    logger = logging.getLogger(logger_name)

    field_styles = {
        "asctime": {"color": "magenta"},
        "msecs": {"color": "magenta"},
        "hostname": {"color": "blue"},
        "programname": {"color": "cyan"},
        "name": {"color": "green"},
        "process": {"color": "green", "bold": True},
        "levelname": {"color": "black", "bold": True, "bright": True},
        "message": {"color": "white", "bright": True},
    }
    coloredlogs.install(
        level=level,
        logger=logger,
        fmt=_FORMAT,
        field_styles=field_styles,
    )

    file_handler = FileHandler(
        filename=Path("logs", datetime.today().strftime("%Y-%m-%d") + ".log"),
        mode="a",
        encoding='utf-8'
    )

    file_handler.setFormatter(Formatter(fmt=_FORMAT))
    file_handler.setLevel(level)

    logger.addHandler(file_handler)

    return logger


def broad_except_logging(logger: Logger) -> Callable:
    """
    Wrap an entire function in a try / except block in order to catch and *log* any Exception.

    Parameters
    ----------
    logger: logging.Logger
        The logger to use for logging raised exceptions.

    Returns
    -------
    callable:
        The decorated function wrapped in a try / except block.
    """
    def decorator_factory(func: Callable):
        @wraps(func)
        def with_logging(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception("An uncaught exception was raised")
        return with_logging
    return decorator_factory
