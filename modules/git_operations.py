#!/usr/bin/env python3

import logging
from pathlib import Path
from datetime import datetime
import subprocess


class Git():


    def __init__(self, configs_path) -> None:
        self.logger = logging.getLogger("backup_app.git_operations.Git")
        self.configs_path = configs_path


    def _create_local_git_repo(self):
        try:
            self.logger.debug(f"Repository don't exist in {self.dir_path}. Creating")
            cmd = subprocess.Popen([
                "/usr/bin/git", "init"],
                cwd = self.dir_path,
                stdout = subprocess.DEVNULL
                )
            output = cmd.communicate()
            _string_output = output[0].decode()

            if "Initialized" not in _string_output:
                self.logger.info(f"Can't initialize git in {self.dir_path}")
                return False

            self.logger.debug(f"Adding all file to repozitory in {self.git_path}")
            cmd = subprocess.Popen(
                ["/usr/bin/git", "add", "-A"],
                cwd = self.dir_path,
                stdout = subprocess.DEVNULL
                )
            
            self.logger.debug(f"Checking status for {self.git_path}")
            cmd = subprocess.Popen(
                ["/usr/bin/git", "status"],
                cwd = self.dir_path,
                stdout = subprocess.DEVNULL
                )
            
            output = cmd.communicate()
            _string_output = output[0].decode()
            
            for line in _string_output.splitlines():
                if "new file:" in line and {self.file_name } in line:
                    self.logger.debug(f"{self.file_name } added to git repozitory.")

                else:
                    self.logger.warning(f"{self.file_name } has not been added to the repository.")
                    return False

        except Exception as e:
            self.logger.error(f"Error ocure: {e}")
            return False


    def _commiting_git_repo(self):
        try:
            self.logger.debug(f"Commiting repository {self.dir_path}")
            cmd = subprocess.Popen(
                ["/usr/bin/git", "commit", "-am", f"{datetime.now().date()}-{datetime.now().time()}"],
                cwd = self.dir_path,
                stdout = subprocess.PIPE
                    )

            output = cmd.communicate()
            _string_output = output[0].decode()

            if "nothing to commit" in _string_output:
                self.logger.info(f"Nothing to commit for {self.ip}")

            elif "file changed" in _string_output:
                self.logger.info(f"Config change for {self.ip}")

            elif "Untracked files" in _string_output:
                self.logger.warning(f"Untracked files in {self.dir_path}")
            
            else:
                self.logger.error("Something goes wrong?")

            return True

        except Exception as e:
            self.logger.error(f"Error ocure: {e}")
            return False


    def git_exceute(self, ip, name):
        self.ip = ip
        self.name = name
        self.dir_path = f"{self.configs_path}/{name}_{ip}"
        self.file_name = f"{ip}_conf.txt"
        self.git_path = f"{self.dir_path}.git"

        self.logger.debug(f"Check if git repozitory exist in {self.self.dir_path}.")
        _git_path_exist = Path(f"{self.dir_path}.git").is_dir()

        if not _git_path_exist:
            self._create_local_git_repo()

        else:
            self.logger.debug(f"Repository exist in {self.dir_path}.")
        
        done = self._commiting_git_repo()

        return done

