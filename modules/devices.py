#!/usr/bin/env python3.10
import logging

module_logging = logging.getLogger("backup_app.devices")

class Device():

    devices_lst = []

    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            soft: str,
            password: str,
            passphrase: str,
            ) -> None:
        self.logger = logging.getLogger("backup_app.devices.Device")
        self.name = name
        self.vendor = vendor
        self.ip = ip
        self.username = username
        self.port = port
        self.connection = connection
        self.soft = soft
        self.password = password
        self.passphrase = passphrase
        Device.devices_lst.append(self)



class Cisco(Device):


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            soft: str,
            password: str,
            passphrase: str,
            ) -> "Device":
        super().__init__(
            name,
            vendor,
            ip,
            username,
            port,
            connection,
            soft,
            password,
            passphrase
            )
        self.logger = logging.getLogger("backup_app.devices.Cisco")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.soft == "ios":
            self.logger.debug(f"Command return for device: {self.ip}")
            return "show running-config"
        else:
            self.logger.info(
                f"Return False for command_show_config for: {self.ip}"
                )
            return False



class Mikrotik(Device):


    def __init__(
            self,
            name: str,
            vendor: str,
            ip: str,
            username: str,
            port: int,
            connection: str,
            soft: str,
            password: str,
            passphrase: str
            ) -> "Device":
        super().__init__(
            name,
            vendor,
            ip,
            username,
            port,
            connection,
            soft,
            password,
            passphrase
            )
        self.logger = logging.getLogger("backup_app.devices.Mikrotik")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.soft == "ros_v6" or self.soft == "ros_v7":
            self.logger.debug(
                f"Command return for device: {self.ip}"
                )
            return "export"
        
        else:
            self.logger.info(
                f"Return False for command_show_config for: {self.ip}"
                )
            return False