#!/usr/bin/env python3

import logging
from subprocess import (
    Popen as subproc_Popen,
    check_output as subproc_check_outpu,
    CalledProcessError as subproc_CalledProcessError,
    DEVNULL as subproc_DEVNULL
)



class Dev_Connection:


    def __init__(self, device) -> None:
        self.logger = logging.getLogger(
            "backup_app.connections.Dev_connection"
            )
        self.device = device


    def _check_ping_response(self) -> bool:
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


