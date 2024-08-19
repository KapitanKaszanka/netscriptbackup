#!/usr/bin/env python3.10

class BaseDevice:
    """
    main device object. Assigns all necessary information.
    returns appropriate variables when the object's child
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
            privilege_cmd: str,
            privilege_password: str,
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
        self.privilege_cmd = privilege_cmd
        self.privilege_password = privilege_password
        BaseDevice.devices_lst.append(self)

    def config_filternig(self, config):
        return config


if __name__ == "__main__":
    pass