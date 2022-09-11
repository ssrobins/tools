#!/usr/bin/env python3

"""Tool to update Conan dependencies to the latest"""

import argparse
import os
import re
import subprocess
import requests


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
        package_strings = re.findall(r'requires\("(.*?)/(.*?)#(.*?)"', conan_file_content)

        for package_string in package_strings:
            package = {
                "name": package_string[0],
                "version": package_string[1],
                "sha": package_string[2],
            }
            packages.append(package)

        gitlab_url = "https://api.github.com/repos/ssrobins/conan-recipes"

        commit = requests.get(f"{gitlab_url}/commits/HEAD", timeout=10)
        commit.raise_for_status()
        latest_sha = commit.json()["sha"]

        for package in packages:
            conan_inspect_output = subprocess.run("conan inspect . --raw version",
                cwd=f"conan-recipes/recipes/{package['name']}",
                shell=True, check=True, stdout=subprocess.PIPE)
            package["latest_version"] = conan_inspect_output.stdout.decode("utf-8")

            old_package = f"{package['name']}/{package['version']}#{package['sha']}"
            new_package = f"{package['name']}/{package['latest_version']}#{latest_sha}"

            if old_package != new_package and old_package in conan_file_content:
                conan_file_content = conan_file_content.replace(old_package, new_package)

                print("Replace:")
                print(f"  {old_package}")
                print("With:")
                print(f"  {new_package}")
                print("https://github.com/ssrobins/conan-recipes/compare/"
                      f"{package['sha']}...{latest_sha}")
                print()

    with open(os.path.join(fullpath, "conanfile.py"),
        "w", encoding="utf-8", newline="") as conan_file:
        conan_file.write(conan_file_content)


if __name__ == "__main__":
    main()
