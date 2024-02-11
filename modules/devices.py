#!/usr/bin/env python3.10
import logging

module_logging = logging.getLogger("backup_app.devices")

class Device():

    devices_lst = []

    def __init__(
            self,
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
        self.logger.debug(f"\n\tDevice {self.ip} creatad.")



class Mikrotik(Device):


    def __init__(
            self,
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
        self.logger.debug(f"\n\tDevice {self.ip} creatad.")