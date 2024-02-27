#!/usr/bin/env python3.10

"""
Mikrotik object with all necessary parameters and functions.
"""

import logging
from modules.devices.base_device import BaseDevice
from modules.connections.conn_ssh import ConnSSH


class Mikrotik(BaseDevice, ConnSSH):
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
            ) -> "BaseDevice":
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
        self.logger = logging.getLogger(
            f"netscriptbackup.devices.Mikrotik"
            )
        self.logger.debug(f"{self.ip}:Creatad.")
        self.device_type = "mikrotik_routeros"

    def get_command_show_config(self):
        self.logger.debug(f"{self.ip}:Returning commands.")
        return "/export"

    def config_filternig(self, config):
        self.logger.debug(f"{self.ip}:Configuration filtering.")
        _tmp_config = []
        config = config.splitlines()
        for line in config:
            if "#" in line:
                self.logger.debug(f"{self.ip}:Skiping line '{line}'.")
                continue
            _tmp_config.append(line)
        config_to_return = "\n".join(_tmp_config)
        return config_to_return


if __name__ == "__main__":
    pass