#!/usr/bin/env python3

import logging
from subprocess import (
    Popen as subproc_Popen,
    check_output as subproc_check_outpu,
    CalledProcessError as subproc_CalledProcessError,
    DEVNULL as subproc_DEVNULL
)
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)



class SSH_Connection():
    """An object responsible for SSH connections and their validation."""


    def __init__(self, device) -> None:
        self.logger = logging.getLogger(
            "backup_app.connections.SSH_Connection"
            )
        self.device = device


    def _check_ping_response(self):
        try:
            self.logger.debug(
                f"{self.device.ip} - Checking if the host is responding"
                )
            ping = ["/usr/bin/ping", "-W", "1", "-c", "4", self.device.ip]
            subproc_check_outpu(ping, stderr=subproc_DEVNULL)
            self.logger.debug(f"{self.device.ip} - The host responds")
            return True

        except subproc_CalledProcessError as e:
            self.logger.warning(
                f"{self.device.ip} - Host isn't responding. Skip."
                )
            return False

        except Exception as e:
            self.logger.error(f"{self.device.ip} - Exception: {e}. Skip")
            return False


    def _get_conection_and_send(self, command_lst):
        
        if not self._check_ping_response():
            return False

        connection_parametrs = {
            "host": self.device.ip,
            "username": self.device.username,
            "port": self.device.port,
            "device_type": self.device.device_type,
            "password": self.device.password,
            "secret": self.device.mode_password,
            "key_file": self.device.key_file,
            "passphrase": self.device.passphrase
        }
        other_parametrs = {
            "cmd": self.device.mode_cmd
        }

        self.logger.debug(
            f"{self.device.ip} - Downloading the necessary commands."
            )

        try:
            self.logger.info(
                f"{self.device.ip} - Trying download configuration "
                "from the device."
                )
            self.logger.debug(
                f"{self.device.ip} - Attempting to create an SSH connection."
                )
            if connection_parametrs["key_file"] == None:
                self.logger.debug(
                    f"{self.device.ip} - Connecting with password."
                    )
                with ConnectHandler(
                    **connection_parametrs,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as connection:
                    self.logger.debug(
                        f"{self.device.ip} - Connection created."
                        )

                    self.logger.debug(
                        f"{self.device.ip} - Check mode."
                        )
                    if not connection.check_enable_mode():
                        self.logger.debug(
                            f"{self.device.ip} - Change mode."
                            )
                        connection.enable(
                            cmd=other_parametrs["cmd"]
                            )

                    self.logger.debug(
                        f"{self.device.ip} - Sending commands."
                        )
                    for command in command_lst:
                        stdout = connection.send_command(
                            command_string=command,
                            read_timeout=60
                            )

                self.logger.debug(
                    f"{self.device.ip} - Connection completend sucessfully."
                    )
                return stdout

            else:
                self.logger.debug(
                    f"{self.device.ip} - Connecting with public key."
                    )
                with ConnectHandler(
                    **connection_parametrs,
                    use_keys=True,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as connection:
                    self.logger.debug(
                        f"{self.device.ip} - Connection created."
                        )

                    self.logger.debug(
                        f"{self.device.ip} - Check mode."
                        )
                    if not connection.check_enable_mode():
                        self.logger.debug(
                            f"{self.device.ip} - Change mode."
                            )
                        connection.enable(
                            cmd=other_parametrs["cmd"]
                            )

                    self.logger.debug(
                        f"{self.device.ip} - Sending commands."
                        )

                    for command in command_lst:
                        stdout = connection.send_command(
                            command_string=command,
                            read_timeout=60
                            )


                self.logger.debug(
                    f"{self.device.ip} - Connection completend sucessfully."
                    )
                return stdout

        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.error(
                    f"{self.device.ip} - Can't connect. Device "
                    "not found in known_host file."
                    )
                return False
            
            else:
                self.logger.error(
                    f"{self.device.ip} - Can't connect. {e}"
                    )
                return False
            
        except NetmikoAuthenticationException as e:
            self.logger.warning(f"{self.device.ip} - Can't connect.")
            self.logger.warning(f"{self.device.ip} - Error {e}")
            return False

        except ValueError as e:
            if "enable mode" in str(e):
                self.logger.warning(
                f"{self.device.ip} - Failed enter enable mode. "
                "Check password."
                )
                return False
            
            else:
                self.logger.warning(
                    f"{self.device.ip} - Unsuported device type."
                    )
                return False
        
        except Exception as e:
            self.logger.error(f"{self.device.ip} - Exceptation {e}")
            return False



    def get_config(self):
        self.logger.debug(
            f"{self.device.ip} - Filtering the configuration file."
            )
        command = self.device.command_show_config()
        commands_list = [command]
        stdout = self._get_conection_and_send(commands_list)
        pars_output = self.device.config_filternig(stdout)

        return pars_output