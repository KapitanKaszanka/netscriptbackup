#!/usr/bin/env python3
import logging
from modules.config_load import Config_Load
from modules.devices import Devices_Load, Device
from modules.connections import SSH_Connection
from modules.git_operations import Git
import subprocess
from pathlib import Path



CONFIG_LOADED = Config_Load()
LOGGER = CONFIG_LOADED.set_logging()



class Backup():


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Devices_Load()
        self.devices.load_jsons(CONFIG_LOADED.devices_path)
        self.devices.create_devices()
        self.configs_path = CONFIG_LOADED.configs_path
        self.git = Git()


    def _file_working(self, ip, name, stdout):
        try:
            dir_path = f"{self.configs_path}/{name}_{ip}"
            file_path = f"{self.configs_path}/{name}_{ip}/{ip}_conf.txt"

            path = Path(dir_path)

            self.logger.debug(f"Check if folder {dir_path} exist.")

            if not path.is_dir():
                self.logger.debug(
                    f"Folder {dir_path}/ don't exist or account don't have permionss. Creating."
                    )
                path.mkdir()

            try:
                self.logger.debug(f"Opening file: {file_path}")
                with open(file_path, "w") as f:
                    self.logger.debug(f"Writing config for {ip}")
                    f.writelines(stdout)
                return True

            except PermissionError:
                self.logger.warning(f"Can't open {file_path}. Permission error.")
                return False

        except Exception as e:
            self.logger.error(f"Error: {e}")
            pass


    def execute_backup(self):
        for dev in Device.devices_lst:
            self.logger.info(f"Start creating backup for: {dev.ip}")
            ssh = SSH_Connection(dev)
            stdout = ssh.get_config()

            if isinstance(stdout, str):
                self.logger.debug(f"Writing config to file for {dev.ip}.")
                done = self._file_working(dev.ip, dev.name, stdout)

                if done:
                    self.logger.debug(f"Git commands execute {dev.ip}")
                    done = self.git.git_exceute(dev.ip, dev.name)
                    if not done:
                        self.logger.warning(f"Can't create backup config {dev.ip}")
                        pass

                else:
                    self.logger.warning(f"Can't create backup config {dev.ip}")
                    pass

            else:
                self.logger.warning(f"Can't connect to device {dev.ip}")
                pass



def backup_execute():

    data = Backup()
    data.execute_backup()

    return True


if __name__ == "__main__":
    pass