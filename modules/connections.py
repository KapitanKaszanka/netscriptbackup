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
            self.logger.debug(f"{self.device.ip} - Checking if the host is responding")
            ping = ["/usr/bin/ping", "-W", "1", "-c", "4", self.device.ip]
            subproc_check_outpu(ping).decode()
            self.logger.debug(f"{self.device.ip} - The host responds")

        except subproc_CalledProcessError as e:
            self.logger.warning(f"{self.device.ip} - Host isn't responding. Skip.")
            return False

        except Exception as e:
            self.logger.error(f"{self.device.ip} - Exception: {e}. Skip")
            return False

        connection_parametrs = {
            "host": self.device.ip,
            "username": self.device.username,
            "port": self.device.port,
            "device_type": self.device.device_type,
            "password": self.device.password,
            "secret": self.device.conf_mode_pass,
            "key_file": self.device.key_file,
            "passphrase": self.device.passphrase
        }
        self.logger.info(f"{self.device.ip} - Downloading configuration from the device.")

        self.logger.debug(f"{self.device.ip} - Downloading the necessary commands.")
        cli_command = self.device.command_show_config()

        try:
            self.logger.debug(f"{self.device.ip} - Attempting to create an SSH connection.")
            if connection_parametrs["key_file"] == None:
                self.logger.debug(f"{self.device.ip} - Connecting with password.")
                with ConnectHandler(
                    **connection_parametrs,
                    ssh_strict = True,
                    system_host_keys = True
                    ) as connection:
                    self.logger.debug(f"{self.device.ip} - Connection created.")
                    self.logger.debug(f"{self.device.ip} - Sending commands.")
                    stdout = connection.send_command(
                        command_string = cli_command,
                        read_timeout = 30
                        )
                self.logger.debug(f"{self.device.ip} - Connection completend sucessfully.")

            else:
                self.logger.debug(f"{self.device.ip} - Connecting with public key.")
                with ConnectHandler(
                    **connection_parametrs,
                    use_keys = True,
                    ssh_strict = True,
                    system_host_keys = True
                    ) as connection:
                    self.logger.debug(f"{self.device.ip} - Connection created.")
                    self.logger.debug(f"{self.device.ip} - Sending commands.")
                    stdout = connection.send_command(
                        command_string = cli_command,
                        read_timeout = 30
                        )
                self.logger.debug(f"{self.device.ip} - Connection completend sucessfully.")

        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.warning(
                    f"{self.device.ip} - Can't connect. Device not found in known_host file."
                )
                return False
            
            else:
                self.logger.warning(f"{self.device.ip} - Can't connect. {e}")
                return False
            
        except NetmikoAuthenticationException as e:
            self.logger.warning(f"{self.device.ip} - Can't connect.")
            self.logger.warning(f"{self.device.ip} - Error {e}")
            return False

        except ValueError:
            self.logger.warning(f"{self.device.ip} - Unsuported device type.")
            return False
        
        except Exception as e:
            self.logger.error(f"{self.device.ip} - Exceptation {e}")
            return False

        self.logger.debug(f"{self.device.ip} - Filtering the configuration file.")
        pars_output = self.device.config_filternig(stdout)

        return pars_output