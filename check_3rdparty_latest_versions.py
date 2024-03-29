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
            "7Zip":            "23.01",
            "AndroidNDK":      "r26c",
            "AndroidSDKAPI":   "34",
            "AndroidStudio":   "2023.2.1",
            "box2d":           "2.4.1",
            "bzip2":           "1.0.8",
            "cmake":           "3.29.0",
            "conan":           "2.2.2",
            "freetype":        "2.13.2",
            "GIMP":            "2.10.36",
            "git":             "2.44.0",
            "glew":            "2.2.0",
            "googletest":      "1.14.0",
            "Gradle":          "8.7",
            "grepWin":         "2.0.15",
            "KeePassXC":       "2.7.7",
            "libpng":          "1.6.43",
            "MuseScore":       "4.2.1",
            "ninja":           "1.11.1",
            "NotepadPlusPlus": "8.6.4",
            "OBS":             "30.1.1",
            "ogg":             "1.3.5",
            "python":          "3.12.2",
            "SDL":             "2.30.1",
            "SDL_image":       "2.8.2",
            "SDL_mixer":       "2.8.0",
            "SDL_ttf":         "2.22.0",
            "SFML":            "2.6.1",
            "vorbis":          "1.3.7",
            "VS2022":          "17.9.5",
            "Xcode":           "15.3",
            "zlib":            "1.3.1",
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
        req = Request("https://developer.android.com/studio/releases",
            headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        with urlopen(req) as response:
            page = response.read().decode('utf8', errors='ignore')
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h1", attrs={"class": "devsite-page-title"}).text.split()

        return version_items[-1]


    def get_latest_version_box2d(self):
        with urlopen("https://github.com/erincatto/box2d/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/erincatto/box2d/releases/tag/v\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


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

        version_items = soup.find("h2", attrs={"id": "latest"}).text.strip().split()

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


    def get_latest_version_GIMP(self):
        with urlopen("https://www.gimp.org/") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"id": "ver"}).text

        return str(version_text)


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
                r"^/google/googletest/releases/tag/v\d+\.\d+\.\d+$")}
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
        with urlopen("https://github.com/keepassxreboot/keepassxc/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/keepassxreboot/keepassxc/releases/tag/\d+\.\d+\.\d+$")}
                ).text.strip().lstrip("Release ")

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

        version_text_raw = soup.find("a",
            attrs={"href": re.compile(
                r"^https://downloads.xiph.org/releases/ogg/libogg-\d+\.\d+\.\d+\.tar.gz$")}).text

        version_text = ""
        result = re.match(r"^libogg-(\d+\.\d+\.\d+)\.tar\.gz$", version_text_raw)
        if result:
            version_text = result.group(1)

        return version_text


    def get_latest_version_MuseScore(self):
        with urlopen("https://github.com/musescore/MuseScore/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/musescore/MuseScore/tree/v\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_ninja(self):
        with urlopen("https://github.com/ninja-build/ninja/releases/latest") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a",
            attrs={"href": re.compile(
                r"^/ninja-build/ninja/releases/tag/v\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_NotepadPlusPlus(self):
        with urlopen("https://github.com/notepad-plus-plus/notepad-plus-plus/releases") as page:
            soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a",
            attrs={"href": re.compile(
                r"^/notepad-plus-plus/notepad-plus-plus/releases/tag/v\d+\.\d+\.\d+$"
                )}).text.split()

        return version_items[-1]


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

        version_text_raw = soup.find("a",
            attrs={"href": re.compile(r"^#\d+\.\d+\.\d+$")})
        if version_text_raw:
            version_text = version_text_raw.text.strip().split()[4]
        else:
            version_text = soup.find("h2",
            attrs={"id": re.compile(
                r"^\d+--visual-studio-\d+-version-\d+$")}).text.strip().split()[-1]

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
