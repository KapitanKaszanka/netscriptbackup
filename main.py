#!/usr/bin/env python3

from backup_tool import backup_execute
import time

def main():
    
    start = time.time()
    backup_execute()
    stop = time.time()
    
    print(f"Script execute in: {round(stop - start, 2)}")

if __name__ == "__main__":
    main()