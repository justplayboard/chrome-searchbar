"""
core/logger.py

Application logging manager.
"""

from __future__ import annotations

import logging
from pathlib import Path


class LoggingManager:
    """
    Configure and provide the application logger.
    """

    LOGGER_NAME = "ChromeSearchBar"

    def __init__(self):

        self._logger = logging.getLogger(self.LOGGER_NAME)

        if self._logger.handlers:
            return

        self._logger.setLevel(logging.INFO)

        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        )

        #
        # File Handler
        #
        file_handler = logging.FileHandler(
            log_dir / "app.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        #
        # Console Handler
        #
        console_handler = logging.StreamHandler()

        console_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)

    @property
    def logger(self):

        return self._logger