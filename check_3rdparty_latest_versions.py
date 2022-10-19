#!/usr/bin/env python3

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
# pylint: disable=R0904

import argparse
import re
import sys
import time
from multiprocessing import Pool
from urllib.request import build_opener, HTTPCookieProcessor, install_opener, Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup



class VersionCheck:
    def __init__(self, debug):
        self.versions = {
            "7Zip":            "22.01",
            "AndroidNDK":      "r25b",
            "AndroidSDKAPI":   "33",
            "AndroidStudio":   "2021.3.1",
            "bzip2":           "1.0.8",
            "cmake":           "3.25.0-rc1",
            "conan":           "2.0.0-beta4",
            "freetype":        "2.12.1",
            "GIMP_mac":        "2.10.32",
            "GIMP_win":        "2.10.32",
            "git":             "2.38.1",
            "glew":            "2.2.0",
            "googletest":      "1.12.1",
            "Gradle":          "7.5.1",
            "grepWin":         "2.0.11",
            "KeePassXC":       "2.7.1",
            "libpng":          "1.6.38",
            "MuseScore":       "3.6.2",
            "ninja":           "1.11.1",
            "NotepadPlusPlus": "8.4.6",
            "OBS":             "28.0.3",
            "ogg":             "1.3.5",
            "python":          "3.10.8",
            "SDL":             "2.24.1",
            "SDL_image":       "2.6.2",
            "SDL_mixer":       "2.6.2",
            "SDL_ttf":         "2.20.1",
            "SFML":            "2.5.1",
            "TortoiseGit":     "2.13.0",
            "vorbis":          "1.3.7",
            "VS2022":          "17.3.6",
            "Xcode":           "14.0.1",
            "zlib":            "1.2.13",
        }

        self.debug = debug


    def compare_latest_to_current(self, tool):
        result = {}
        result["error"] = False
        result["uptodate"] = True

        start_time = ""
        try:
            if self.debug:
                start_time = time.time()
            latest_version = getattr(self, f"get_latest_version_{tool}")()
            if latest_version != self.versions[tool]:
                print(f"{tool} {self.versions[tool]} can be upgraded to {latest_version}.")
                result["uptodate"] = False
        except AttributeError as error:
            print(f"{tool} version could not be found. Check the website.")
            print(f"  Details: {error}")
            result["error"] = True
        except (HTTPError, URLError) as error:
            print(f"{tool} website could not be loaded.")
            print(f"  Details: {error}")
            result["error"] = True
        finally:
            if self.debug:
                elapsed_time = time.time() - start_time
                print(f"{tool}: {elapsed_time} seconds")
        return result


    def get_latest_version_7Zip(self):
        with urlopen("https://www.7-zip.org/") as page:
            soup = BeautifulSoup(page, "html.parser")

        b_tag_contents = soup.findAll("b")
        version_text_raw = None
        for b_tag_content in b_tag_contents:
            if "Download" in b_tag_content.text:
                version_text_raw = b_tag_content.text
                break

        return version_text_raw.split()[2]


    def get_latest_version_AndroidNDK(self):
        with urlopen("https://developer.android.com/ndk/downloads/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("h2", attrs={"id": "lts-downloads"}).text.split()[-1].strip("()")

        return version_text


    def get_latest_version_AndroidSDKAPI(self):
        with urlopen(
            "https://developer.android.com/guide/topics/manifest/uses-sdk-element") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(r"^/sdk/api_diff/\d+/changes$")}).text

        return version_text


    def get_latest_version_AndroidStudio(self):
        opener = build_opener(HTTPCookieProcessor())
        install_opener(opener)
        req = Request("https://developer.android.com/studio/",
            headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        with urlopen(req) as response:
            page = response.read().decode('utf8', errors='ignore')
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("div", attrs={"class": "dac-info-size"}).text.split()

        return version_items[4]


    def get_latest_version_bzip2(self):
        with urlopen("https://sourceware.org/bzip2/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("td", attrs={"colspan": "2"}).text

        for line in version_text_raw.splitlines():
            if "The current stable version" in line:
                version_text = line.split()[-1].strip(".")
                break

        return version_text


    def get_latest_version_cmake(self):
        opener = build_opener(HTTPCookieProcessor())
        install_opener(opener)
        req = Request("https://cmake.org/download/",
            headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        with urlopen(req) as response:
            page = response.read().decode('utf8', errors='ignore')
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h3").text.strip().split()

        version_text = version_items[2].strip("()")

        return version_text


    def get_latest_version_conan(self):
        with urlopen("https://github.com/conan-io/conan/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_texts = soup.findAll("a",
            attrs={"href":
            re.compile(r"^/conan-io/conan/releases/tag")})
        for version_text_raw in version_texts:
            version_text = version_text_raw.text.strip().split()[0]
            if version_text.split(".")[0] == "2":
                break

        return version_text


    def get_latest_version_freetype(self):
        with urlopen("https://sourceforge.net/projects/freetype/files/freetype2/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href":
            lambda L: L and L.startswith("/projects/freetype/files/freetype2/")}).text.strip()

        return str(version_text)


    def get_latest_version_GIMP_mac(self):
        with urlopen("https://www.gimp.org/downloads/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: "osx" in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_GIMP_win(self):
        with urlopen("https://www.gimp.org/downloads/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href": lambda L: "windows" in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_git(self):
        req = Request("https://git-scm.com/download", headers={"User-Agent": "Mozilla/72"})
        with urlopen(req) as response:
            page = response.read()
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"class": "version"}).text.strip()

        return version_text


    def get_latest_version_glew(self):
        with urlopen("https://github.com/nigels-com/glew/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href":
            re.compile(r"^/nigels-com/glew/releases/tag/glew-\d+\.\d+\.\d+$")}).text.split()

        return version_items[1]


    def get_latest_version_googletest(self):
        with urlopen("https://github.com/google/googletest/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href":
            re.compile(
                r"^/google/googletest/releases/tag/release-\d+\.\d+\.\d+$")}
            ).text.strip().lstrip("v")

        return version_text


    def get_latest_version_Gradle(self):
        with urlopen("https://gradle.org/install/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("p").text.strip().split()

        version_text = ""
        for word in version_items:
            result = re.match(r"^(\d+\.){1,2}(\d+)", word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_grepWin(self):
        with urlopen("https://github.com/stefankueng/grepWin/releases/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href": re.compile(
                r"^/stefankueng/grepWin/releases/tag/\d+\.\d+\.\d+$")}).text.split()

        return version_items[1]


    def get_latest_version_KeePassXC(self):
        with urlopen("https://keepassxc.org/download/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"class": "label label-success"}).text.lstrip("v")

        return version_text


    def get_latest_version_libpng(self):
        with urlopen("http://www.libpng.org/pub/png/libpng.html") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("font", attrs={"size": "+1"}).text.strip()

        return version_text


    def get_latest_version_OBS(self):
        with urlopen("https://obsproject.com/download") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("span",
            attrs={"class": "dl_ver"}).text.replace(" ", "").split(":")

        return version_items[1]


    def get_latest_version_ogg(self):
        with urlopen("https://xiph.org/downloads/") as page:
            soup = BeautifulSoup(page, "html.parser")

        td_tag_contents = soup.findAll("td")
        version_text = None
        ogg_version_found = False
        for td_tag_content in td_tag_contents:
            if ogg_version_found:
                version_text = td_tag_content.text
                break
            if "libogg" in td_tag_content.text:
                ogg_version_found = True

        return version_text


    def get_latest_version_MuseScore(self):
        with urlopen("https://musescore.org/en") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("span", attrs={"id": "download-version"}).text.split()

        return version_items[1]


    def get_latest_version_ninja(self):
        with urlopen("https://github.com/ninja-build/ninja/releases/latest") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/ninja-build/ninja/releases/tag/v\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_NotepadPlusPlus(self):
        req = Request("https://notepad-plus-plus.org/downloads",
            headers={"User-Agent": "Mozilla/72"})
        with urlopen(req) as response:
            page = response.read()
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href": lambda L: L and L.startswith("/downloads/")}).text.split()

        return version_items[2]


    def get_latest_version_python(self):
        with urlopen("https://www.python.org/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href":
            lambda L: L and L.startswith("/downloads/release/python-")}).text.strip().split()

        return version_items[1]


    def get_latest_version_SDL(self):
        with urlopen("https://github.com/libsdl-org/SDL/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href":
            re.compile(r"^/libsdl-org/SDL/releases/tag/release-\d+\.\d+\.\d+$")}).text.strip()

        return version_text


    def get_latest_version_SDL_image(self):
        with urlopen("https://github.com/libsdl-org/SDL_image/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/libsdl-org/SDL_image/releases/tag/release-\d+\.\d+\.\d+$")}).text.strip()

        return version_text


    def get_latest_version_SDL_mixer(self):
        with urlopen("https://github.com/libsdl-org/SDL_mixer/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/libsdl-org/SDL_mixer/releases/tag/release-\d+\.\d+\.\d+$")}).text

        return version_text


    def get_latest_version_SDL_ttf(self):
        with urlopen("https://github.com/libsdl-org/SDL_ttf/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/libsdl-org/SDL_ttf/releases/tag/release-\d+\.\d+\.\d+$")}).text.strip()

        return version_text


    def get_latest_version_SFML(self):
        with urlopen("https://www.sfml-dev.org/download.php") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("div", attrs={"class": "title"}).text.strip().split()

        return version_items[-1]


    def get_latest_version_TortoiseGit(self):
        with urlopen("https://tortoisegit.org/download/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("strong").text.strip().split()

        return version_items[-1]


    def get_latest_version_vorbis(self):
        with urlopen("https://xiph.org/downloads/") as page:
            soup = BeautifulSoup(page, "html.parser")

        td_tag_contents = soup.findAll("td")
        version_text = None
        vorbis_version_found = False
        for td_tag_content in td_tag_contents:
            if vorbis_version_found:
                version_text = td_tag_content.text
                break
            if "libvorbis" in td_tag_content.text:
                vorbis_version_found = True

        return version_text


    def get_latest_version_VS2022(self):
        with urlopen(
            "https://docs.microsoft.com/en-us/visualstudio/releases/2022/release-notes") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^#\d+\.\d+\.\d+$")}).text.strip().split()[4]

        return version_text


    def get_latest_version_Xcode(self):
        req = Request("https://apps.apple.com/us/app/xcode/id497799835",
            headers={"User-Agent": "Mozilla/72"})
        with urlopen(req) as response:
            page = response.read()
            soup = BeautifulSoup(page, "html.parser")
        version_items = soup.find("p",
            attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split()

        return version_items[1]


    def get_latest_version_zlib(self):
        with urlopen("https://zlib.net/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("font", attrs={"size": "+2"}).text.strip().split()

        return version_items[1]



def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug",
        required=False,
        help="Turn on debug info",
        action="store_true"
    )

    parser.add_argument(
        "--tool",
        required=False,
        help="Tool to version check",
        type=str
    )

    args = parser.parse_args()

    version_check = VersionCheck(args.debug)

    error = []
    uptodate = []

    if args.tool:
        results = version_check.compare_latest_to_current(args.tool)
        error.append(results["error"])
        uptodate.append(results["uptodate"])
    else:
        with Pool(processes=len(version_check.versions)) as pool:
            results = pool.map(version_check.compare_latest_to_current, version_check.versions)
        for result in results:
            error.append(result["error"])
            uptodate.append(result["uptodate"])

    if False in uptodate:
        print("Do the upgrade(s) and update the latest version(s) at the top of this script.")
        sys.exit(1)
    else:
        if True in error:
            sys.exit(1)
        else:
            print("Everything is up-to-date!")
            sys.exit(0)


if __name__ == "__main__":
    main()
