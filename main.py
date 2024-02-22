#!/usr/bin/env python3.10

from modules.backup_app import backup_execute
import time


def main():
    start = time.time()
    backup = backup_execute()

    if backup:
        print("Script execute..")
    end = time.time()

    print(f"Execute time: {(end - start):01}")

if __name__ == "__main__":
    main()