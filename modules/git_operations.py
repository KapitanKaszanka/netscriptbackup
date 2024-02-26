#!/usr/bin/env python3.10
"""
Simple implementation of operations on a git repository
"""

import logging
from pathlib import Path
from datetime import datetime
from subprocess import (
    Popen as subproc_Popen,
    DEVNULL as subproc_DEVNULL,
    PIPE as subproc_PIPE
)


class Git:
    """
    An object that collects all 
    the functions needed to operate on the Git repository.
    """

    def __init__(
            self,
            ip: str,
            name: str,
            configs_path: str
            ) -> None:
        """
        :param ip: device ip, used for naming purpose,
        :param name: device name,
        :param configs_path: path to file where configs are store
        """

        self.logger = logging.getLogger(
            "netscriptbackup.git_operations.Git"
            )
        self.ip = ip
        self.name = name
        self.dir_path = configs_path / f"{self.name}_{self.ip}"
        self.file_name = f"{self.ip}_conf.txt"
        self.git_path = Path(f"{self.dir_path}/.git/")

    def _check_file_git_status(self) -> str | bool:
        """
        The function check if file is added to git. If the file is added, 
        the function will return its status, otherwise it will return false.

        :retur: str | bool 
        """

        self.logger.debug(f"{self.ip}:Checking status.")
        try:
            _cmd = subproc_Popen(
                ["/usr/bin/git", "status"],
                cwd=self.dir_path,
                stdout=subproc_PIPE
                )
            _output = _cmd.communicate()
            _string_output = _output[0].decode()
            _git_status = _string_output.splitlines()
            _new_file_index = 0
            _commit_index = 50
            _untracked_index = 100
            for index, line in enumerate(_git_status):
                if line == "Changes to be committed:":
                    _new_file_index = index
                    pass
                elif line == "Changes not staged for commit:":
                    _commit_index = index
                    pass
                elif line == "Untracked files:":
                    _untracked_index = index
                    break
                else:
                    pass
            _status = ""
            for index, line in enumerate(_git_status):
                if "nothing to commit" in line:
                    self.logger.debug(f"{self.ip}:Nothing to commmit.")
                    _status = "nothing"
                    pass
                elif (self.file_name in line and
                      _new_file_index < index < _commit_index):
                    self.logger.debug(
                        f"{self.ip}:The file added to repozitory."
                        )
                    _status = "new_file"
                    pass
                elif (self.file_name in line and
                      _commit_index < index < _untracked_index):
                    self.logger.debug(
                        f"{self.ip}:The file has been modified."
                        )
                    _status = "modify"
                    pass
                elif self.file_name in line and index > _untracked_index:
                    self.logger.warning(
                        f"{self.ip}:The file has not been "
                        "added to the repository."
                        )
                    _status = "untracked"
                    pass
            return _status
        except Exception as e:
            self.logger.error(f"{self.ip}:Check error ocure: {e}")
            return False


    def _add_file_to_git(self) -> bool:
        """
        The function add file to git repozitory.

        :return: bool
        """

        try:
            self.logger.debug(f"{self.ip}:Adding file to repozitory.")
            subproc_Popen(
                ["/usr/bin/git", "add", self.file_name],
                cwd=self.dir_path,
                stdout=subproc_DEVNULL
                )
            return True
        except Exception as e:
            self.logger.error(f"{self.ip}:Add error ocure: {e}")
            return False

    def _create_local_git_repo(self) -> bool:
        """
        The function will create git repozitory in dir_path folder

        :return: bool
        """

        try:
            self.logger.debug(f"{self.ip}:Creating repozitory.")
            _cmd = subproc_Popen([
                "/usr/bin/git", "init"],
                cwd=self.dir_path,
                stdout=subproc_PIPE
                )
            _output = _cmd.communicate()
            _string_output = _output[0].decode()
            if "Initialized empty Git repository" not in _string_output:
                self.logger.warning(f"{self.ip}:Can't initialize git.")
                return False
            if not self._add_file_to_git():
                return False
            if self._check_file_git_status() == "new_file":
                self.logger.debug(
                    f"{self.ip}:Status correct after create git for."
                    )
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"{self.ip}:Create error ocure: {e}")
            return False

    def _commiting_git_repo(self) -> bool:
        """
        The function will commit git repozitory.

        :return: bool
        """

        try:
            timestamp = datetime.now()
            timestamp = timestamp.strftime("%d/%m/%Y - %H:%M:%S")
            self.logger.info(f"{self.ip}:Commiting repository.")
            _cmd = subproc_Popen(
                [
                    "/usr/bin/git",
                    "commit", "-am",
                    timestamp
                ],
                cwd=self.dir_path,
                stdout=subproc_PIPE
                    )
            output = _cmd.communicate()
            _string_output = output[0].decode()
            if "file changed" in _string_output:
                self.logger.info(f"{self.ip}:Commited.")
                return True
            if "files changed" in _string_output:
                self.logger.info(f"{self.ip}:Commited.")
                return True
            elif "Untracked files" in _string_output:
                self.logger.info(f"{self.ip}:Commited.")
                self.logger.warning(f"{self.ip}:Untracked files.")
                return True
            else:
                self.logger.error(f"{self.ip}:Something goes wrong?")
                self.logger.error(f"{self.ip}:{_string_output}")
        except Exception as e:
            self.logger.error(f"{self.ip}:Commit error ocure: {e}")
            return False

    def git_exceute(self) -> bool:
        """
        The function is responsible for performing all necessary operations
        from the Git repository and validating them

        :return: bool
        """

        self.logger.debug(f"{self.ip}:Check if git repozitory exist.")
        if not self.git_path.is_dir():
            self.logger.debug(f"{self.ip}:Repozitory don't exist.")
            _create_local_repo_status = self._create_local_git_repo()
            if not _create_local_repo_status:
                self.logger.warning(
                    f"{self.ip}:Can't create local repozitory."
                    )
                return False
        else:
            self.logger.debug(f"{self.ip}:Repository exist.")
        _file_status = self._check_file_git_status()
        if _file_status == "nothing":
            self.logger.info(f"{self.ip}:Nothing to commit.")
            return True
        elif _file_status == "untracked":
            self.logger.debug(f"{self.ip}:Untracked file.")
            if self._add_file_to_git():
                if self._check_file_git_status() == "untracked":
                    self.logger.warning(
                        f"{self.ip}:Can't add file to repozitory."
                        )
                    return False
                else:
                    self.logger.debug(
                        f"{self.ip}:Added file to repozitory."
                        )
                    return self._commiting_git_repo()
            else:
                self.logger.warning(
                    f"{self.ip}:Can't add file to repozitory."
                    )
                return False
        elif _file_status == "new_file" or "modify":
            self.logger.info(f"{self.ip}:File modify.")
            return self._commiting_git_repo() 
        else:
            return False


if __name__ == "__main__":
    pass

