#!/usr/bin/env python3
import logging
from modules.config_load import Config_Load
from modules.devices import Devices_Load, Device
from modules.connections import SSH_Connection
import subprocess
from pathlib import Path
from datetime import datetime



CONFIG_LOADED = Config_Load()
LOGGER = CONFIG_LOADED.set_logging()



class Backup():


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Devices_Load()
        self.devices.load_jsons(CONFIG_LOADED.devices_path)
        self.devices.create_devices()
        self.configs_path = CONFIG_LOADED.configs_path


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


    def _git_working(self, ip, name):
        dir_path = f"{self.configs_path}/{name}_{ip}"
        file_name = f"{ip}_conf.txt"

        self.logger.debug(f"Check if git repozitory exist in {dir_path}.")
        git_path = Path(f"{dir_path}.git").is_dir()

        if not git_path:
            try:
                self.logger.debug(f"Repository don't exist in {dir_path}. Creating")
                cmd = subprocess.Popen([
                    "/usr/bin/git", "init"],
                    cwd = dir_path,
                    stdout = subprocess.DEVNULL
                    )
                output = cmd.communicate()
                _string_output = output[0].decode()

                if "Initialized" not in _string_output:
                    self.logger.info(f"Can't initialize git in {dir_path}")
                    return False

                self.logger.debug(f"Adding all file to repozitory in {git_path}")
                cmd = subprocess.Popen(
                    ["/usr/bin/git", "add", "-A"],
                    cwd = dir_path,
                    stdout = subprocess.DEVNULL
                    )
                
                self.logger.debug(f"Checking status for {git_path}")
                cmd = subprocess.Popen(
                    ["/usr/bin/git", "status"],
                    cwd = dir_path,
                    stdout = subprocess.DEVNULL
                    )
                
                output = cmd.communicate()
                _string_output = output[0].decode()
                
                for line in _string_output.splitlines():
                    if "new file:" in line and {file_name} in line:
                        self.logger.debug(f"{file_name} added to git repozitory.")

                    else:
                        self.logger.warning(f"{file_name} has not been added to the repository.")
                        return False

            except Exception as e:
                self.logger.error(f"Error ocure: {e}")
                return False
        else:
            self.logger.debug(f"Repository exist in {dir_path}.")

        try:
            self.logger.debug(f"Commiting repository {dir_path}")
            cmd = subprocess.Popen(
                ["/usr/bin/git", "commit", "-am", f"{datetime.now().date()}-{datetime.now().time()}"],
                cwd = dir_path,
                stdout = subprocess.PIPE
                    )

            output = cmd.communicate()
            _string_output = output[0].decode()

            if "nothing to commit" in _string_output:
                self.logger.info(f"Nothing to commit for {ip}")

            elif "file changed" in _string_output:
                self.logger.info(f"Config change for {ip}")

            elif "Untracked files" in _string_output:
                self.logger.warning(f"Untracked files in {dir_path}")
            
            else:
                self.logger.error("Something goes wrong?")

            return True

        except Exception as e:
            self.logger.error(f"Error ocure: {e}")
            return False


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
                    done = self._git_working(dev.ip, dev.name)
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