#!/usr/bin/env python3

from modules.config_load import Config_Load
import logging
import json
from modules.devices import Device, Cisco, Mikrotik
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException)
import subprocess
from pathlib import Path
from datetime import datetime


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

            self.devices_data = _basic_devs
            self.logger.debug(f"Empty RAM memory.")
            del _basic_devs


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


    def create_devices(self):
        self.logger.info(f"Creating device objects..")
        devices = self.devices_data

        for ip in devices:
            if devices[ip]["vendor"] == "cisco":
                Cisco(
                    name = devices[ip]["name"],
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    device_type = devices[ip]["device_type"],
                    passphrase = devices[ip]["passphrase"],
                    key_file = devices[ip]["key_file"],
                    password = devices[ip]["password"],
                    conf_mode_pass = devices[ip]["conf_mode_pass"]
                )

            elif devices[ip]["vendor"] == "mikrotik":
                Mikrotik(
                    name = devices[ip]["name"],
                    vendor = devices[ip]["vendor"],
                    ip = ip,
                    username = devices[ip]["username"],
                    port = devices[ip]["port"],
                    connection = devices[ip]["connection"],
                    device_type = devices[ip]["device_type"],
                    passphrase = devices[ip]["passphrase"],
                    key_file = devices[ip]["key_file"],
                    password = devices[ip]["password"],
                    conf_mode_pass = devices[ip]["conf_mode_pass"]
                )

            else:
                self.logger.warning(f"Device is not supported. IP: {ip}")
                pass



class SSH_Connection():


    def __init__(self, device) -> None:
        self.logger = logging.getLogger("backup_app.SSH_Connection")
        self.device = device
        if CONFIG_LOADED.ssh_config_file != None:
            self.ssh_config_file = CONFIG_LOADED.ssh_config_file
        else:
            self.ssh_config_file = None


    def _connect(self):
        try:
            self.logger.debug(f"Checking if the host {self.device.ip} is responding")
            ping = ["/usr/bin/ping", "-W", "1", "-c", "4", self.device.ip]
            subprocess.check_output(ping).decode()
            self.logger.debug(f"Device {self.device.ip} responding")

        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Host {self.device.ip} is not responding. Skip.")
            return False
        
        except Exception as e:
            self.logger.error(f"Exception: {e}. Skip")
            return False
        
        connection_parametrs = {
            "host": self.device.ip,
            "username": self.device.username,
            "port": self.device.port,
            "device_type": self.device.device_type,
            "key_file": self.device.key_file,
            "passphrase": self.device.passphrase,
            "password": self.device.password,
            "secret": self.device.conf_mode_pass
        }

        try:
            self.logger.debug(f"Trying create connection to: {self.device.ip}")
            self.client = ConnectHandler(**connection_parametrs)
            return True
        
        except NetmikoTimeoutException as e:
            self.logger.warning(
                f"Can't connect to {self.device.ip}."
                )
            self.logger.warning(f"Error {e}")
            return False

        except NetmikoAuthenticationException as e:
            self.logger.warning(
                f"Can't connect to {self.device.ip}"
                )
            self.logger.warning(f"Error {e}")

        except Exception as e:
            self.logger.error(f"Exceptation {e}")
            return False


    def _close(self):
        try:
            self.logger.debug(f"Closing connection to: {self.device.ip}")
            if self.client.is_alive():
                self.client.disconnect()

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
                stdout = self.client.send_command(
                    command_string = cli_command
                    )
                
                self.logger.debug(f"Reading output from: {self.device.ip}")
                pars_output = self.device.config_parser(stdout)

                self.logger.info(f"Closing connection to: {self.device.ip}")
                self._close()

                return pars_output
        
        else:
            self.logger.warning(f"Can't get config from: {self.device.ip}")
            self._close()
            return False



class Backup():


    def __init__(self) -> None:
        self.logger = logging.getLogger("backup_app.Backup")
        self.devices = Devices_Load()
        self.devices.load_jsons()
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
            # _string = str(cmd).decode()
            # if "nothing to commit" in _string:
            #     self.logger.info(f"Nothing to commit for {ip}")

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