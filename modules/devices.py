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
            self.logger.critical(f"{e}")
            exit()

        except json.decoder.JSONDecodeError as e:
            self.logger.critical(f"{e}")
            exit()

        except Exception as e:
            self.logger.critical(f"{e}")
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
            try:
                _device_parametrs = {
                    "ip": ip,
                    "port": devices[ip]["port"],
                    "name": devices[ip]["name"],
                    "vendor": devices[ip]["vendor"],
                    "connection": devices[ip]["connection"],
                    "username": devices[ip]["username"],
                    "password": devices[ip]["password"],
                    "mode_cmd": "",
                    "mode_password": None,
                    "key_file": None,
                    "passphrase": None
                }

                if devices[ip]["change_mode"] != None:
                    mode = devices[ip]["change_mode"]
                    if isinstance(devices[ip]["change_mode"], list):
                        if mode[0] == None:
                            _device_parametrs["mode_cmd"] = ""
                        else:
                            _device_parametrs["mode_cmd"] = mode[0]
                        _device_parametrs["mode_password"] = mode[1]\

                if devices[ip]["key_file"] != None:
                    _device_parametrs["key_file"] = _get_and_valid_path(
                        devices[ip]["key_file"], ip
                        )
                    _device_parametrs["passphrase"] = devices[ip]["passphrase"]

            except KeyError as e:
                self.logger.warning(f"{ip} - KeyError in devices file: {e}")
                pass
            
            except Exception as e:
                self.logger.critical(f"Error ocure {e}")
                exit()

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
            ip: str,
            port: int,
            name: str,
            vendor: str,
            connection: str,
            username: str,
            password: str,
            mode_cmd: str,
            mode_password: str,
            key_file: str,
            passphrase: str
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
        self.mode_cmd = mode_cmd
        self.mode_password = mode_password
        Device.devices_lst.append(self)


    def config_filternig(self, config):
        return config



class Cisco(Device):
    """Cisco device object."""


    def __init__(
            self,
            ip: str,
            port: int,
            name: str,
            vendor: str,
            connection: str,
            username: str,
            password: str,
            mode_cmd: str,
            mode_password: str,
            key_file: str,
            passphrase: str
            ) -> "Device":
        super().__init__(
            ip,
            port,
            name,
            vendor,
            connection,
            username,
            password,
            mode_cmd,
            mode_password,
            key_file,
            passphrase
            )
        self.logger = logging.getLogger("backup_app.devices.Cisco")
        self.logger.debug(f"{self.ip} - Creatad.")
        self.device_type = "cisco_ios"


    def command_show_config(self):
        self.logger.debug(f"{self.ip} - Returning commands.")
        return "show running-config view full"


    def config_filternig(self, config):
        self.logger.debug(f"{self.ip} - Configuration filtering.")
        _tmp_config = []
        config = config.splitlines()

        # add_enter = True
        for line in config:
            if "!" in line:
                if add_enter == True:
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
            ip: str,
            port: int,
            name: str,
            vendor: str,
            connection: str,
            username: str,
            password: str,
            mode_cmd: str,
            mode_password: str,
            key_file: str,
            passphrase: str
            ) -> "Device":
        super().__init__(
            ip,
            port,
            name,
            vendor,
            connection,
            username,
            password,
            mode_cmd,
            mode_password,
            key_file,
            passphrase
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
            ip: str,
            port: int,
            name: str,
            vendor: str,
            connection: str,
            username: str,
            password: str,
            mode_cmd: str,
            mode_password: str,
            key_file: str,
            passphrase: str
            ) -> "Device":
        super().__init__(
            ip,
            port,
            name,
            vendor,
            connection,
            username,
            password,
            mode_cmd,
            mode_password,
            key_file,
            passphrase
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