#!/usr/bin/env python3

from configparser import ConfigParser
from pathlib import Path
import logging



class Config_Load():
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


    def load_config(self):
        def _get_and_valid_path(path):
            valid_path = Path(path)
            if valid_path.exists():
                return valid_path
            else:
                print(f"Error: {path} doesn't exist.")
                exit()

        try:
            _devices_path = self._config["Application_Setup"]["Devices_Path"]
            self.devices_path = _get_and_valid_path(_devices_path)

            _configs_path = self._config["Application_Setup"]["Configs_Path"]
            _configs_path = _get_and_valid_path(_configs_path)

            self.configs_path = _configs_path

        except KeyError as e:
            print(
                f"Loading mandatory parametrs faild. Not allowed atribute: {e}"
                )
            exit()

        try:
            _logging_lv_lst = ["debug", "info", "warning", "error", "critical"]
            _logging_level = self._config["Logging"]["Level"].lower()
            if _logging_level not in _logging_lv_lst:
                print("Not allowed loggin level.")
                exit()
            else:
                self.logging_level = _logging_level

        except KeyError as e:
            self.logging_level = "warning"
            
        try:
            _logging_path = self._config["Logging"]["File_Path"]
            self.logging_path = _get_and_valid_path(_logging_path)

        except KeyError as e:
            self.logging_path = "backup_app.log"


    def set_logging(self):
        logger = logging.getLogger("backup_app")

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