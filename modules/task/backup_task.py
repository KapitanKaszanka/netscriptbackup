#!/usr/bin/env python3.10
import logging
from git_operations import Git
from modules.functions import save_to_file


class Backup_Task:
    def _make_backup_ssh(self, dev: object) -> bool:
        """
        the functions is responsible for creating bakup with object.

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
