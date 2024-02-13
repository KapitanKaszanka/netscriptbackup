#!/usr/bin/env python3

<<<<<<< HEAD
from backaupnet_tool import backup_execute
=======
from backupnet_tool import backup_execute
>>>>>>> bc38824 (Restore git)

import os
import psutil


# inner psutil function
def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


# decorator function
def profile(func):
    def wrapper(*args, **kwargs):

        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
<<<<<<< HEAD
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))
=======
        print()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))
        print()
>>>>>>> bc38824 (Restore git)

        return result
    return wrapper



@profile
def main():
    
    backup_execute()

if __name__ == "__main__":
    main()