import os
from logging import getLogger, StreamHandler, Formatter, getLevelName, Logger
from typing import Literal


def create_logger(
    format_: str = os.getenv("SLF4PY_LOG_FORMAT", "[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s"),
    level: Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'] = os.getenv("SLF4PY_LOG_LEVEL", "DEBUG")
) -> Logger:
    log = getLogger(__name__)

    level_name = getLevelName(level)
    handler = StreamHandler()
    handler.setLevel(level_name)
    handler.setFormatter(Formatter(format_))

    log.setLevel(level_name)
    log.addHandler(handler)
    log.propagate = False

    return log
