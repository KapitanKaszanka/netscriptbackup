#!/usr/bin/env python3.10

from modules.application import backup_execute
from modules.other.my_decorators import profiling, mesure_time

@mesure_time
@profiling
def main():

    backup = backup_execute()
    if backup:
        print("Script execute..")

if __name__ == "__main__":
    main()