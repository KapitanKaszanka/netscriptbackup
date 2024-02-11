#!/usr/bin/env python3

from configparser import ConfigParser
from modules.devices import Device, Cisco, Mikrotik
import logging
import json


class Config_Load():


    def __init__(self):
        self._config = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()
        except Exception as e:
            print()
            print("#! CAN'T LOAD CONFIG FILE")
            print(f"#! Problem: {e}")
            print("#! Exiting...")
            print()
            exit()


    def load_config(self):
        self.devices_path = self._config["Application_Setup"]["Devices_Path"]
        self.passwords_path = self._config["Application_Setup"]["Passwords_Path"]

        _logging_lv_lst = ["debug", "info", "warning", "error", "critical"]
        _logging_level = self._config["Logging"]["Level"]
        if _logging_level not in _logging_lv_lst:
            print()
            print("Not allowed loggin level")
            print(f"Allowed logging level list: {_logging_lv_lst}")
            print("#! Exiting...")
            print()
            exit()
        else:
            self.logging_level = _logging_level.lower()
        self._logging_path = self._config["Logging"]["File_Path"]
    
    ## Logging setup
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

        file_handler = logging.FileHandler(self._logging_path)
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
            '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
            )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger



CONFIG_LOADED = Config_Load()
LOGGER = CONFIG_LOADED.set_logging()



class Devices_Load():
    """Class loads device and store this in object."""


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Devices_Load")


    def load_jsons(self):
        try:
            self.logger.debug("\n\tLoading basic devices list.")
            with open(CONFIG_LOADED.devices_path) as f:
                _basic_devs = json.load(f)
            self.logger.debug("\n\tLoading passwords list.")
            with open(CONFIG_LOADED.passwords_path) as f:
                _passwords = json.load(f)

            def mergign_dcts(dct1, dct2):
                self.logger.debug("\n\tMerging lists.")
                for key in dct1.keys():
                    try:
                        dct1[key]["password"] = dct2[key]["password"]
                        dct1[key]["passphrase"] = dct2[key]["passphrase"]

                    except KeyError as e:
                        print()
                        self.logger.error(
                            f"\n\tKey error, check devices or passwords file for ip: {e}"
                            )
                        print("#! Exiting...")
                        print()
                        exit()

                return dct1
            
            self.devices_data = mergign_dcts(_basic_devs, _passwords)

        except FileNotFoundError as e:
            print()
            self.logger.error(f"\n\t{e}")
            print("#! Exiting...")
            exit()

        except json.decoder.JSONDecodeError as e:
            print()
            self.logger.error(f"\n\t{e}")
            print("#! Exiting...")
            print()
            exit()

        except Exception as e:
            print()
            self.logger.error(f"\n\t{e}")
            print("#! Exiting...")
            print()
            exit()



class SSH_Connection():


    def __init__(self) -> None:
        pass



class Backup():


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Devices_Load()
        self.devices.load_jsons()
        self.ssh = SSH_Connection()


    def create_devices(self):
        devices = self.devices.devices_data

        for ip in devices:
            if devices[ip]["vendor"] == "cisco":
                Cisco(
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    soft = devices[ip]["soft"],
                    password = devices[ip]["password"],
                    passphrase = devices[ip]["passphrase"]
                )

            elif devices[ip]["vendor"] == "mikrotik":
                Mikrotik(
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    soft = devices[ip]["soft"],
                    password = devices[ip]["password"],
                    passphrase = devices[ip]["passphrase"]
                )
                
            else:
                self.logger.warning(f"Device is not supported. IP: {ip}")
                pass


if __name__ == "__main__":
    pass