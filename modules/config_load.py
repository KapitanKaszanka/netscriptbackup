#!/usr/bin/env python3.10
import logging
import sys
from configparser import ConfigParser
from functions import get_and_valid_path
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
            sys.exit(1)

    def _load_devices_path(self) -> None:
        """
        load the path to the file with device parameters.
        """
        try:
            _devices_path: str = self._config["Application_Setup"][
                "Devices_Path"
            ]
            self.devices_path: Path = self._vaild_path(_devices_path)
        except KeyError as e:
            print(
                "Loading mandatory parametrs failed. "
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_configs_path(self) -> None:
        """load the path to the folder where the backups will be stored."""
        try:
            _configs_path = self._config["Application_Setup"]["Configs_Path"]
            self.configs_path: Path = self._vaild_path(_configs_path)
        except KeyError as e:
            print(
                "Loading mandatory parametrs faild. "
                f"Not allowed atribute: {e}"
            )
            sys.exit(1)
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_logging_path(self) -> None:
        """load the path to the folder where the logs will be stored."""
        try:
            _logging_path: str = self._config["Logging"]["File_Path"]
            self.logging_path = self._vaild_path(_logging_path)
        except KeyError as e:
            self.logging_path = "netscriptbackup.log"
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def _load_logging_level(self) -> None:
        """load the selected login level."""
        try:
            _logging_lv_lst: list[str] = [
                "debug",
                "info",
                "warning",
                "error",
                "critical",
            ]
            _logging_level: str = self._config["Logging"]["Level"].lower()
            if _logging_level not in _logging_lv_lst:
                print("Not allowed loggin level.")
                sys.exit(1)
            else:
                self.logging_level: str = _logging_level
        except KeyError as e:
            self.logging_level: str = "info"
        except Exception as e:
            print(f"Some error ocure: {e}")
            sys.exit(2)

    def load_config(self) -> None:
        """
        the function is responsible for executing functions that
        load configuration from the 'config.ini' file.
        """
        self._load_devices_path()
        self._load_configs_path()
        self._load_logging_path()
        self._load_logging_level()

    @staticmethod
    def _vaild_path(path_str: str) -> Path:
        _path_obj: Path | None = get_and_valid_path(path_str)
        if _path_obj == None:
            print(f"{_path_obj} dosn't exist.")
            sys.exit(1)
        return _path_obj


if __name__ == "__main__":
    pass
