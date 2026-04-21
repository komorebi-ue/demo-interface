from __future__ import annotations

import os
import sys
from pathlib import Path

from loguru import logger


def setup_logger(log_path: str | os.PathLike = "logs/test.log"):
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)

    logger.remove()
    logger.add(sys.stdout, level="INFO", colorize=True, backtrace=False, diagnose=False)
    logger.add(
        str(log_path),
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
        backtrace=False,
        diagnose=False,
    )
    return logger


log = setup_logger()
