#!/usr/bin/env python3.10
import logging

module_logging = logging.getLogger("backup_app.devices")

class Device():


    devices_lst = []
    supported_dev_type = ["cisco_ios", "mikrotik_routeros"]


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            device_type: str,
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
        self.device_type = device_type
        self.passphrase = passphrase
        self.key_file = key_file
        self.password = password
        self.conf_mode_pass = conf_mode_pass
        Device.devices_lst.append(self)



class Cisco(Device):


    soft_supported = ["cisco_ios"]


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            device_type: str,
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
            device_type,
            passphrase,
            key_file,
            password,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Cisco")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.device_type  in Cisco.soft_supported:
            self.logger.debug(f"Command return for device: {self.ip}")
            return "show running-config"

        else:
            self.logger.info(
                f"Return False for command_show_config for: {self.ip}"
                )
            return False


    def config_parser(self, config):
        self.logger.debug(f"Parsing config {self.ip}")
        _tmp_config = []
        config = config.splitlines()

        for line in config:
            self.logger.debug(f"Skiping line ! for {self.ip}.")
            if "!" in line:
                _tmp_config.append("")
                continue

            elif "Building configuration" in line:
                continue

            elif "Current configuration" in line:
                continue

            else:
                _tmp_config.append(line)

        config_to_return = "\n".join(_tmp_config)

        return config_to_return



class Mikrotik(Device):


    soft_supported = ["mikrotik_routeros"]


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            device_type: str,
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
            device_type,
            passphrase,
            key_file,
            password,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Mikrotik")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.device_type in Mikrotik.soft_supported:
            self.logger.debug(
                f"Command return for device: {self.ip}"
                )
            return "export"
        
        else:
            self.logger.warning(
                f"Soft type not supported: {self.ip}"
                )
            return False
        
    def config_parser(self, config):
        self.logger.debug(f"Parsing config {self.ip}")
        _tmp_config = []
        config = config.splitlines()

        for line in config:
            if "#" in line:
                self.logger.debug(f"Skiping line {line} for {self.ip}.")
                continue

            _tmp_config.append(line)
        
        config_to_return = "\n".join(_tmp_config)

        return config_to_return
