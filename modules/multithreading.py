#!/usr/bin/env python3.10
"""
implementing multithreading to optimize code execution
"""

from os import cpu_count
from concurrent.futures import ThreadPoolExecutor, wait


class Multithreading:

    def __init__(self, _thred_num: int = None) -> None:
        """
        an object that is responsible for dividing a task
        into many threads.

        :param threading: bool split the task into multiple threads,
        :param _thred_num: int maximum number of threads.
                          defualt = cpu threds * 2
        :return: None
        """
        if _thred_num is None:
            self._thred_num = cpu_count() * 2
        else:
            self._thred_num = _thred_num

    def _threading(self) -> None:
        """
        the function splits the task into multiple threads

        :return: None
        """
        with ThreadPoolExecutor(max_workers=self._thred_num) as executor:
            wait([executor.submit(self.func, i) for i in self.lst])

    def execute(self, func, lst: list) -> None:
        """
        the function begins the process of splitting
        the received function into multiple threads.

        :param func: function to perform
        :param lst: List of objects on which
                    the sent function is to be executed.
        :return: None
        """
        self.func = func
        self.lst: list = lst
        self._threading()


if __name__ == "__main__":
    pass
