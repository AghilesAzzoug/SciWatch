import logging
from logging import Logger
from typing import Literal

import coloredlogs
import verboselogs

from sci_watch.core.settings import settings


def get_logger(
    logger_name: str,
    level: Literal[
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "FATAL", "CRITICAL"
    ] = settings.log_level,
) -> Logger:
    """
    Logger getter function

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
        fmt="%(asctime)s.%(msecs)04d %(hostname)s %(name)s [%(process)d] %(levelname)s %(message)s",
        field_styles=field_styles,
    )

    return logger
