#!/usr/bin/env python3

import logging
from subprocess import (
    check_output as subproc_check_outpu,
    CalledProcessError as subproc_CalledProcessError
)
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)



class SSH_Connection():


    def __init__(self, device) -> None:
        self.logger = logging.getLogger("backup_app.connections.SSH_Connection")
        self.device = device


    def get_config(self):
        try:
            self.logger.debug(f"Checking if the host {self.device.ip} is responding")
            ping = ["/usr/bin/ping", "-W", "1", "-c", "4", self.device.ip]
            subproc_check_outpu(ping).decode()
            self.logger.debug(f"Device {self.device.ip} responding")

        except subproc_CalledProcessError as e:
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
        self.logger.info(f"Getting config from: {self.device.ip}")

        self.logger.debug(f"Getting commands to send for device: {self.device.ip}")
        cli_command = self.device.command_show_config()
        
        try:
            self.logger.debug(f"Trying create connection to: {self.device.ip}")
            with ConnectHandler(**connection_parametrs) as connection:
                self.logger.debug(f"Sending commands to: {self.device.ip}")
                stdout = connection.send_command(
                    command_string = cli_command
                    )

            self.logger.debug(f"Processing the configuration file: {self.device.ip}")
            pars_output = self.device.config_parser(stdout)

            return pars_output
        
        except NetmikoTimeoutException as e:
            self.logger.warning(f"Can't connect to {self.device.ip}.")
            self.logger.warning(f"Error {e}")
            return False

        except NetmikoAuthenticationException as e:
            self.logger.warning(f"Can't connect to {self.device.ip}")
            self.logger.warning(f"Error {e}")
            return False

        except Exception as e:
            self.logger.error(f"Exceptation {e}")
            return False