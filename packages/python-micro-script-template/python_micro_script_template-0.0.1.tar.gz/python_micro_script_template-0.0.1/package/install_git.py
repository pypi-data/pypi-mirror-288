#!/usr/bin/env python3

import os
from pathlib import PurePath
import re
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


def extract_setup_url_value(setup_py_path: str):
    read_file: str | None = None
    with open(setup_py_path, "r") as file_reader:
        read_file = file_reader.read()

    if (not read_file):
        exit()

    match_url_regex = re.compile('url\s*=\s*"(.+)"')

    matched_url_field = re.search(match_url_regex, read_file)
    # print(matched_url_field)
    # print(matched_url_field.group(0))
    # print(matched_url_field.group(1))

    matched_url = matched_url_field.group(1)
    return matched_url


def main():

    package_dir: str = get_package_dir_arg_or_relative_default()
    print(f"Package dir: {package_dir}")

    setup_py_path = os.path.realpath(os.path.join(package_dir, 'setup.py'))

    selected_protocol = 'ssh'
    if (len(sys.argv) > 1):
        selected_protocol = sys.argv[1]

    print(f"Selected protocol: {selected_protocol}")

    matched_url = extract_setup_url_value(setup_py_path)

    if (not matched_url.startswith('http')):
        raise Exception("Error only http prefixed urls are supported")

    after_protocol_url = re.sub(r'^(http://|https://)', '', matched_url)

    domain_url_parts = after_protocol_url.split('/')
    domain = domain_url_parts[0]
    after_domain_parts = domain_url_parts[1:]
    after_domain_parts_joined = '/'.join(after_domain_parts)

    if (selected_protocol in ['http', 'https']):
        http_target = f"git+https://{domain}/{after_domain_parts_joined}.git"
        print_exec_cmd(f'pip3 install "{http_target}"')
        exit()

    ssh_target = f"git+ssh://git@{domain}/{after_domain_parts_joined}.git"

    print_exec_cmd(f'pip3 install "{ssh_target}"')

    # pip3 install git+ssh://git@github.com/markuspeitl/python_micro_script_template.git
    # pip3 install git+https://github.com/markuspeitl/python_micro_script_template.git


if __name__ == '__main__':
    sys.exit(main())
