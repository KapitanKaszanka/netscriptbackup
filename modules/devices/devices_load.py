#!/usr/bin/env python3.10
import logging
import json
from pathlib import Path
from other.functions import get_and_valid_path
from devices.cisco import Cisco
from devices.mikrotik import Mikrotik
from devices.juniper import Juniper


class Devices_Load:
    """
    An object that collects all the functions 
    needed to create device objects.
    """
    def __init__(self) -> None:
        self.logger: logging = logging.getLogger(
            "netscriptbackup.devices.Devices_Load"
            )

    def load_devices_file(self, path: Path) -> None:
        """
        This function loads devices from device.json file.
        
        :param path: path to devices json file.
        """
        try:
            self.logger.debug("Loading basic devices list.")
            with open(path, "r") as f:
                _loded_devs: dict[dict] = json.load(f)
            self.devices_data: dict[dict] = _loaded_devices
            del _loaded_devices
        except FileNotFoundError as e:
            self.logger.critical(f"{e}")
            exit()
        except json.decoder.JSONDecodeError as e:
            self.logger.critical(f"{e}")
            exit()
        except Exception as e:
            self.logger.critical(f"{e}")
            exit()

    def create_devices(self) -> None:
        """
        The function is responsible for creating 
        all devices based on the loaded json file
        """
        self.logger.info(f"Creating device objects..")
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
                    "passphrase": None
                }
                if devices[ip]["change_privilege"] != None:
                    change_privilege = devices[ip]["change_privilege"]
                    if isinstance(change_privilege, list):
                        if change_privilege[0] != None:
                            device_parametrs["privilege_cmd"] = change_privilege[0]
                        device_parametrs["privilege_password"] = change_privilege[1]
                    else:
                        device_parametrs["privilege_password"] = change_privilege
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
                exit()
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