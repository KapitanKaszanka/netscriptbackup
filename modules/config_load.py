#!/usr/bin/env python3.10
import logging
from configparser import ConfigParser
from modules.functions import get_and_valid_path


class Config_Load:
    """
    An object that has the necessary functions 
    to load config.ini and validate it.
    """

    def __init__(self):
        self._config = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()
        except Exception as e:
            print("Can't read config.ini file...")
            print(e)
            exit()

    def _load_devices_path(self):
        """
        Load the path to the file with device parameters.
        """

        try:
            _devices_path = self._config["Application_Setup"]["Devices_Path"]
            self.devices_path = get_and_valid_path(_devices_path)
        except KeyError as e:
            print(
                "Loading mandatory parametrs failed. "
                f"Not allowed atribute: {e}"
                )
            exit()

    def _load_configs_path(self):
        """Load the path to the folder where the backups will be stored."""

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

    def _load_logging_path(self):
        """Load the path to the folder where the logs will be stored."""
        
        try:
            _logging_path = self._config["Logging"]["File_Path"]
            _logging_path = get_and_valid_path(_logging_path)
            if _logging_path == None:
                print(f"{_logging_path} dosn't exist.")
                exit()
            self.logging_path = _logging_path
        except KeyError as e:
            self.logging_path = "netscriptbackup.log"

    def _load_logging_level(self):
        """Load the selected login level."""

        try:
            _logging_lv_lst = [
                "debug",
                "info",
                "warning",
                "error",
                "critical"
            ]
            _logging_level = self._config["Logging"]["Level"].lower()
            if _logging_level not in _logging_lv_lst:
                print("Not allowed loggin level.")
                exit()
            else:
                self.logging_level = _logging_level
        except KeyError as e:
            self.logging_level = "warning"

    def load_config(self):
        """
        The function is responsible for executing functions that 
        load configuration from the 'config.ini' file.
        """

        self._load_devices_path()
        self._load_configs_path()
        self._load_logging_path()
        self._load_logging_level()

    def set_logging(self):
        """The function responsible for setting the logging system"""
        
        logger = logging.getLogger("netscriptbackup")
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
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            "%(asctime)s:%(name)s:%(levelname)s:%(message)s"
            )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        return logger


if __name__ == "__main__":
    pass
