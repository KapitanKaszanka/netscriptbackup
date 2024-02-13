#!/usr/bin/env python3

from configparser import ConfigParser
import logging
import json
from modules.devices import Device, Cisco, Mikrotik
import paramiko
import subprocess
from io import StringIO



class Config_Load():


    def __init__(self):
        self._config = ConfigParser()
        try:
            self._config.read("config.ini")
            self.load_config()

        except KeyError as e:
            print(f"Not allowed atribute: {e}")
            exit()
        except Exception as e:
            print("Can't read config.ini file...")
            exit()


    def load_config(self):
        self.devices_path = self._config["Application_Setup"]["Devices_Path"]
        self.passwords_path = self._config["Application_Setup"]["Passwords_Path"]
        self.configs_path = self._config["Application_Setup"]["Configs_Path"]

        _logging_lv_lst = ["debug", "info", "warning", "error", "critical"]
        _logging_level = self._config["Logging"]["Level"]

        if _logging_level not in _logging_lv_lst:
            print("Not allowed loggin level. Exiting...")
            exit()

        else:
            self.logging_level = _logging_level.lower()

        self._logging_path = self._config["Logging"]["File_Path"]
    
    ## Logging setup
    def set_logging(self):
        logger = logging.getLogger("backup_app")
        if self.logging_level.lower() == "debug":
            logger.setLevel(logging.DEBUG)

        elif self.logging_level.lower() == "info":
            logger.setLevel(logging.INFO)

        elif self.logging_level.lower() == "warning":
            logger.setLevel(logging.WARNING)

        elif self.logging_level.lower() == "error":
            logger.setLevel(logging.ERROR)

        elif self.logging_level.lower() == "critical":
            logger.setLevel(logging.CRITICAL)

        file_handler = logging.FileHandler(self._logging_path)
        if self.logging_level.lower() == "debug":
            file_handler.setLevel(logging.DEBUG)

        elif self.logging_level.lower() == "info":
            file_handler.setLevel(logging.INFO)

        elif self.logging_level.lower() == "warning":
            file_handler.setLevel(logging.WARNING)

        elif self.logging_level.lower() == "error":
            file_handler.setLevel(logging.ERROR)

        elif self.logging_level.lower() == "critical":
            file_handler.setLevel(logging.CRITICAL)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.ERROR)

        formatter = logging.Formatter(
            "%(asctime)s:%(name)s:%(levelname)s:\n\t%(message)s"
            )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger


CONFIG_LOADED = Config_Load()
LOGGER = CONFIG_LOADED.set_logging()


class Devices_Load():
    """Class loads device and store this in object."""


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Devices_Load")


    def load_jsons(self):
        try:
            self.logger.debug("Loading basic devices list.")
            with open(CONFIG_LOADED.devices_path) as f:
                _basic_devs = json.load(f)
            self.logger.debug("Loading passwords list.")
            with open(CONFIG_LOADED.passwords_path) as f:
                _passwords = json.load(f)

            def mergign_dcts(dct1, dct2):
                self.logger.debug("Merging devices and passwords files.")
                dev_to_remove = []
                for key in dct1.keys():
                    try:
                        self.logger.debug(f"Trying merge passphrase info for device: {key}.")
                        dct1[key]["passphrase"] = dct2[key]["passphrase"]
                        self.logger.debug(f"Trying password passphrase info for device: {key}.")
                        dct1[key]["password"] = dct2[key]["password"]
                        self.logger.debug(f"Trying merge config_pass info for device: {key}.")
                        dct1[key]["conf_mode_pass"] = dct2[key]["conf_mode_pass"]

                    except KeyError as e:
                        self.logger.warning(
                            f"Key error, check devices or passwords file for ip: {e}"
                            )
                        self.logger.warning(
                            f"Skip device {key}, because lack of informations."
                            )
                        self.logger.debug(f"Append {key} to remove list.")
                        dev_to_remove.append(key)
                        pass

                    except Exception as e:
                        self.logger.error(
                            f"Problem ocure: {e}"
                            )
                        self.logger.warning(
                            f"Skip device {key}, because error."
                            )
                        self.logger.debug(f"Append {key} to remove list.")
                        dev_to_remove.append(key)
                        pass
                
                if len(dev_to_remove) != 0:
                    self.logger.debug("Removing items.")
                    for ip in dev_to_remove:
                        self.logger.debug(f"Removing {ip}.")
                        dct1.pop(ip)

                return dct1
            
            self.devices_data = mergign_dcts(_basic_devs, _passwords)
            self.logger.debug(f"Empty RAM memory.")
            del _basic_devs
            del _passwords

        except FileNotFoundError as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            exit()

        except json.decoder.JSONDecodeError as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            print()
            exit()

        except Exception as e:
            print()
            self.logger.critical(f"{e}")
            print("#! Exiting...")
            print()
            exit()



class SSH_Connection():


    def __init__(self, device) -> None:
        self.logger = logging.getLogger("backup_app.SSH_Connection")
        self.device = device


    def _connect(self):
        try:
            self.logger.debug(f"Checking if the host {self.device.ip} is responding")
            ping = ["ping", "-W", "1", "-c", "4", self.device.ip]
            subprocess.check_output(ping).decode()

        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Host {self.device.ip} is not responding. Skip.")
            return False
        
        except Exception as e:
            self.logger.error(f"Exception: {e}. Skip")
            return False

        try:
            self.logger.debug(f"Trying create connection with public key to: {self.device.ip}")
            self.client = paramiko.SSHClient()
            self.client.load_system_host_keys()
            self.client.connect(
                hostname = self.device.ip,
                port = self.device.port,
                username = self.device.username,
                passphrase = self.device.passphrase
            )
            return True
        
        except paramiko.BadHostKeyException as e:
            self.logger.warning(f"Bad host key{e}")
            return False
        
        except paramiko.AuthenticationException as e:
            self.logger.warning(f"{e}: {self.device.ip}")
            return False
        
        except paramiko.SSHException as e:
            if "known_hosts" in str(e):
                self.logger.warning(
                    f"Can't connect. You need to add key policy for host: {self.device.ip}"
                    )
                return False
            
            # elif "Invalid key" in str(e):
            #     self.logger.warning(
            #         f"Can't connectto {self.device.ip}. Invalid key"
            #         )
            #     return False
            
            else:
                self.logger.debug(f"Trying create connection with password to: {self.device.ip}")
                self.client = paramiko.SSHClient()
                self.client.connect(
                    hostname = self.device.ip,
                    port = self.device.port,
                    username = self.device.username,
                    password = self.device.password,
                    allow_agent = False,
                    look_for_keys = False
                )
                return True
        
        except Exception as e:
            self.logger.error(f"Exceptation {e}")
            return False


    def _close(self):
        try:
            self.logger.debug(f"Closing connection to: {self.device.ip}")
            if self.client.get_transport().is_active():
                self.client.close()

            else:
                self.logger.debug(f"Connection to {self.device.ip} was not opened.")
                pass

        except:
            self.logger.debug(f"Connection to {self.device.ip} was not opened.")
            pass


    def get_config(self):

        self.logger.info(f"Opening a connection to: {self.device.ip}")
        connection = self._connect()

        if connection:
            self.logger.info(f"Getting config from: {self.device.ip}")
            
            self.logger.debug(f"Getting commands to send for device: {self.device.ip}")
            cli_command = self.device.command_show_config()

            if not cli_command:
                self.logger.warning(
                    f"Can't get command. Check soft name for: {self.device.ip}"
                    )
                return False
            
            else:
                self.logger.debug(f"Sending commands to: {self.device.ip}")
                stdin, stdout, stderr = self.client.exec_command(
                    command = cli_command,
                    bufsize = 10_000,
                    timeout = 2
                    )
                
                self.logger.debug(f"Reading output from: {self.device.ip}")
                stdout = stdout.readlines()

                self.logger.info(f"Closing connection to: {self.device.ip}")
                self._close()

                return stdout
        
        else:
            self.logger.warning(f"Can't get config from: {self.device.ip}")
            self._close()
            return False



class Backup():


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Devices_Load()
        self.devices.load_jsons()


    def create_devices(self):
        devices = self.devices.devices_data

        for ip in devices:
            if devices[ip]["vendor"] == "cisco":
                Cisco(
                    name = devices[ip]["name"],
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    soft = devices[ip]["soft"],
                    password = devices[ip]["password"],
                    passphrase = devices[ip]["passphrase"]
                )

            elif devices[ip]["vendor"] == "mikrotik":
                Mikrotik(
                    name = devices[ip]["name"],
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    soft = devices[ip]["soft"],
                    password = devices[ip]["password"],
                    passphrase = devices[ip]["passphrase"]
                )
                
            else:
                self.logger.warning(f"Device is not supported. IP: {ip}")
                pass


    def get_configuration(self):
        for dev in Device.devices_lst:
            self.logger.info(f"Start creating backup for: {dev.ip}")
            ssh = SSH_Connection(dev)
            stdout = ssh.get_config()

            if not stdout:
                self.logger.warning(f"Config is empty for: {dev.ip}")
                pass

            else:
                self.logger.debug("Writing config to file.")
                self.write_config(dev.ip, dev.name, stdout)


    def write_config(self, ip, name, stdout):
        try:
            self.logger.debug(
                f"Opening file: {CONFIG_LOADED.configs_path}/{name}_{ip}.txt"
                )
            file_path = f"{CONFIG_LOADED.configs_path}/{name}_{ip}.txt"
            with open(file_path, "w") as f:
                f.writelines(stdout)

        except FileNotFoundError as e:
            self.logger.error(f"File or dictionary not found: {file_path}")
            pass



def backup_execute():

    data = Backup()
    data.create_devices()
    data.get_configuration()

    return True


if __name__ == "__main__":
    pass