#!/usr/bin/env python3

"""Tool to run commands across multiple repos"""

import argparse
import os
import subprocess

def main():
    """
    Set the various scopes of repo dirs and then run the user's command
    """
    apps = [
        "games",
        "sdl2-example",
        "sfml-examples",
        "stackblox"
    ]

    conan_singleplat = [
        "conan-recipes/recipes/android_sdl",
        "conan-recipes/recipes/cmake_utils"
    ]

    conan_multiplat = [
        "conan-recipes/recipes/box2d",
        "conan-recipes/recipes/bzip2",
        "conan-recipes/recipes/freetype",
        "conan-recipes/recipes/glew",
        "conan-recipes/recipes/gtest",
        "conan-recipes/recipes/libpng",
        "conan-recipes/recipes/ogg",
        "conan-recipes/recipes/sdl",
        "conan-recipes/recipes/sdl_image",
        "conan-recipes/recipes/sdl_mixer",
        "conan-recipes/recipes/sdl_ttf",
        "conan-recipes/recipes/sfml",
        "conan-recipes/recipes/ssrobins_engine",
        "conan-recipes/recipes/vorbis",
        "conan-recipes/recipes/zlib"
    ]

    conan = conan_singleplat + conan_multiplat

    all_dirs = apps + conan

    scope = {
        "all": all_dirs,
        "apps": apps,
        "conan": conan,
        "conan-singleplat": conan_singleplat,
        "conan-multiplat": conan_multiplat
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",
        help="Command you want to run in each dir", required=True)
    parser.add_argument("--scope",
        choices=list(scope.keys()),
        help="Define the group of dirs where the command should run", required=True)
    command_args = parser.parse_args()

    repo_dirs = scope[command_args.scope]

    rootdir = os.getcwd()
    cmd = command_args.cmd
    for repo_dir in repo_dirs:
        fullpath = os.path.join(rootdir, repo_dir)
        print(f"######## Running '{cmd}' in {dir}", flush=True)
        subprocess.run(cmd, cwd=fullpath, shell=True, check=True)
        print("###################################")
        print()


if __name__ == "__main__":
    main()
