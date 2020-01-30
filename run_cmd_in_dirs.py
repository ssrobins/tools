#!/usr/bin/env python3

import argparse
import json
import os
import subprocess


def main():
    apps = [
        "games",
        "sdl2-example",
        "sfml-examples",
        "stackblox"
    ]

    conan_singleplat = [
        "conan-android_sdl2",
        "conan-cmake_utils"
    ]

    conan_multiplat = [
        "conan-box2d",
        "conan-bzip2",
        "conan-freetype",
        "conan-glew",
        "conan-gtest",
        "conan-libpng",
        "conan-sdl2",
        "conan-sdl2_image",
        "conan-sdl2_mixer",
        "conan-sdl2_ttf",
        "conan-sfml",
        "conan-ssrobins_engine",
        "conan-zlib"
    ]

    conan = conan_singleplat + conan_multiplat

    docker = [
        "docker-android-build",
        "docker-linux-build",
        "docker-windows-build"
    ]

    all = apps + conan + docker

    scope = {
        "all": all,
        "apps": apps,
        "conan": conan,
        "conan-singleplat": conan_singleplat,
        "conan-multiplat": conan_multiplat,
        "docker": docker
    }
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",
        help="Command you want to run in each dir", required=True)
    parser.add_argument("--scope",
        choices=list(scope.keys()),
        help="Define the group of dirs where the command should run", required=True)
    command_args = parser.parse_args() 

    dirs = scope[command_args.scope]

    rootdir = os.getcwd()
    cmd = command_args.cmd
    for dir in dirs:
        fullpath = os.path.join(rootdir, dir)
        print(f"######## Running '{cmd}' in {dir}")
        subprocess.run(cmd, cwd=fullpath, shell=True, check=True)
        print("###################################")
        print()


if __name__ == "__main__":
    main()
