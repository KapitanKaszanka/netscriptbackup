#!/usr/bin/env python3

from backup_tool import backup_execute



def main():

    backup = backup_execute()

    if backup:
        print("Script execute..")


if __name__ == "__main__":
    main()