#!/usr/bin/env python3.10
"""
simple implementation of operations on a git repository
"""

import logging
from pathlib import Path
from datetime import datetime
from subprocess import (
    Popen as subproc_Popen,
    DEVNULL as subproc_DEVNULL,
    PIPE as subproc_PIPE,
)


class Git:
    """
    an object that collects all the functions
    needed to operate on the Git repository.
    """

    def __init__(self, ip: str, name: str, configs_path: str) -> None:
        """
        :param ip: str device ip, used for naming purpose,
        :param name: str device name,
        :param configs_path: str path to dir where configs are store
        """
        self.logger = logging.getLogger("netscriptbackup.git_operations.Git")
        self.ip = ip
        self.name = name
        self.dir_path: Path = configs_path / f"{self.name}_{self.ip}"
        self.file_name: str = f"{self.ip}_conf.txt"
        self.git_path: Path = self.dir_path / ".git"

    def _check_file_git_status(self) -> int:
        """
        the function checks the file status in the local Git repository.

        :return: int    |0:nothing
                        |1:new_file
                        |2:modify
                        |3:untracked
                        |4:error
        """
        self.logger.debug(f"{self.ip}:Checking status.")
        try:
            _cmd = subproc_Popen(
                ["/usr/bin/git", "status"],
                cwd=self.dir_path,
                stdout=subproc_PIPE,
            )
            _output = _cmd.communicate()
            _string_output = _output[0].decode()
            _git_status = _string_output.splitlines()
            _new_file_index = 0
            _commit_index = 50
            _untracked_index = 100
            # set the indexes of the appropriate lines
            # to check the status of the file
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
            _status = 4
            for index, line in enumerate(_git_status):
                if "nothing to commit" in line:
                    self.logger.debug(f"{self.ip}:Nothing to commmit.")
                    _status = 0
                    pass
                elif (
                    self.file_name in line
                    and _new_file_index < index < _commit_index
                ):
                    self.logger.debug(
                        f"{self.ip}:The file added to repozitory."
                    )
                    _status = 1
                    pass
                elif (
                    self.file_name in line
                    and _commit_index < index < _untracked_index
                ):
                    self.logger.debug(f"{self.ip}:The file has been modified.")
                    _status = 2
                    pass
                elif self.file_name in line and index > _untracked_index:
                    self.logger.warning(
                        f"{self.ip}:The file has not been "
                        "added to the repository."
                    )
                    _status = 3
                    pass
            return _status
        except Exception as e:
            self.logger.error(
                f"{self.ip}:An error occurred while checking: {e}"
            )
            return 4

    def _add_file_to_git(self) -> bool:
        """
        the function adds the file to the git repository

        :return: True when the process completes successfully
                 or Flase when a problem occurs.
        """
        try:
            self.logger.debug(f"{self.ip}:Adding file to repozitory.")
            subproc_Popen(
                ["/usr/bin/git", "add", self.file_name],
                cwd=self.dir_path,
                stdout=subproc_DEVNULL,
            )
            return True
        except Exception as e:
            self.logger.error(
                f"{self.ip}:There was a problem "
                f"adding the file to the repository - {e}"
            )
            return False

    def _create_local_git_repo(self) -> bool:
        """
        The function will create git repozitory in dir_path folder

        :return: bool
        """
        try:
            self.logger.debug(f"{self.ip}:Creating repozitory.")
            _cmd = subproc_Popen(
                ["/usr/bin/git", "init"],
                cwd=self.dir_path,
                stdout=subproc_PIPE,
            )
            _output = _cmd.communicate()
            _string_output = _output[0].decode()
            if "Initialized empty Git repository" not in _string_output:
                self.logger.warning(f"{self.ip}:Couldn't initialize git.")
                return False
            if not self._add_file_to_git():
                return False
            if self._check_file_git_status() == 1:
                self.logger.debug(
                    f"{self.ip}:Correct status after git initialization."
                )
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(
                f"{self.ip}:An error occurred while "
                "creating the repository - {e}"
            )
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
                ["/usr/bin/git", "commit", "-am", timestamp],
                cwd=self.dir_path,
                stdout=subproc_PIPE,
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
            self.logger.error(
                f"{self.ip}:An error occurred while "
                f"committing the repository: {e}"
            )
            return False

    def git_execute(self) -> bool:
        """
        the function is responsible for performing all necessary operations
        from the Git repository and validating them.

        :return: bool
        """
        self.logger.debug(f"{self.ip}:Checking if git repozitory exists.")
        if not self.git_path.is_dir():
            self.logger.debug(f"{self.ip}:The local repozitory doesn't exist.")
            _create_local_repo_status = self._create_local_git_repo()
            if not _create_local_repo_status:
                self.logger.warning(
                    f"{self.ip}:Couldn't create local repozitory."
                )
                return False
        else:
            self.logger.debug(f"{self.ip}:Repository exist.")
        _file_status: int = self._check_file_git_status()
        if _file_status == 0:
            self.logger.info(f"{self.ip}:Nothing to commit.")
            return True
        elif _file_status == 3:
            self.logger.debug(f"{self.ip}:Untracked file.")
            if self._add_file_to_git():
                if self._check_file_git_status() == 3:
                    self.logger.warning(
                        f"{self.ip}:The file couldn't "
                        "be added to the repository"
                    )
                    return False
                else:
                    self.logger.debug(
                        f"{self.ip}:Added the file to the repozitory."
                    )
                    return self._commiting_git_repo()
            else:
                self.logger.warning(
                    f"{self.ip}:The file couldn't be added to the repository"
                )
                return False
        elif _file_status == 1 or 2:
            self.logger.info(f"{self.ip}:The file modified.")
            return self._commiting_git_repo()
        else:
            return False


if __name__ == "__main__":
    pass
