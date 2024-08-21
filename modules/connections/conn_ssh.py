#!/usr/bin/env python3.10
"""
ssh connection object with all necesery parametrs and funcitons.
"""

import logging
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)


class ConnSSH:
    """
    an object responsible for SSH connections and their validation.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"netscriptbackup.connections.ConnSSH")

    def _set_privilege(self) -> None:
        """
        this function change privilge level if device support it.

        :param _connection: netmiko connection object.
        """
        self.logger.debug(f"{self.ip}:Check privilege mode.")
        if not self._connection.check_enable_mode():
            self.logger.debug(f"{self.ip}:Change privilege mode.")
            self._connection.enable(cmd=self.mode_cmd)

    def _send_command(self, command: str) -> object:
        """
        this function send command to device.

        :param _connection: netmiko connection object.
        :param command_lst: command to send.
        """
        self.logger.debug(f"{self.ip}:Sending command.")
        output: str = self._connection.send_command(
            command_string=command, read_timeout=60
        )
        return output

    def _send(self, commands: str) -> str:
        """
        the function decide how send commands.

        :param _connection: netmiko connection object.
        :param command_lst: str or list of command(s) to send.
        """
        output = self._send_command(commands)
        return output

    def _get_conection_and_send(self, command: str) -> str | bool:
        """
        the function connects to the device. If necessary, determines
        the appropriate level of permissions. It then executes functions
        that send commands.

        :param commands: commands list or string,
        :return: interable netmiko object.
        """
        conn_parametrs = {
            "host": self.ip,
            "username": self.username,
            "port": self.port,
            "device_type": self.device_type,
            "password": self.password,
            "secret": self.mode_password,
            "key_file": self.key_file,
            "passphrase": self.passphrase,
        }
        try:
            self.logger.info(
                f"{self.ip}:Trying download " "configuration from the device."
            )
            if conn_parametrs["key_file"] == None:
                self.logger.debug(
                    f"{self.ip}:Attempting " "connect with password."
                )
                with ConnectHandler(
                    **conn_parametrs, ssh_strict=True, system_host_keys=True
                ) as self._connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege()
                    output = self._send(command)
            else:
                self.logger.debug(f"{self.ip}:Connecting with public key.")
                with ConnectHandler(
                    **conn_parametrs,
                    use_keys=True,
                    ssh_strict=True,
                    system_host_keys=True,
                ) as self._connection:
                    self.logger.debug(f"{self.ip}:Connection created.")
                    self._set_privilege()
                    output = self._send(command)
            self.logger.debug(f"{self.ip}:Connection completend sucessfully.")
            return output
        except NetmikoTimeoutException as e:
            if "known_hosts" in str(e):
                self.logger.warning(
                    f"{self.ip}:Can't connect. "
                    "Device not found in known_host file."
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
                    f"{self.ip}:Failed enter enable mode. " "Check password."
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
        the function retrieves the necessary commands
        and returns the device configuration.

        :return: filtered device configuration.
        """
        self.logger.debug(f"{self.ip}:Get command.")
        command = self.get_command_show_config()
        self.logger.debug(f"{self.ip}:Set connection parametrs.")
        output: str = self._get_conection_and_send(command)
        if not output:
            return None
        pars_output = self.config_filternig(output)
        return pars_output


if __name__ == "__main__":
    pass
