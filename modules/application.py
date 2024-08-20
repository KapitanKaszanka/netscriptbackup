#!/usr/bin/env python3.10
import logging
from pathlib import Path
from config_load import Config_Load
from devices.devices_load import Devices_Load
from multithreading import Multithreading
from devices.base_device import BaseDevice
from git_operations import Git
from other.functions import save_to_file


class Application:
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(self, backup_files_path: Path) -> None:
        self.logger = logging.getLogger("netscriptbackup.Application")
        self.devices: list[BaseDevice] = BaseDevice.devices_lst
        self.backup_files_path = backup_files_path

    def _make_backup_ssh(self, dev: object) -> bool:
        """
        The functions is responsible for creating bakup with object.

        :param dev: device object,
        :return bool: done or not.
        """
        self.logger.info(f"{dev.ip}:Attempting to create a backup.")
        config_string: str | None = dev.get_config()

        if config_string is not None:
            self.logger.debug(f"{dev.ip}:Saving the configuration to a file.")
            done: bool = save_to_file(
                self.backup_files_path, dev.ip, dev.name, config_string
            )
            if done:
                self.logger.info(f"{dev.ip}:Operating on the Git repository.")
                _git = Git(dev.ip, dev.name, self.backup_files_path)
                done = _git.git_execute()
                if done:
                    self.logger.info(f"{dev.ip}:Backup created.")
                    return True
                else:
                    self.logger.warning(f"{dev.ip}:Unable to create backup.")
                    return False
            else:
                self.logger.warning(f"{dev.ip}:Unable to create backup.")
                return False
        else:
            self.logger.warning(f"{dev.ip}:Unable to connect to device.")
            return False

    def start_backup(self):
        """
        The function used to implement multithreading in a script.
        """
        self.logger.info(f"Start creating backup for devices.")
        execute = Multithreading()
        execute.execute(self._make_backup_ssh, self.devices)


def _init_system():
    """The function initialize all needed objects."""
    config_loaded = Config_Load()
    config_loaded.set_logging()
    devices_load = Devices_Load()
    devices_load.load_devices_file(config_loaded.devices_path)
    devices_load.create_devices()
    return Application(config_loaded.configs_path)


def backup_execute():
    """
    The function starts backing up the device configuration.
    """
    app = _init_system()
    app.start_backup()
    return True


if __name__ == "__main__":
    pass
