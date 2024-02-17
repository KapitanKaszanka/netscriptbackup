#!/usr/bin/env python3.10
import logging
import json
from pathlib import Path

class Devices_Load():
    """
    An object that collects all the functions 
    needed to create device objects.
    """


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.devices.Devices_Load")


    def load_jsons(self, path):
        try:
            self.logger.debug("Loading basic devices list.")
            with open(path, "r") as f:
                _basic_devs = json.load(f)

            self.devices_data = _basic_devs
            self.logger.debug(f"Empty RAM memory.")
            del _basic_devs


        except FileNotFoundError as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            exit()

        except json.decoder.JSONDecodeError as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            print()
            exit()

        except Exception as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            print()
            exit()


    def create_devices(self):
        def _get_and_valid_path(path, ip):
            valid_path = Path(path)
            if valid_path.exists():
                return valid_path
            else:
                self.logger.warning(
                    f"{ip} - Path to key doesn't exist {path}."
                    )
                return None

        self.logger.info(f"Creating device objects..")
        devices = self.devices_data

        for ip in devices:
            _device_parametrs = {
                "name": devices[ip]["name"],
                "vendor": devices[ip]["vendor"],
                "ip": ip,
                "username": devices[ip]["username"],
                "port": devices[ip]["port"],
                "connection": devices[ip]["connection"],
                "passphrase": devices[ip]["passphrase"],
                "key_file": devices[ip]["key_file"],
                "password": devices[ip]["password"],
                "conf_mode_pass": devices[ip]["conf_mode_pass"]
            }
            if devices[ip]["key_file"] != None:
                _device_parametrs["key_file"] = _get_and_valid_path(
                    devices[ip]["key_file"], ip
                    )

            if devices[ip]["vendor"] == "cisco":
                Cisco(**_device_parametrs)

            elif devices[ip]["vendor"] == "mikrotik":
                Mikrotik(**_device_parametrs)

            elif devices[ip]["vendor"] == "juniper":
                Juniper(**_device_parametrs)

            else:
                self.logger.warning(f"{ip} - Device is not supported.")
                pass



class Device():
    """
    Main device object. Assigns all necessary information.
    Returns appropriate variables when the object's child
    does not support the given module.
    """

    devices_lst = []


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            passphrase: str,
            key_file: str,
            password: str,
            conf_mode_pass: str
            ) -> None:
        self.logger = logging.getLogger("backup_app.devices.Device")
        self.name = name
        self.vendor = vendor
        self.ip = ip
        self.username = username
        self.port = port
        self.connection = connection
        self.passphrase = passphrase
        self.key_file = key_file
        self.password = password
        self.conf_mode_pass = conf_mode_pass
        Device.devices_lst.append(self)


    def config_filternig(self, config):
        return config



class Cisco(Device):
    """Cisco device object."""


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            passphrase: str,
            key_file: str,
            password: str,
            conf_mode_pass: str
            ) -> "Device":
        super().__init__(
            name,
            vendor,
            ip,
            username,
            port,
            connection,
            passphrase,
            key_file,
            password,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Cisco")
        self.logger.debug(f"{self.ip} - Creatad.")
        self.device_type = "cisco_ios"


    def command_show_config(self):
        self.logger.debug(f"{self.ip} - Returning commands.")
        return "show running-config"


    def config_filternig(self, config):
        self.logger.debug(f"{self.ip} - Configuration filtering.")
        _tmp_config = []
        config = config.splitlines()

        for line in config:
            if "!" in line:
                if add_enter == True or add_enter == None:
                    _tmp_config.append("")
                    add_enter = False
                continue

            elif "Building configuration" in line:
                self.logger.info(f"{self.ip} - Skiping line '{line}'.")
                continue

            elif "Current configuration" in line:
                self.logger.info(f"{self.ip} - Skiping line '{line}'.")
                continue

            elif len(line) == 0:
                self.logger.debug(f"{self.ip} - Skiping empty line for.")
                continue

            else:
                _tmp_config.append(line)
                add_enter = True

        config_to_return = "\n".join(_tmp_config)

        return config_to_return



class Mikrotik(Device):
    """Mikrotik device object."""

    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            passphrase: str,
            key_file: str,
            password: str,
            conf_mode_pass: str
            ) -> "Device":
        super().__init__(
            name,
            vendor,
            ip,
            username,
            port,
            connection,
            passphrase,
            key_file,
            password,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Mikrotik")
        self.logger.debug(f"{self.ip} - Creatad.")
        self.device_type = "mikrotik_routeros"


    def command_show_config(self):
        self.logger.debug(f"{self.ip} - Returning commands.")
        return "/export"


    def config_filternig(self, config):
        self.logger.debug(f"{self.ip} - Configuration filtering.")
        _tmp_config = []
        config = config.splitlines()

        for line in config:
            if "#" in line:
                self.logger.info(f"{self.ip} - Skiping line '{line}'.")
                continue

            _tmp_config.append(line)
        
        config_to_return = "\n".join(_tmp_config)

        return config_to_return



class Juniper(Device):
    """Juniper device object."""


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            passphrase: str,
            key_file: str,
            password: str,
            conf_mode_pass: str
            ) -> "Device":
        super().__init__(
            name,
            vendor,
            ip,
            username,
            port,
            connection,
            passphrase,
            key_file,
            password,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Juniper")
        self.logger.debug(f"Device {self.ip} creatad.")
        self.device_type = "juniper"

    def command_show_config(self):
        self.logger.debug(f"{self.ip} - Returning commands.")
        return "show config | display set"

    def config_filternig(self, config):
        self.logger.debug(f"{self.ip} - Configuration filtering.")
        _tmp_config = []
        config = config.splitlines()

        for line in config:
            if "#" in line:
                self.logger.info(f"{self.ip} - Skiping line '{line}'.")
                continue

            _tmp_config.append(line)
        
        config_to_return = "\n".join(_tmp_config)

        return config_to_return