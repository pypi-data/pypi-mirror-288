#!/usr/bin/env python3

import os
from pathlib import PurePath
import sys


def print_exec_cmd(cmd: str):
    print(cmd)
    os.system(cmd)


def is_direct_exec():
    script_file_path_obj = PurePath(__file__)
    return script_file_path_obj.name in sys.argv[0]


def get_package_dir_arg_or_relative_default():

    # Check if the script is directly called (file name is in argv) -> otherwise assume installed through console_scripts
    if (is_direct_exec()):
        script_dir: str = os.path.dirname(os.path.realpath(__file__))
        package_dir: str = os.path.dirname(os.path.realpath(script_dir))
        # print(f"Script dir: {script_dir}")
        return package_dir

    if (len(sys.argv) > 1):
        return os.path.realpath(sys.argv[1])

    return None


def main():
    package_dir: str = get_package_dir_arg_or_relative_default()
    print(f"Package dir: {package_dir}")

    print_exec_cmd(f'pip3 install -e {package_dir}')


if __name__ == '__main__':
    sys.exit(main())
