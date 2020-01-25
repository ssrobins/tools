import argparse
import base64
import os
import requests
import subprocess


def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", help="Repo name of the package to update", required=True)
    command_args = parser.parse_args()

    repo = command_args.repo
    rootdir = os.getcwd()
    fullpath = os.path.join(rootdir, repo)

    # Run the command once to update so the next run doesn'tell
    # have warning messages that mess up the string parsing
    subprocess.run(
        "conan info . --update",
        cwd=fullpath, capture_output=True, shell=True, check=True)
    
    conan_info_raw = subprocess.run(
        "conan info . --only id",
        cwd=fullpath, capture_output=True, shell=True, check=True).stdout.splitlines()

    packages = list()

    for index in range(0, len(conan_info_raw), 2):
        if "conanfile.py" not in conan_info_raw[index].decode("UTF-8"):
            package = {
                "name": conan_info_raw[index].decode("UTF-8").split("/")[0],
                "version": conan_info_raw[index].decode("UTF-8").split("/")[1],
            }
            packages.append(package)

    with open(os.path.join(fullpath, "conanfile.py"), "r", newline="") as conan_file:
        conan_file_content = conan_file.read()
        
        base_gitlab_url = "https://gitlab.com/api/v4/projects"

        for package in packages:
            conan_info_raw = subprocess.run(
                f"conan info . --update --package-filter {package['name']}/{package['version']}",
                cwd=fullpath, capture_output=True, shell=True, check=True).stdout.decode("utf-8").splitlines()
            for line in conan_info_raw:
                if "Revision" in line:
                    package["sha"] = line.split(":")[1].strip()
                    break
        
            commit = requests.get(
                f"{base_gitlab_url}/ssrobins%2Fconan-{package['name']}/repository/commits/HEAD").json()
            package["latest_sha"] = commit["id"]
        
            conanfile = requests.get(
                f"{base_gitlab_url}/ssrobins%2Fconan-{package['name']}/repository/files/conanfile.py?ref=HEAD").json()
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
                print()

    with open(os.path.join(fullpath, "conanfile.py"), "w", newline="") as conan_file:
        conan_file.write(conan_file_content)
    

if __name__ == "__main__":
    main()