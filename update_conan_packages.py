#!/usr/bin/env python3

"""Tool to update Conan dependencies to the latest"""

import argparse
import json
import os
import re
import subprocess


def main():
    """
    Read Conan dependencies, look for updates, and update the conanfile.py with updates
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Repo name of the package to update", required=True)
    command_args = parser.parse_args()

    fullpath = os.path.join(os.getcwd(), command_args.repo)

    with open(os.path.join(fullpath, "conanfile.py"),
        "r", encoding="utf-8", newline="") as conan_file:
        conan_file_content = conan_file.read()

        packages = []
        package_strings = re.findall(r'requires\("(.*?)/(.*?)@', conan_file_content)

        for package_string in package_strings:
            package = {
                "name": package_string[0],
                "version": package_string[1],
            }
            packages.append(package)

        for package in packages:
            conan_inspect_output = subprocess.run("conan inspect . --format json",
                cwd=f"conan-recipes/recipes/{package['name']}",
                shell=True, check=True, stdout=subprocess.PIPE)
            conan_inspect_json = json.loads(conan_inspect_output.stdout.decode("utf-8"))
            package["latest_version"] = conan_inspect_json["version"]

            old_package = f"{package['name']}/{package['version']}"
            new_package = f"{package['name']}/{package['latest_version']}"

            if old_package != new_package and old_package in conan_file_content:
                conan_file_content = conan_file_content.replace(old_package, new_package)

                print("Replace:")
                print(f"  {old_package}")
                print("With:")
                print(f"  {new_package}")
                print()

    with open(os.path.join(fullpath, "conanfile.py"),
        "w", encoding="utf-8", newline="") as conan_file:
        conan_file.write(conan_file_content)


if __name__ == "__main__":
    main()
