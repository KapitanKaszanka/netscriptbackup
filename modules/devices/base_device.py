#!/usr/bin/env python3.10

class BaseDevice:
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
        BaseDevice.devices_lst.append(self)

    def config_filternig(self, config):
        return config


if __name__ == "__main__":
    pass