#!/usr/bin/env python3

import argparse
import base64
import os
import re
import requests
import subprocess


def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Repo name of the package to update", required=True)
    command_args = parser.parse_args()

    rootdir = os.getcwd()
    fullpath = os.path.join(rootdir, command_args.repo)

    with open(os.path.join(fullpath, "conanfile.py"), "r", newline="") as conan_file:
        conan_file_content = conan_file.read()

        packages = list()
        package_strings = re.findall('requires\("(.*?)/(.*?)#(.*?)"', conan_file_content)

        for package_string in package_strings:
            package = {
                "name": package_string[0],
                "version": package_string[1],
                "sha": package_string[2],
            }
            packages.append(package)

        base_gitlab_url = "https://api.github.com/repos/ssrobins"

        for package in packages:
            commit = requests.get(
                f"{base_gitlab_url}/conan-{package['name']}/commits/HEAD")
            commit.raise_for_status()
            package["latest_sha"] = commit.json()["sha"]
        
            conanfile = requests.get(
                f"{base_gitlab_url}/conan-{package['name']}/contents/conanfile.py").json()
            content_list = base64.b64decode(conanfile["content"]).decode("utf-8").splitlines()

            for line in content_list:
                if "version" in line:
                    latest_version = line.split("=")[1].strip().replace('"', '')
                    package["latest_version"] = latest_version
                    break
            
            old_package = f"{package['name']}/{package['version']}#{package['sha']}"
            new_package = f"{package['name']}/{package['latest_version']}#{package['latest_sha']}"
            
            if old_package != new_package and old_package in conan_file_content:
                conan_file_content = conan_file_content.replace(old_package, new_package)
                
                print("Replace:")
                print(f"  {old_package}")
                print("With:")
                print(f"  {new_package}")
                print(f"https://github.com/ssrobins/conan-{package['name']}/compare/{package['sha']}...{package['latest_sha']}")
                print()

    with open(os.path.join(fullpath, "conanfile.py"), "w", newline="") as conan_file:
        conan_file.write(conan_file_content)
    

if __name__ == "__main__":
    main()
