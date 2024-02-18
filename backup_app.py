#!/usr/bin/env python3
import logging
from modules.config_load import Config_Load
from modules.devices import Devices_Load, Device
from modules.connections import SSH_Connection
from modules.git_operations import Git
import concurrent.futures
from pathlib import Path



CONFIG_LOADED = Config_Load()
LOGGER = CONFIG_LOADED.set_logging()



class Backup():
    """Main application object. Manages the backup process."""

    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        devices_load = Devices_Load()
        devices_load.load_jsons(CONFIG_LOADED.devices_path)
        devices_load.create_devices()
        self.devices = Device.devices_lst
        self.configs_path = CONFIG_LOADED.configs_path


    def _save_config_to_file(self, ip, name, stdout):
        try:
            dir_path = self.configs_path / f"{name}_{ip}"
            file_path = self.configs_path / f"{name}_{ip}" / f"{ip}_conf.txt"

            self.logger.debug(f"{ip} - Check if the folder exist.")

            if not dir_path.is_dir():
                self.logger.info((
                    f"{ip} - The folder doesn't exist ",
                    "or account doesn't have permissions."
                    ))
                self.logger.info(f"{ip} - Creating a folder.")
                dir_path.mkdir()

            try:
                self.logger.debug(f"{ip} - Opening the file.")
                with open(file_path, "w") as f:
                    self.logger.debug(f"{ip} - Writing config.")
                    f.writelines(stdout)
                return True

            except PermissionError:
                self.logger.warning(
                    f"{ip} - The file cannot be opened. Permission error."
                    )
                return False

        except Exception as e:
            self.logger.error(f"{ip} - Error: {e}")
            pass


    def _make_backup(self, dev):
            self.logger.info(f"{dev.ip} - Trying create backup.")
            ssh = SSH_Connection(dev)
            stdout = ssh.get_config()

            if isinstance(stdout, str):
                self.logger.debug(f"{dev.ip} - Writing config to the file.")
                done = self._save_config_to_file(dev.ip, dev.name, stdout)

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
        self.logger.info(f"Start application.")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self._make_backup, self.devices)



def backup_execute():

    data = Backup()
    data.start_backup()

    return True


if __name__ == "__main__":
    pass