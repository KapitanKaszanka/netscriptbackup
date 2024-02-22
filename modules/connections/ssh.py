#!/usr/bin/env python3.10

import logging
from modules.connections.dev_connection import Dev_Connection
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)


class SSH_Connection(Dev_Connection):
    """
    An object responsible for SSH connections and their validation.
    """


    def __init__(self, device: object) -> "Dev_Connection":
        """
        A class for SSH connections. Connects via netmiko to the device. 
        Sends commands and returns output.

        :param connection_parametrs: all the data you need to connect.
        """
        super().__init__(device)
        self.logger = logging.getLogger(
            f"backup_app.connections.SSH_Connection:{self.device.ip}"
            )
        self.connection_parametrs = {
            "host": self.device.ip,
            "username": self.device.username,
            "port": self.device.port,
            "device_type": self.device.device_type,
            "password": self.device.password,
            "secret": self.device.mode_password,
            "key_file": self.device.key_file,
            "passphrase": self.device.passphrase
        }


    def _set_privilege(self, _connection: object) -> None:
        """
        This function change privilge level if device support it.

        :param _connection: netmiko connection object.
        """
        self.logger.debug("Check mode.")
        if not _connection.check_enable_mode():
            self.logger.debug("Change mode.")
            _connection.enable(cmd=self.device.mode_cmd)


    def _send_command(self, _connection: object, command: str) -> object:
        """
        This function send one command to device.

        :param _connection: netmiko connection object.
        :param command_lst: command to send.
        """
        self.logger.debug("Sending commands.")
        output = _connection.send_command(
            command_string=command,
            read_timeout=60
            )
        return output


    def _send_commands(
            self,
            _connection: object,
            command_lst: list
            ) -> object:
        """
        This function send multi commands to device.

        :param _connection: netmiko connection object.
        :param command_lst: list of commands to send.
        """
        self.logger.debug("Sending commands.")
        output = []
        for command in command_lst:
            stdout = _connection.send_command(
                command_string=command,
                read_timeout=60
                )
            output.append(stdout)
        return output


    def _send(
            self,
            _connection: object,
            commands: list | str
            ) -> object | bool:
        """
        The function decide how send commands.

        :param _connection: netmiko connection object.
        :param command_lst: list of commands to send.
        """
        if isinstance(commands, list):
            output = self._send_commands(_connection, commands)
            return output
        elif isinstance(commands, str):
            output = self._send_command(_connection, commands)
            return output
        else:
            self.logger.warning("Can't send command.")
            return False


    def _get_conection_and_send(self, commands: str | list) -> object:
        """
        The function connects to the device and calls functions 
        to set the permission level and send commands

        :param commands: commands list or string,
        :return: interable netmiko object. 
        """

        if not self._check_ping_response():
            return False
        try:
            self.logger.info("Trying download configuration from the device.")
            if self.device.key_file == None:
                self.logger.debug("Attempting connect with password.")
                with ConnectHandler(
                    **self.connection_parametrs,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as _connection:
                    self.logger.debug("Connection created.")
                    self._set_privilege(_connection)
                    output = self._send(_connection, commands)

                self.logger.debug("Connection completend sucessfully.")
                if self.device.ip == "r3.home":
                    print(output)
                return output

            else:
                self.logger.debug("Connecting with public key.")
                with ConnectHandler(
                    **self.connection_parametrs,
                    use_keys=True,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as _connection:
                    self.logger.debug("Connection created.")
                    self._set_privilege(_connection)
                    stdout = self._send(_connection, commands)

                self.logger.debug("Connection completend sucessfully.")
                return stdout

        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.error("Can't connect. Device "
                                  "not found in known_host file.")
                return False

            else:
                self.logger.error(f"Can't connect. {e}")
                return False

        except NetmikoBaseException as e:
            self.logger.warning("Can't connect.")
            self.logger.warning(f"Error {e}")
            return False

        except NetmikoAuthenticationException as e:
            self.logger.warning("Can't connect.")
            self.logger.warning(f"Error {e}")
            return False

        except ValueError as e:
            if "enable mode" in str(e):
                self.logger.warning("Failed enter enable mode. "
                                    "Check password.")
                return False
            
            else:
                self.logger.warning("Unsuported device type.")
                return False
        
        except Exception as e:
            self.logger.error(f"{self.device.ip} - Exceptation {e}")
            return False


    def get_config(self) -> bool | str:
        """
        The function retrieves the necessary commands 
        and returns the device configuration.

        :return: filtered device configuration.
        """
        self.logger.debug("Filtering the configuration file.")

        command = self.device.command_show_config()
        output = self._get_conection_and_send(command)

        if not output:
            return False

        pars_output = self.device.config_filternig(output)
        return pars_output