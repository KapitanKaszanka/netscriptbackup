#!/usr/bin/env python3.10
"""
Implementing multithreading to optimize code execution
"""

from os import cpu_count
from concurrent.futures import (
    ThreadPoolExecutor, 
    ProcessPoolExecutor, 
    wait
    )


class Multithreading:

    def __init__(self) -> None:
        self.cpus = cpu_count() - 1

    def _split_list_into_smaller_lists(self, lst: list) -> None:
        """
        This function splits the main list and many smaller 
        ones depending on the number of cpu -1.

        :param lst: list to split
        :return: None
        """
        self.split_lst = []
        for _ in range(self.cpus):
            self.split_lst.append([])
        for index, element in enumerate(lst):
            self.split_lst[index % self.cpus].append(element)

    def _threading(self, func, lst: list) -> None:
        """
        The function divides processes into threads.

        :param func: function to perform
        :param lst: list of variables to pass
        :return: None
        """
        with ThreadPoolExecutor(max_workers=self.cpus * 4) as executor:
            wait([executor.submit(func, i) for i in lst])

    def _multi_procesing(self, func) -> None:
        """
        The function starts separate processes on 
        each CPU -1 the device has. 
        Each process is supposed to start the _threading process.

        :param func: function to perform
        :return: None
        """
        with ProcessPoolExecutor(self.cpus) as exe:
            wait([exe.submit(
                self._threading, 
                func, 
                i
                ) for i in self.split_lst])

    def execute_multitreading(self, func, lst: list) -> None:
        """
        The function begins the process of splitting
        the received function into multiple threads and processes.
        
        :param func: function to perform
        :param lst: List of objects on which 
                    the sent function is to be executed
        :return: None
        """
        self._split_list_into_smaller_lists(lst)
        self._multi_procesing(func)
