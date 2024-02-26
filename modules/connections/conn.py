#!/usr/bin/env python3.10

import logging
from subprocess import (
    Popen as subproc_Popen,
    check_output as subproc_check_outpu,
    CalledProcessError as subproc_CalledProcessError,
    DEVNULL as subproc_DEVNULL
)


class Conn:
    """
    Base class for creating connection objects.

    :param device: Device object.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(
            f"netscriptbackup.connections.Conn"
            )

    def _check_ping_response(self) -> bool:
        """
        Sends 4 pings, and check if host is responding.
        Work only for linux.

        :return: False if host is not responding, or domain name is wrong.
        """

        try:
            self.logger.debug(f"{self.ip}:Checking if the host is responding")
            ping = ["/usr/bin/ping", "-W", "1", "-c", "4", self.ip]
            subproc_check_outpu(ping, stderr=subproc_DEVNULL)
            self.logger.debug("The host responds")
            return True
        except subproc_CalledProcessError:
            self.logger.warning(f"{self.ip}:Host isn't responding. Skip.")
            return False
        except Exception as e:
            self.logger.error(f"{self.ip}:Exception: {e}. Skip")
            return False


if __name__ == "__main__":
    pass