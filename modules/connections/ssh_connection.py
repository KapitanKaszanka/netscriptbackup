import logging
from modules.connections.dev_connection import Dev_Connection
from netmiko import (
    ConnectHandler,
    NetmikoBaseException,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)


class SSH_Connection(Dev_Connection):
    """An object responsible for SSH connections and their validation."""


    def __init__(self, device) -> "Dev_Connection":
        self.logger = logging.getLogger(
            "backup_app.connections.SSH_Connection"
            )
        self.connection_parametrs = {
            "host": self.device.ip,
            "username": self.device.username,
            "port": self.device.port,
            "device_type": self.device.vendor,
            "password": self.device.password,
            "secret": self.device.secret,
            "key_file": self.device.key_file,
            "passphrase": self.device.passphrase
        }


    def _set_privilege(self, _connection: object) -> None:
        self.logger.debug(
            f"{self.device.ip} - Check mode."
            )
        if not _connection.check_enable_mode():
            self.logger.debug(
                f"{self.device.ip} - Change mode."
                )
            _connection.enable(cmd=self.device.mode_cmd)


    def _send_commands(self, _connection, command_lst) -> object:
        self.logger.debug(f"{self.device.ip} - Sending commands.")
        output = []
        for command in command_lst:
            stdout = _connection.send_command(command_string=command,
                                              read_timeout=60)
            output.append(stdout)
        return output


    def _get_conection_and_send(self, command_lst):

        if not self._check_ping_response():
            return False
        try:
            self.logger.info(
                f"{self.device.ip} - Trying download configuration "
                "from the device."
                )
            if self.device.key_file == None:
                self.logger.debug(
                    f"{self.device.ip} - Attempting connect with password."
                    )
                with ConnectHandler(**self.connection_parametrs,
                                    ssh_strict=True,
                                    system_host_keys=True
                                    ) as _connection:
                    self.logger.debug(
                        f"{self.device.ip} - Connection created."
                        )
                    self._set_privilege(_connection)
                    stdout = self._send_commands(_connection,
                                                  command_lst)
                self.logger.debug(
                    f"{self.device.ip} - Connection completend sucessfully."
                    )
                return stdout
            
            else:
                self.logger.debug(
                    f"{self.device.ip} - Connecting with public key."
                    )
                with ConnectHandler(**self.connection_parametrs,
                                    use_keys=True,
                                    ssh_strict=True,
                                    system_host_keys=True
                                    ) as _connection:
                    self.logger.debug(
                        f"{self.device.ip} - Connection created."
                        )
                    self._set_privilege(_connection)
                    stdout = self._send_commands(_connection,
                                                 command_lst)

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

        except NetmikoBaseException as e:
            self.logger.warning(f"{self.device.ip} - Can't connect.")
            self.logger.warning(f"{self.device.ip} - Error {e}")
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