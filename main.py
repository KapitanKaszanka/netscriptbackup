#!/usr/bin/env python3.10

from modules.application import backup_execute
from modules.other.my_decorators import profiling

@profiling
def main():

    backup = backup_execute()
    if backup:
        print("Script execute..")

if __name__ == "__main__":
    print(type(main))
    main()