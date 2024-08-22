#!/usr/bin/env python3.10
import logging

from netinfscript.agent.config_load import Config_Load
from netinfscript.agent.devices_load import Devices_Load


class InitSystem:
    """
    the class responsible for initializa all nedded functions
    """

    def __init__(self) -> None:
        self.config_loaded = Config_Load()
        ## init fucntion for setup logging
        self.logging_level: str = self.config_loaded.logging_level
        self.set_logging()
        devices_loaded = Devices_Load(self.config_loaded.devices_path)
        devices_loaded.create_devices()

    def set_logging(self) -> None:
        """
        the function responsible for setting the logging system to do
        """
        logger: logging = logging.getLogger("netscriptbackup")
        if self.logging_level.lower() == "debug":
            logger.setLevel(logging.DEBUG)
        elif self.logging_level.lower() == "info":
            logger.setLevel(logging.INFO)
        elif self.logging_level.lower() == "warning":
            logger.setLevel(logging.WARNING)
        elif self.logging_level.lower() == "error":
            logger.setLevel(logging.ERROR)
        elif self.logging_level.lower() == "critical":
            logger.setLevel(logging.CRITICAL)
        file_handler = logging.FileHandler(self.logging_path)
        if self.logging_level.lower() == "debug":
            file_handler.setLevel(logging.DEBUG)
        elif self.logging_level.lower() == "info":
            file_handler.setLevel(logging.INFO)
        elif self.logging_level.lower() == "warning":
            file_handler.setLevel(logging.WARNING)
        elif self.logging_level.lower() == "error":
            file_handler.setLevel(logging.ERROR)
        elif self.logging_level.lower() == "critical":
            file_handler.setLevel(logging.CRITICAL)
        formatter: logging.Formatter = logging.Formatter(
            "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger


if __name__ == "__main__":
    pass
