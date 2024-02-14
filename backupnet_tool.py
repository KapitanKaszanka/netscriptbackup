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


    def get_configuration(self):
        for dev in Device.devices_lst:
            self.logger.info(f"Start creating backup for: {dev.ip}")
            ssh = SSH_Connection(dev)
            stdout = ssh.get_config()

            if not stdout:
                self.logger.warning(f"Config is empty for: {dev.ip}")
                pass

            else:
                self.logger.info("Writing config to file and execute git commit.")
                self.logger.debug("Writing config to file.")
                path = CONFIG_LOADED.configs_path
                done = self.write_config(path, dev.ip, dev.name, stdout)
                if done:
                    self.logger.debug("Git commands execute.")
                    done = self.git_execute(path, dev.ip, dev.name)
                    if not done:
                        self.logger.error("Can't create backup config.")
                        pass
                else:
                    self.logger.error("Can't create backup config.")
                    pass


    def write_config(self, path, ip, name, stdout):
        try:
            file_path = f"{path}/{name}_{ip}/"
            path = Path(file_path)

            self.logger.debug(f"Check if folder {file_path} exist.")

            if not path.is_dir():
                self.logger.debug(
                    f"Folder {file_path} don't exist or account don't have permionss. Creating."
                    )
                path.mkdir()

            try:
                self.logger.debug(f"Opening file: {file_path}config.txt")
                with open(f"{file_path}config.txt", "w") as f:
                    self.logger.debug(f"Writing config for {ip}")
                    f.writelines(stdout)
                return True

            except PermissionError:
                self.logger.warning(f"Can't open {file_path}/config.txt. Permission error.")
                return False

        except Exception as e:
            self.logger.error(f"Error: {e}")
            pass


    def git_execute(self, path, ip, name):
        file_path = f"{path}/{name}_{ip}/"
        self.logger.debug(f"Check if git repozitory exist in {file_path}.")
        git_path = Path(f"{file_path}.git").is_dir()

        if not git_path:
            try:
                self.logger.debug(f"Repository don't exist in {file_path}. Creating")
                cmd = subprocess.Popen([
                    "/usr/bin/git", "init"],
                    cwd = file_path,
                    stdout = subprocess.DEVNULL
                    )
                cmd.communicate()
                
                self.logger.debug(f"Adding all file to repozitory in {file_path}")
                cmd = subprocess.Popen(
                    ["/usr/bin/git", "add", "-A"],
                    cwd = file_path,
                    stdout = subprocess.DEVNULL
                    )
                cmd.communicate()

            except Exception as e:
                self.logger.error(f"Error ocure: {e}")
                return False
        else:
            self.logger.debug(f"Repository exist in {file_path}.")

        try:
            self.logger.info(f"Commiting repository {file_path}")
            cmd = subprocess.Popen(
                ["/usr/bin/git", "commit", "-am", f"{datetime.now().date()}-{datetime.now().time()}"],
                cwd = file_path,
                stdout = subprocess.PIPE
                    )

            output = cmd.communicate()
            _string_output = output[0].decode()

            if "nothing to commit" in _string_output:
                self.logger.info(f"Nothing to commit for {ip}")
            elif "file changed" in _string_output and "rewrite" in _string_output:
                self.logger.info(f"Config change for {ip}")
            elif "Untracked files" in _string_output:
                self.logger.warning(f"Untracked files in {file_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error ocure: {e}")
            return False



def backup_execute():

    data = Backup()
    data.get_configuration()

    return True


if __name__ == "__main__":
    pass