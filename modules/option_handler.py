#!/usr/bin/env python3.10
import logging
from pathlib import Path
from config_load import Config_Load
from devices.devices_load import Devices_Load


class Option_Handler:
    """
    An object that collects functions that manage
    the correct execution of the script.
    """

    def __init__(self, backup_files_path: Path) -> None:
        self.logger = logging.getLogger("netscriptbackup.Option_Handler")


if __name__ == "__main__":
    pass
