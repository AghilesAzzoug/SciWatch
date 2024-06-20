import logging
from datetime import datetime
from functools import wraps
from logging import FileHandler, Formatter, Logger
from pathlib import Path
from typing import Callable, Literal

import coloredlogs
import verboselogs

from sci_watch.core.settings import settings


_FORMAT = "[%(levelname)s] [%(process)d] [%(thread)d] [%(name)s] %(asctime)s.%(msecs)04d %(message)s"
_DATE_FORMAT = "%H:%M:%S"


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
        datefmt=_DATE_FORMAT,
        field_styles=field_styles,
    )

    log_path = Path("logs", datetime.today().strftime("%Y-%m-%d") + ".log")
    log_path.parent.mkdir(exist_ok=True, parents=True)
    file_handler = FileHandler(
        filename=log_path,
        mode="a+",
        encoding='utf-8'
    )

    file_handler.setFormatter(Formatter(fmt=_FORMAT, datefmt=_DATE_FORMAT))
    file_handler.setLevel(level)

    logger.addHandler(file_handler)

    return logger


def logging_wrapper(logger: Logger) -> Callable:
    """
    Wrap an entire function in a try / except block in order to catch and *log* any Exception; such exceptions 
    are propagated to the caller.

    Parameters
    ----------
    logger: logging.Logger
        The logger to use for logging raised exceptions.

    Returns
    -------
    callable:
        The decorated function wrapped in a try / except block with error propagation.
    """
    def decorator_factory(func: Callable):
        @wraps(func)
        def with_logging(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.exception("An unexpected exception was raised")
                raise
        return with_logging
    return decorator_factory
