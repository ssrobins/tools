#!/usr/bin/env python3

"""Tool to time a command"""

import argparse
import datetime
import subprocess
import time

def main():
    """
    Time running the specified command in the specified directory
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",
        help="Command you want to time", required=True)
    parser.add_argument("--dir",
        help="Current working directory for command", required=True)
    command_args = parser.parse_args()

    start_time = time.time()
    subprocess.run(command_args.cmd, cwd=command_args.dir, shell=True, check=True)
    end_time = time.time()

    print(f"duration of the command '{command_args.cmd}' in hours:minutes:seconds")
    print(str(datetime.timedelta(seconds=end_time - start_time)))


if __name__ == "__main__":
    main()
