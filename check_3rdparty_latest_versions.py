#!/usr/bin/env python3

from urllib.request import Request, urlopen
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
            "AndroidNDK":      "r21",
            "AndroidSDKAPI":   "29",
            "AndroidSDKTools": "6200805",
            "AndroidStudio":   "3.6.2",
            "bzip2":           "1.0.8",
            "cmake":           "3.17.1",
            "conan":           "1.24.0",
            "DockerCE":        "2.2.0.5",
            "DockerEngine":    "19.03.8",
            "freetype":        "2.10.1",
            "gcc":             "9.3.0",
            "GIMP_mac":        "2.10.14",
            "GIMP_win":        "2.10.18",
            "git_mac":         "2.23.0",
            "git_win":         "2.26.1",
            "GitLabRunner":    "12.9.0", # Stuck at 12.5.0: https://gitlab.com/gitlab-org/gitlab-runner/issues/6202 and won't support Windows 1903 and greater: https://gitlab.com/gitlab-org/gitlab-runner/issues/4396
            "glew":            "2.1.0",
            "googletest":      "1.10.0",
            "Gradle":          "6.3",
            "grepWin":         "2.0.0",
            "KeePassXC":       "2.5.4",
            "libpng":          "1.6.37",
            "MuseScore":       "3.4.2",
            "ninja":           "1.10.0",
            "NotepadPlusPlus": "7.8.5",
            "OBS_mac":         "25.0.7",
            "OBS_win":         "25.0.4",
            "openjdk":         "8u252",
            "python":          "3.8.2",
            "SDL2":            "2.0.12", # See if I can finally upgrade from 2.0.8: https://bugzilla.libsdl.org/show_bug.cgi?id=4601
            "SDL2_image":      "2.0.5",
            "SDL2_mixer":      "2.0.4",
            "SDL2_ttf":        "2.0.15",
            "SFML":            "2.5.1",
            "TortoiseGit":     "2.10.0",
            "VS2017":          "15.9.22",
            "VS2019":          "16.5.4",
            "WinSCP":          "5.17.3",
            "Xcode":           "11.4.1 (11E503a)",
            "zlib":            "1.2.11",
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


    def get_latest_version_AndroidNDK(self):
        page = urlopen("https://developer.android.com/ndk/downloads/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("h2", attrs={"id": "stable-downloads"}).text.split()[-1].strip("()")

        return version_text


    def get_latest_version_AndroidSDKAPI(self):
        page = urlopen("https://developer.android.com/studio/releases/platforms")
        soup = BeautifulSoup(page, "html.parser")

        h2_tag_contents = soup.findAll("h2", attrs={"id": re.compile("^\d+(\.\d)*$")})
        for h2_tag_content in h2_tag_contents:
            match = re.search("\(API level (\d+)\)", h2_tag_content.text)
            if match:
                version_text = match.group(1)
                break

        return version_text


    def get_latest_version_AndroidSDKTools(self):
        page = urlopen("https://developer.android.com/studio/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("button", attrs={"data-modal-dialog-id": "sdk_linux_download"}).text.replace("_", "-").split("-")

        version_subitems = version_items[2].split(".")

        return version_subitems[0]


    def get_latest_version_AndroidStudio(self):
        req = Request("https://developer.android.com/studio/", headers={"User-Agent": "Mozilla/72 (X11; Linux i686)"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("div", attrs={"class": "dac-info-size"}).text.split()

        return version_items[0]


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
        page = urlopen("https://cmake.org/download/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h3").text.strip().split()
        
        version_text = version_items[2].strip("()")
        
        return version_text


    def get_latest_version_conan(self):
        page = urlopen("https://conan.io/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("span", attrs={"class": "dl-version"}).text.strip()

        return version_text


    def get_latest_version_DockerCE(self):
        page = urlopen("https://docs.docker.com/docker-for-windows/release-notes/")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("h2", attrs={"id": lambda L: L and L.startswith("docker-desktop-community")}).text.split()

        return version_items[3]


    def get_latest_version_DockerEngine(self):
        page = urlopen("https://registry.hub.docker.com/v1/repositories/docker/tags")
        soup = BeautifulSoup(page, "html.parser")

        data = json.loads(soup.get_text())

        version_text_list = list()
        for item in data:
            docker_tag = item.get("name")
            match = re.match("^\d+\.\d+\.\d+", docker_tag)
            if match:
                version_text_list.append(match.group())
        version_text_list.sort()

        return version_text_list[-1]


    def get_latest_version_freetype(self):
        page = urlopen("https://sourceforge.net/projects/freetype/files/freetype2/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": lambda L: L and L.startswith("/projects/freetype/files/freetype2/")}).text.strip()

        return str(version_text)


    def get_latest_version_gcc(self):
        page = urlopen("https://registry.hub.docker.com/v1/repositories/gcc/tags")
        soup = BeautifulSoup(page, "html.parser")

        data = json.loads(soup.get_text())

        version_text_list = list()
        for item in data:
            docker_tag = item.get("name")
            if "latest" not in docker_tag:
                version_text_list.append(item.get("name"))
        version_text_list.sort()

        return version_text_list[-1]


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


    def get_latest_version_git_mac(self):
        req = Request("https://git-scm.com/download", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("span", attrs={"id": "installer-version"})

        return version_text_raw["data-mac"]


    def get_latest_version_git_win(self):
        req = Request("https://git-scm.com/download", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("span", attrs={"id": "installer-version"})

        return version_text_raw["data-win"]


    def get_latest_version_GitLabRunner(self):
        req = Request("https://gitlab.com/gitlab-org/gitlab-runner/raw/master/CHANGELOG.md", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req)

        version_text_raw = ""
        for line in page.readlines():
            line_str = line.decode("utf-8")
            if line_str.startswith("## v"):
                version_text_raw = line_str.split("## v")[1].split("(")[0].strip()
                if "rc" not in version_text_raw:
                    break

        return version_text_raw


    def get_latest_version_glew(self):
        page = urlopen("http://glew.sourceforge.net/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": lambda L: L and L.startswith("https://sourceforge.net/projects/glew/files/glew/")}).text

        return str(version_text)


    def get_latest_version_googletest(self):
        page = urlopen("https://github.com/google/googletest/releases")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/google/googletest/releases/tag/release-\d+\.\d+\.\d+$")}).text.lstrip("v")

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


    def get_latest_version_OBS_mac(self):
        page = urlopen("https://obsproject.com")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("div", attrs={"class": "latest_icon latest_mac"}).next_sibling.text

        return version_text


    def get_latest_version_OBS_win(self):
        page = urlopen("https://obsproject.com")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("div", attrs={"class": "latest_icon latest_win"}).next_sibling.text

        return version_text


    def get_latest_version_MuseScore(self):
        page = urlopen("https://musescore.org/en")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("span", attrs={"id": "download-version"}).text.split()

        return version_items[1]


    def get_latest_version_ninja(self):
        page = urlopen("https://github.com/ninja-build/ninja/releases/latest")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/ninja-build/ninja/releases/tag/v\d+\.\d+\.\d+$")}).text.lstrip("v")

        return version_text


    def get_latest_version_NotepadPlusPlus(self):
        req = Request("https://notepad-plus-plus.org/downloads", headers={"User-Agent": "Mozilla/72"})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": lambda L: L and L.startswith("/downloads/")}).text.split()

        return version_items[2]


    def get_latest_version_openjdk(self):
        page = urlopen("https://registry.hub.docker.com/v1/repositories/amd64/openjdk/tags")
        soup = BeautifulSoup(page, "html.parser")

        data = json.loads(soup.get_text())

        version_text_list = list()
        for item in data:
            docker_tag = item.get("name")
            if "jdk-slim" in docker_tag and "8u" in docker_tag:
                version_text_list.append(re.match("^\d+u\d+", docker_tag).group())
        version_text_list.sort()

        return version_text_list[-1]


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
        page = urlopen("https://www.libsdl.org/projects/SDL_ttf/")
        soup = BeautifulSoup(page, "html.parser")

        version_text_raw = soup.find("a", attrs={"href": lambda L: L and L.startswith("release/SDL2_ttf-")}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = f"{version_items[1]}.{version_items[2]}.{version_items[3]}"

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


    def get_latest_version_VS2017(self):
        page = urlopen("https://docs.microsoft.com/en-us/visualstudio/releasenotes/vs2017-relnotes")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": re.compile("^#(\d+\.){1,2}(\d+)$")}).text.strip().split()

        version_text = ""
        for word in version_items:
            result = re.match("^(\d+\.){1,2}(\d+)$", word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_VS2019(self):
        page = urlopen("https://docs.microsoft.com/en-us/visualstudio/releases/2019/release-notes")
        soup = BeautifulSoup(page, "html.parser")

        version_items = soup.find("a", attrs={"href": re.compile("^#(\d+\.){1,2}(\d+)$")}).text.strip().split()

        version_text = ""
        for word in version_items:
            result = re.match("^(\d+\.){1,2}(\d+)$", word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_WinSCP(self):
        page = urlopen("https://sourceforge.net/projects/winscp/files/WinSCP/")
        soup = BeautifulSoup(page, "html.parser")

        version_text = soup.find("a", attrs={"href": re.compile("^/projects/winscp/files/WinSCP/\d+\.\d+[\.\d+]*/$")}).text.strip()
        
        return version_text


    def get_latest_version_Xcode(self):
        page = urlopen("http://developer.apple.com/news/releases/")
        soup = BeautifulSoup(page, "html.parser")

        h2_tag_contents = soup.findAll("h2")
        version_text_raw = None
        for h2_tag_content in h2_tag_contents:
            if ("Xcode" in h2_tag_content.text and
               "beta" not in h2_tag_content.text and
               "GM seed" not in h2_tag_content.text):
                version_text_raw = h2_tag_content.text
                break

        version_items = version_text_raw.split()
        version_text = " ".join(version_items[1:])

        return version_text


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
