#!/usr/bin/env python3.10
"""
SSH connection object with all necesery parametrs and funcitons.
"""

from modules.connections.conn import Conn
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)


class ConnSSH(Conn):
    """
    An object responsible for SSH connections and their validation.
    """
    def _set_privilege(self, _connection: object) -> None:
        """
        This function change privilge level if device support it.

        :param _connection: netmiko connection object.
        """

        self.logger.debug(f"{self.ip}:Check mode.")
        if not _connection.check_enable_mode():
            self.logger.debug(f"{self.ip}:Change mode.")
            _connection.enable(cmd=self.mode_cmd)


    def _send_command(self, _connection: object, command: str) -> object:
        """
        This function send command to device.

        :param _connection: netmiko connection object.
        :param command_lst: command to send.
        """
        self.logger.debug(f"{self.ip}:Sending command.")
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
        The function sends a list of commands from the device.

        :param _connection: netmiko connection object.
        :param command_lst: list of commands to send.
        """
        self.logger.debug(f"{self.ip}:Sending commands.")
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
        :param command_lst: str or list of command(s) to send.
        """
        if isinstance(commands, list):
            output = self._send_commands(_connection, commands)
            return output
        elif isinstance(commands, str):
            output = self._send_command(_connection, commands)
            return output
        else:
            self.logger.warning(f"{self.ip}:Can't send command.")
            return False

    def _get_conection_and_send(
        self,
        commands: str | list
        ) -> str | bool:
        """
        The function connects to the device. If necessary, determines 
        the appropriate level of permissions. It then executes functions 
        that send commands.

        :param commands: commands list or string,
        :return: interable netmiko object. 
        """
        if not self.check_ping_response():
            return False
        conn_parametrs = {
            "host": self.ip,
            "username": self.username,
            "port": self.port,
            "device_type": self.device_type,
            "password": self.password,
            "secret": self.mode_password,
            "key_file": self.key_file,
            "passphrase": self.passphrase
        }
        try:
            self.logger.info(
                f"{self.ip}:Trying download "
                "configuration from the device."
                )
            if conn_parametrs["key_file"] == None:
                self.logger.debug(
                    f"{self.ip}:Attempting "
                    "connect with password."
                    )
                with ConnectHandler(
                    **conn_parametrs,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as _connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege(_connection)
                    output = self._send(_connection, commands)
            else:
                self.logger.debug(f"{self.ip}:Connecting with public key.")
                with ConnectHandler(
                    **conn_parametrs,
                    use_keys=True,
                    ssh_strict=True,
                    system_host_keys=True
                    ) as _connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege(_connection)
                    output = self._send(_connection, commands)
            self.logger.debug(
                f"{self.ip}:Connection completend sucessfully."
                )
            return output
        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.warning(
                    f"{self.ip}:Can't connect. Device "
                    "not found in known_host file."
                    )
                return False
            else:
                self.logger.warning(f"{self.ip}:Can't connect. {e}")
                return False
        except NetmikoBaseException as e:
            self.logger.warning(f"{self.ip}:Can't connect.")
            self.logger.warning(f"{self.ip}:Error {e}")
            return False
        except NetmikoAuthenticationException as e:
            self.logger.warning(f"{self.ip}:Can't connect.")
            self.logger.warning(f"{self.ip}:Error {e}")
            return False
        except ValueError as e:
            if "enable mode" in str(e):
                self.logger.warning(
                    f"{self.ip}:Failed enter enable mode. "
                    "Check password."
                    )
                return False
            else:
                self.logger.warning(f"{self.ip}:Unsuported device type.")
                return False
        except Exception as e:
            self.logger.error(f"{self.ip}:Exceptation - {e}")
            return False

    def get_config(self) -> str:
        """
        The function retrieves the necessary commands 
        and returns the device configuration.

        :return: filtered device configuration.
        """
        self.logger.debug(f"{self.ip}:Get command.")
        command = self.get_command_show_config()
        self.logger.debug(f"{self.ip}:Set connection parametrs.")
        output = self._get_conection_and_send(command)
        if not output:
            return None
        pars_output = self.config_filternig(output)
        return pars_output


if __name__ == "__main__":
    pass
