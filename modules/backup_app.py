#!/usr/bin/env python3.10
import logging
from modules.config_load import Config_Load
from modules.devices import Devices_Load, Device
from modules.connections.ssh import SSH_Connection
from modules.git_operations import Git
from concurrent.futures import ThreadPoolExecutor
from modules.functions import save_config_to_file


class Aplication():
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(
            self, 
            configs_path: str | object
            ) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Device.devices_lst
        self.configs_path = configs_path

    def _make_backup_ssh(
            self, 
            dev: object
            ) -> bool:
        """
        The functions is responsible for creating bakup with ssh module.

        :param dev: device object,
        
        :return bool: done or not.
        """

        self.logger.info(f"{dev.ip} - Trying create backup.")
        ssh = SSH_Connection(dev)
        stdout = ssh.get_config()
        if isinstance(stdout, str):
            self.logger.debug(f"{dev.ip} - Writing config to the file.")
            done = save_config_to_file(dev.ip, dev.name, stdout)
            if done:
                self.logger.debug(f"{dev.ip} - Git commands execute.")
                _git = Git(dev.ip, dev.name, self.configs_path)
                done = _git.git_exceute()
                if done:
                    self.logger.info(f"{dev.ip} - Backup completed.")
                    return True
                else:
                    self.logger.warning(
                        f"{dev.ip} - Unable to create backup."
                        )
                    return False
            else:
                self.logger.warning(f"{dev.ip} - Unable to create backup.")
                return False
        else:
            self.logger.warning(
                f"{dev.ip} - Unable to connect to device."
                )
            return False

    def start_backup(self):
        """
        Functions used to implement multithreading in a script
        """

        self.logger.info(f"Start creating backup for devices.")
        with ThreadPoolExecutor() as executor:
            executor.map(self._make_backup_ssh, self.devices)


def _init_system():
    """The function initialize all needed objects."""

    CONFIG_LOADED = Config_Load()
    CONFIG_LOADED.set_logging()
    devices_load = Devices_Load()
    devices_load.load_jsons(CONFIG_LOADED.devices_path)
    devices_load.create_devices()
    return Aplication(CONFIG_LOADED.configs_path)


def backup_execute():
    app = _init_system()
    app.start_backup()
    return True


if __name__ == "__main__":
    pass