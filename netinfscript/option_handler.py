#!/usr/bin/env python3.10
import logging
import argparse
from task.backup_task import BackupTask

PARSER_SETUP = {
    "prog": "NetInfScript",
    "description": "Program to creat backup configuration network devices.",
}

PARS_BACKUP = {["-h", "--help"]}


class OptionHandler:
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(self) -> None:
        option_handler = argparse.ArgumentParser(**PARSER_SETUP)
        option_handler.add_argument(**PARS_BACKUP)


# def start_backup(self):
#    """
#    The function used to implement multithreading in a script.
#    """
#    self.logger.info(f"Start creating backup for devices.")
#    execute = Multithreading()
#    execute.execute(self._make_backup_ssh, self.devices)


if __name__ == "__main__":
    pass
