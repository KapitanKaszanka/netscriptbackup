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


    def _connect(self):
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