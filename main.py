#!/usr/bin/env python3.10

from modules.backup_app import backup_execute


def main():

    backup = backup_execute()
    if backup:
        print("Script execute..")

if __name__ == "__main__":
    main()