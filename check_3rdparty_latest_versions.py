#!/usr/bin/env python3

from urllib.request import build_opener, HTTPCookieProcessor, install_opener, Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
from multiprocessing import Pool
import argparse
import json
import re
import time



class VersionCheck:
    def __init__(self, debug):
        self.versions = {
            "7Zip":            "22.00",
            "AndroidNDK":      "r23c",
            "AndroidSDKAPI":   "33",
            "AndroidStudio":   "2021.2.1",
            "bzip2":           "1.0.8",
            "cmake":           "3.24.0-rc2",
            "conan":           "1.49.0",
            "freetype":        "2.12.1",
            "GIMP_mac":        "2.10.32",
            "GIMP_win":        "2.10.32",
            "git":             "2.36.1",
            "glew":            "2.1.0",
            "googletest":      "1.12.0",
            "Gradle":          "7.4.2",
            "grepWin":         "2.0.10",
            "KeePassXC":       "2.7.1",
            "libpng":          "1.6.37",
            "MuseScore":       "3.6.2",
            "ninja":           "1.11.0",
            "NotepadPlusPlus": "8.4.2",
            "OBS":             "27.2.4",
            "ogg":             "1.3.5",
            "python":          "3.10.5",
            "SDL2":            "2.0.22",
            "SDL2_image":      "2.0.5",
            "SDL2_mixer":      "2.0.4",
            "SDL2_ttf":        "2.0.18",
            "SFML":            "2.5.1",
            "TortoiseGit":     "2.13.0",
            "vorbis":          "1.3.7",
            "VS2022":          "17.2.5",
            "Xcode":           "13.4.1",
            "zlib":            "1.2.12",
        }

        self.debug = debug
        

    def compare_latest_to_current(self, tool):
        result = dict();
        result["error"] = False
        result["uptodate"] = True

        try:
            if self.debug:
                start_time = time.time()
            latest_version = getattr(self, f"get_latest_version_{tool}")()
            if(latest_version != self.versions[tool]):
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
        page = urlopen("https://www.7-zip.org/")
        soup = BeautifulSoup(page, "html.parser")

        b_tag_contents = soup.findAll("b")
        version_text_raw = None
        for b_tag_content in b_tag_contents:
            if "Download" in b_tag_content.text:
                version_text_raw = b_tag_content.text
                break

        return version_text_raw.split()[2]


    def get_latest_version_AndroidNDK(self):
        page = urlopen("https://developer.android.com/ndk/downloads/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("h2", attrs={"id": "lts-downloads"}).text.split()[-1].strip("()")

        return version_text


    def get_latest_version_AndroidSDKAPI(self):
        page = urlopen("https://developer.android.com/guide/topics/manifest/uses-sdk-element")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/sdk/api_diff/\d+/changes$")}).text

        return version_text


    def get_latest_version_AndroidStudio(self):
        opener = build_opener(HTTPCookieProcessor())
        install_opener(opener)
        req = Request("https://developer.android.com/studio/", headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        page = urlopen(req).read().decode('utf8', errors='ignore')
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("div", attrs={"class": "dac-info-size"}).text.split()

        return version_items[4]


    def get_latest_version_bzip2(self):
        page = urlopen("https://sourceware.org/bzip2/")
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
        req = Request("https://cmake.org/download/", headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        page = urlopen(req).read().decode('utf8', errors='ignore')
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h3").text.strip().split()
        
        version_text = version_items[2].strip("()")
        
        return version_text


    def get_latest_version_conan(self):
        page = urlopen("https://docs.conan.io/en/latest/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": lambda L: L and L.startswith("changelog.html#")}).text.split()[0]
        #version_text = soup.find("span", attrs={"class": "dl-version"}).text.strip()

        return version_text


    def get_latest_version_freetype(self):
        page = urlopen("https://sourceforge.net/projects/freetype/files/freetype2/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": lambda L: L and L.startswith("/projects/freetype/files/freetype2/")}).text.strip()

        return str(version_text)


    def get_latest_version_GIMP_mac(self):
        page = urlopen("https://www.gimp.org/downloads/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: "osx" in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_GIMP_win(self):
        page = urlopen("https://www.gimp.org/downloads/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: "windows" in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_git(self):
        req = Request("https://git-scm.com/download", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"class": "version"}).text.strip()

        return version_text


    def get_latest_version_glew(self):
        page = urlopen("http://glew.sourceforge.net/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": lambda L: L and L.startswith("https://sourceforge.net/projects/glew/files/glew/")}).text

        return str(version_text)


    def get_latest_version_googletest(self):
        page = urlopen("https://github.com/google/googletest/releases")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/google/googletest/releases/tag/release-\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_Gradle(self):
        page = urlopen("https://gradle.org/install/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("p").text.strip().split()

        version_text = ""
        for word in version_items:
            result = re.match("^(\d+\.){1,2}(\d+)", word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_grepWin(self):
        page = urlopen("https://github.com/stefankueng/grepWin/releases/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": re.compile("^/stefankueng/grepWin/releases/tag/\d+\.\d+\.\d+$")}).text.split()

        return version_items[1]


    def get_latest_version_KeePassXC(self):
        page = urlopen("https://keepassxc.org/download/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"class": "label label-success"}).text.lstrip("v")

        return version_text


    def get_latest_version_libpng(self):
        page = urlopen("http://www.libpng.org/pub/png/libpng.html")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("font", attrs={"size": "+1"}).text.strip()

        return version_text


    def get_latest_version_OBS(self):
        page = urlopen("https://obsproject.com/download")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("span", attrs={"class": "dl_ver"}).text.replace(" ", "").split(":")

        return version_items[1]


    def get_latest_version_ogg(self):
        page = urlopen("https://xiph.org/downloads/")
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
        page = urlopen("https://musescore.org/en")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("span", attrs={"id": "download-version"}).text.split()

        return version_items[1]


    def get_latest_version_ninja(self):
        page = urlopen("https://github.com/ninja-build/ninja/releases/latest")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/ninja-build/ninja/releases/tag/v\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_NotepadPlusPlus(self):
        req = Request("https://notepad-plus-plus.org/downloads", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: L and L.startswith("/downloads/")}).text.split()

        return version_items[2]


    def get_latest_version_python(self):
        page = urlopen("https://www.python.org/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: L and L.startswith("/downloads/release/python-")}).text.strip().split()

        return version_items[1]


    def get_latest_version_SDL2(self):
        page = urlopen("https://www.libsdl.org/download-2.0.php")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h1").text.strip().split()
            
        return version_items[2]


    def get_latest_version_SDL2_image(self):
        page = urlopen("https://www.libsdl.org/projects/SDL_image/")
        soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("a", attrs={"href": lambda L: L and L.startswith("release/SDL2_image-")}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = f"{version_items[1]}.{version_items[2]}.{version_items[3]}"

        return version_text


    def get_latest_version_SDL2_mixer(self):
        page = urlopen("https://www.libsdl.org/projects/SDL_mixer/")
        soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("a", attrs={"href": lambda L: L and L.startswith("release/SDL2_mixer-")}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = f"{version_items[1]}.{version_items[2]}.{version_items[3]}"

        return version_text


    def get_latest_version_SDL2_ttf(self):
        page = urlopen("https://github.com/libsdl-org/SDL_ttf/releases")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/libsdl-org/SDL_ttf/releases/tag/release-\d+\.\d+\.\d+$")}).text.strip().lstrip("v")

        return version_text


    def get_latest_version_SFML(self):
        page = urlopen("https://www.sfml-dev.org/download.php")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("div", attrs={"class": "title"}).text.strip().split()

        return version_items[-1]


    def get_latest_version_TortoiseGit(self):
        page = urlopen("https://tortoisegit.org/download/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("strong").text.strip().split()
        
        return version_items[-1]


    def get_latest_version_vorbis(self):
        page = urlopen("https://xiph.org/downloads/")
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
        page = urlopen("https://docs.microsoft.com/en-us/visualstudio/releases/2022/release-notes")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": re.compile("^#(\d+\.){1,3}(\d+)$")}).text.strip().split()

        version_text = ""
        for word in version_items:
            result = re.match("^(\d+\.){1,2}(\d+)$", word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_Xcode(self):
        req = Request("https://apps.apple.com/us/app/xcode/id497799835", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("p", attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split()

        return version_items[1]


    def get_latest_version_zlib(self):
        page = urlopen("https://zlib.net/")
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

    error = list()
    uptodate = list()

    if args.tool:
        results = version_check.compare_latest_to_current(args.tool)
        error.append(results["error"])
        uptodate.append(results["uptodate"])
    else:
        with Pool(processes=len(version_check.versions)) as pool:
            results = pool.map(version_check.compare_latest_to_current, version_check.versions)
        for index in range(len(results)):
            error.append(results[index]["error"])
            uptodate.append(results[index]["uptodate"])

    if False in uptodate:
        print("Do the upgrade(s) and update the latest version(s) at the top of this script.")
        exit(1)
    else:
        if True in error:
            exit(1)
        else:
            print("Everything is up-to-date!")
            exit(0)


if __name__ == "__main__":
    main()
