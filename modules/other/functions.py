#!/usr/bin/env python3.10
import logging
from pathlib import Path


logger = logging.getLogger("netscriptbackup.functions")


def save_to_file(
    path: object,
    ip: str,
    name: str,
    data: str
    ) -> bool:
    """
    The function that is responsible for creating and saving 
    data to the file.

    :param path: path to file
    :param ip: device ip used for log and naming purposes,
    :param name: name of device, used for naming purpose,
    :param data: data that will be saved,
    :return: bool done or not.
    """
    try:
        if name == None:
            dir_path = path / f"{ip}"
            file_path = path / f"{ip}" / f"{ip}_conf.txt"
        else:
            dir_path = path / f"{name}_{ip}"
            file_path = path / f"{name}_{ip}" / f"{ip}_conf.txt"
        logger.debug(f"{ip}:Check if the folder exist.")
        if not dir_path.is_dir():
            logger.info(
                f"{ip}:The folder doesn't exist "
                "or account doesn't have permissions."
                )
            logger.info(f"{ip}:Creating a folder.")
            dir_path.mkdir()
        try:
            logger.debug(f"{ip}:Opening the file.")
            with open(file_path, "w") as f:
                logger.debug(f"{ip} - Writing config.")
                f.writelines(data)
            return True
        except PermissionError:
            logger.warning(
                f"{ip}:The file cannot be opened. Permissions error."
                )
            return False
    except Exception as e:
        logger.error(f"{ip}:Error: {e}")
        return False


def get_and_valid_path(path: str) -> Path | None:
    """
    The function check if path or file exist.

    :return: Path or None
    """
    valid_path = Path(path)
    if valid_path.exists():
        return valid_path
    else:
        logger.error(f"{path} doesn't exist.")
        return None


if __name__ == "__main__":
    pass