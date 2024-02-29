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

    def __init__(
            self, 
            process: bool = True,
            threading: bool = True,
            proc_num: int = None,
            thred_num: int = None
            ) -> None:
        """
        An object that is responsible for dividing a task
        into many threads and/or processes.

        If process: True && threading: False -> multiprocessing only.
        If process: True && threading: True -> multiprocessing && threading.
        If process: False && threading: True -> threading only.
        If process: False && threading: False -> error.

        :param process: bool divide the task into multiple processes,
        :param threading: bool split the task into multiple threads,
        :param proc_num: int maximum number of processes.
                         defualt = cpu threds / 2
        :param thred_num: int maximum number of threads.
                          defualt = cpu threds * 2
        :return: None
        """
        if not process and not threading:
            return "ERROR"
        self.process = process,
        self.threading = threading,
        if proc_num is None:
            self.proc_num = int(cpu_count() / 2)
        else:
            self.proc_num = proc_num
        if thred_num is None:
            self.thred_num = cpu_count() * 2
        else:
            self.thred_num = thred_num

    def _splits_list_into_smaller_lists(self) -> None:
        """
        The function splits the main list into many 
        smaller ones depending on the number of 
        processors that will be used.

        :return: None
        """
        self.splited_lst = []
        for _ in range(self.proc_num):
            self.splited_lst.append([])
        for index, element in enumerate(self.lst):
            self.splited_lst[index % self.proc_num].append(element)

    def _threading(self, lst: list) -> None:
        """
        the function splits the task into multiple threads

        :param func: function to perform
        :param lst: list of variables to pass
        :return: None
        """
        with ThreadPoolExecutor(max_workers=self.thred_num) as executor:
            wait([executor.submit(self.func, i) for i in lst])

    def _multi_processing(self, use_threading: bool) -> None:
        """
        The function starts separate processes on 
        each CPU -1 the device has. 
        Each process is supposed to start the _threading process.

        :param use_threading: bool make threading,
        :return: None.
        """
        if use_threading:
            self._splits_list_into_smaller_lists()
            with ProcessPoolExecutor(max_workers=self.proc_num) as exe:
                wait(
                    [exe.submit(self._threading, i) for i in self.splited_lst]
                    )
        else:
            with ProcessPoolExecutor(max_workers=self.proc_num) as exe:
                wait([exe.submit(self.func, i) for i in self.lst])

    def execute(
            self,
            func,
            lst: list,
            ) -> None:
        """
        The function begins the process of splitting
        the received function into multiple processes and threads.
        
        :param func: function to perform
        :param lst: List of objects on which 
                    the sent function is to be executed.
        :return: None
        """
        self.func = func
        self.lst = lst
        if self.process and not self.threading:
            self._multi_processing(False)
        elif self.process and self.threading:
            self._multi_processing(True)
        elif self.threading and not self.process:
            self._threading(self.lst)
