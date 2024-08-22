#!/usr/bin/env python3.10
import logging
import json
import sys
from pathlib import Path

from netinfscript.functions import get_and_valid_path
from netinfscript.devices.cisco import Cisco
from netinfscript.devices.mikrotik import Mikrotik
from netinfscript.devices.juniper import Juniper


class Devices_Load:
    """
    an object that collects all the functions
    needed to create device objects.
    """

    def __init__(self, path: Path) -> None:
        self.logger: logging = logging.getLogger(
            "netscriptbackup.devices.Devices_Load"
        )
        self.devices_path = path

    def _load_devices_file(self) -> None:
        """
        this function loads devices from device.json file.

        :param path: path to devices json file.
        """
        try:
            self.logger.debug("Loading basic devices list.")
            with open(self.devices_path, "r") as f:
                _loaded_devices: dict[dict] = json.load(f)
            self.devices_data: dict[dict] = _loaded_devices
            del _loaded_devices
        except FileNotFoundError as e:
            self.logger.critical(f"{e}")
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            self.logger.critical(f"{e}")
            sys.exit(1)
        except Exception as e:
            self.logger.critical(f"{e}")
            sys.exit(2)

    def create_devices(self) -> None:
        """
        the function is responsible for creating
        all devices based on the loaded json file
        """
        self.logger.debug(f"Loading devices file...")
        self._load_devices_file(self.devices_path)
        self.logger.info(f"Creating device objects...")
        devices: dict[dict] = self.devices_data
        for ip in devices:
            try:
                device_parametrs: dict = {
                    "ip": ip,
                    "port": devices[ip]["port"],
                    "name": devices[ip]["name"],
                    "vendor": devices[ip]["vendor"],
                    "connection": devices[ip]["connection"],
                    "username": devices[ip]["username"],
                    "password": devices[ip]["password"],
                    "privilege_cmd": "",
                    "privilege_password": None,
                    "key_file": None,
                    "passphrase": None,
                }
                if devices[ip]["privilege"] != None:
                    privilege: list[str | None] | None = devices[ip][
                        "privilege"
                    ]
                    if isinstance(privilege, list):
                        if privilege[0] != None:
                            device_parametrs["privilege_cmd"] = privilege[0]
                        device_parametrs["privilege_password"] = privilege[1]
                    else:
                        device_parametrs["privilege_password"] = privilege
                if devices[ip]["key_file"] != None:
                    device_parametrs["key_file"] = get_and_valid_path(
                        devices[ip]["key_file"]
                    )
                    if device_parametrs == None:
                        pass
                    device_parametrs["passphrase"] = devices[ip]["passphrase"]
            except KeyError as e:
                self.logger.warning(f"{ip}:KeyError in devices file: {e}")
                pass
            except Exception as e:
                self.logger.critical(f"Error ocure {e}")
                sys.exit(2)
            if devices[ip]["vendor"] == "cisco":
                Cisco(**device_parametrs)
            elif devices[ip]["vendor"] == "mikrotik":
                Mikrotik(**device_parametrs)
            elif devices[ip]["vendor"] == "juniper":
                Juniper(**device_parametrs)
            else:
                self.logger.warning(f"{ip}:Device is not supported.")
                pass


if __name__ == "__main__":
    pass
