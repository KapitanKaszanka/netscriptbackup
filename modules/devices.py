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
            conf_mode_pass: str
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
        self.conf_mode_pass = conf_mode_pass
        Device.devices_lst.append(self)



class Cisco(Device):

    soft_supported = ["ios"]

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
            conf_mode_pass: str
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
            passphrase,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Cisco")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.soft  in Cisco.soft_supported:
            self.logger.debug(f"Command return for device: {self.ip}")
            return "show running-config"
        else:
            self.logger.info(
                f"Return False for command_show_config for: {self.ip}"
                )
            return False



class Mikrotik(Device):


    soft_supported = ["ros_v6", "ros_v7"]


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
            conf_mode_pass: str
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
            passphrase,
            conf_mode_pass
            )
        self.logger = logging.getLogger("backup_app.devices.Mikrotik")
        self.logger.debug(f"Device {self.ip} creatad.")


    def command_show_config(self):
        if self.soft in Mikrotik.soft_supported:
            self.logger.debug(
                f"Command return for device: {self.ip}"
                )
            return "export"
        
        else:
            self.logger.warning(
                f"Soft type not supported: {self.ip}"
                )
            return False