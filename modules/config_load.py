#!/usr/bin/env python3.10
import logging
import sys
from configparser import ConfigParser
from modules.other.functions import get_and_valid_path
from pathlib import Path

class Config_Load:
    """
    an object that has the necessary functions 
    to load config.ini and validate it.
    """
    def __init__(self) -> None:
        self._config: ConfigParser = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()
        except Exception as e:
            print("Can't read config.ini file...")
            print(e)
            exit()

    def _load_devices_path(self) -> None:
        """
        load the path to the file with device parameters.
        """
        try:
            _devices_path: str = self._config["Application_Setup"]["Devices_Path"]
            self.devices_path: Path | None = get_and_valid_path(_devices_path)
        except KeyError as e:
            print(
                "Loading mandatory parametrs failed. "
                f"Not allowed atribute: {e}"
                )
            sys.exit(1)

    def _load_configs_path(self) -> None:
        """load the path to the folder where the backups will be stored."""
        try:
            _configs_path = self._config["Application_Setup"]["Configs_Path"]
            _configs_path = get_and_valid_path(_configs_path)
            if _configs_path == None:
                print(f"{_configs_path} dosn't exist.")
                exit()
            self.configs_path = _configs_path
        except KeyError as e:
            print(
                "Loading mandatory parametrs faild. "
                f"Not allowed atribute: {e}"
                )
            exit()

    def _load_logging_path(self) -> None:
        """load the path to the folder where the logs will be stored."""
        try:
            _logging_path: str = self._config["Logging"]["File_Path"]
            _logging_path: Path | None = get_and_valid_path(_logging_path)
            if _logging_path == None:
                print(f"{_logging_path} dosn't exist.")
                sys.exit(1)
            self.logging_path = _logging_path
        except KeyError as e:
            self.logging_path = "netscriptbackup.log"

    def _load_logging_level(self) -> None:
        """load the selected login level."""
        try:
            _logging_lv_lst: list[str] = [
                "debug",
                "info",
                "warning",
                "error",
                "critical"
            ]
            _logging_level: str = self._config["Logging"]["Level"].lower()
            if _logging_level not in _logging_lv_lst:
                print("Not allowed loggin level.")
                sys.exit(1)
            else:
                self.logging_level: str = _logging_level
        except KeyError as e:
            self.logging_level: str = "info"

    def load_config(self) -> None:
        """
        the function is responsible for executing functions that 
        load configuration from the 'config.ini' file.
        """
        self._load_devices_path()
        self._load_configs_path()
        self._load_logging_path()
        self._load_logging_level()

    def set_logging(self) -> None:
        """
        the function responsible for setting the logging system
        to_rebuild
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
