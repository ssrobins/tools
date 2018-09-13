from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import re



class VersionCheck:
    def __init__(self):
        self.versions = {
            'AndroidNDK':      {'installed': 'r17c'},
            'AndroidSDKTools': {'installed': '4333796'},
            'AndroidStudio':   {'installed': '3.1.4'},
            'bzip2':           {'installed': 'cannot'},
            'bzip2new':        {'installed': '1.0.6'},
            'cmake':           {'installed': '3.12.2'},
            'freetype':        {'installed': '2.9.1'},
            'gcc':             {'installed': '8.2'},
            'GIMP_mac':        {'installed': '2.10.6'},
            'GIMP_win':        {'installed': '2.10.6'},
            'git_mac':         {'installed': '2.18.0'},
            'git_win':         {'installed': '2.19.0'},
            'GitLabRunner':    {'installed': '11.2.0'},
            'glew':            {'installed': '2.1.0'},
            'googletest':      {'installed': '1.8.1'},
            'grepWin':         {'installed': '1.7.1'},
            'KeePass':         {'installed': '2.40'},
            'libpng':          {'installed': '1.6.35'},
            'MuseScore':       {'installed': '2.3.2'},
            'NotepadPlusPlus': {'installed': '7.5.8'},
            'python':          {'installed': '3.7.0'},
            'SDL2':            {'installed': '2.0.8'},
            'SDL2_image':      {'installed': '2.0.3'},
            'SDL2_mixer':      {'installed': '2.0.2'},
            'SDL2_ttf':        {'installed': '2.0.14'},
            'SFML':            {'installed': '2.5.0'},
            'TortoiseGit':     {'installed': '2.7.0'},
            'VisualStudio':    {'installed': '15.8.4'},
            'WinSCP':          {'installed': '5.13.4'},
            'Xcode':           {'installed': '9.4.1'},
            'zlib':            {'installed': '1.2.11'},
        }
        
        self.error = False
        self.uptodate = True


    def has_error(self):
        return self.error


    def all_uptodate(self):
        return self.uptodate


    def compare_latest_to_current(self):
        for item in self.versions:
            try:
                self.versions[item]['latest'] = getattr(self, 'get_latest_version_' + item)()
                if(self.versions[item]['latest'] != self.versions[item]['installed']):
                    print(item + ' ' + self.versions[item]['installed'] + ' can be upgraded to ' + self.versions[item]['latest'] + '.')
                    self.uptodate = False
            except AttributeError:
                print(item + ' version could not be found. Check the website.')
                self.error = True
            except (HTTPError, URLError):
                print(item + ' website couldn\'t be loaded.')
                self.error = True

        print()


    def get_latest_version_AndroidNDK(self):
        page = urlopen('https://developer.android.com/ndk/downloads/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('h2', attrs={'id': 'stable-downloads'}).text.split()[-1].strip('()')

        return version_text


    def get_latest_version_AndroidSDKTools(self):
        page = urlopen('https://developer.android.com/studio/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('button', attrs={'data-modal-dialog-id': 'sdk_linux_download'}).text.split('-')
        version_subitems = version_items[3].split('.')

        return version_subitems[0]


    def get_latest_version_AndroidStudio(self):
        req = Request('https://developer.android.com/studio/', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686)'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('div', attrs={'class': 'dac-studio-version'}).text.split()

        return version_items[0]


    def get_latest_version_bzip2(self):
        page = urlopen('http://www.bzip.org/downloads.html')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h3').text.strip().split()

        return version_items[2]


    def get_latest_version_bzip2new(self):
        page = urlopen('https://github.com/nemequ/bzip2/releases')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': re.compile('^/nemequ/bzip2/releases/tag/v[0-9]+\.[0-9]+\.[0-9]+$')}).text

        return version_text


    def get_latest_version_cmake(self):
        page = urlopen('https://cmake.org/download/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h3').text.strip().split()
        
        version_text = version_items[2].strip('()')
        
        return version_text


    def get_latest_version_freetype(self):
        page = urlopen('https://sourceforge.net/projects/freetype/files/freetype2/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('/projects/freetype/files/freetype2/')}).text.strip()

        return str(version_text)


    def get_latest_version_gcc(self):
        page = urlopen('https://gcc.gnu.org/releases.html')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('gcc')}).text.strip().split()

        return str(version_text[1])


    def get_latest_version_GIMP_mac(self):
        page = urlopen('https://www.gimp.org/downloads/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('a', attrs={'href': lambda L: 'osx' in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_GIMP_win(self):
        page = urlopen('https://www.gimp.org/downloads/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('a', attrs={'href': lambda L: 'windows' in L}).text.strip().split()

        return str(version_items[2])


    def get_latest_version_git_mac(self):
        req = Request('https://git-scm.com/download', headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('span', attrs={'id': 'installer-version'})

        return version_text_raw['data-mac']


    def get_latest_version_git_win(self):
        req = Request('https://git-scm.com/download', headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('span', attrs={'id': 'installer-version'})

        return version_text_raw['data-win']


    def get_latest_version_GitLabRunner(self):
        page = urlopen('https://gitlab.com/gitlab-org/gitlab-runner/raw/master/CHANGELOG.md')

        version_text_raw = ''
        for line in page.readlines():
            line_str = line.decode("utf-8")
            if line_str.startswith('v'):
                version_text_raw = line_str.split()[1]
                if 'rc' not in version_text_raw:
                    break

        return version_text_raw


    def get_latest_version_glew(self):
        page = urlopen('http://glew.sourceforge.net/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('https://sourceforge.net/projects/glew/files/glew/')}).text

        return str(version_text)


    def get_latest_version_googletest(self):
        page = urlopen('https://github.com/google/googletest/releases')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': re.compile('^/google/googletest/releases/tag/release-[0-9]+\.[0-9]+\.[0-9]+$')}).text.lstrip('v')

        return version_text


    def get_latest_version_grepWin(self):
        page = urlopen('https://sourceforge.net/projects/grepwin/files/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': re.compile('^/projects/grepwin/files/[0-9]+\.[0-9]+[\.[0-9]+]*/$')}).text.strip()

        return version_text


    def get_latest_version_KeePass(self):
        page = urlopen('https://keepass.info/download.html')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('th', attrs={'colspan': '2'}).text.strip().split()

        return version_items[-1]


    def get_latest_version_libpng(self):
        page = urlopen('http://www.libpng.org/pub/png/libpng.html')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('font', attrs={'size': '+1'}).text.strip()

        return version_text


    def get_latest_version_MuseScore(self):
        page = urlopen('https://musescore.org/en')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('span', attrs={'id': 'download-version'}).text.split()

        return version_items[1]


    def get_latest_version_NotepadPlusPlus(self):
        page = urlopen('https://notepad-plus-plus.org/download')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h1').text.strip().split()
        
        return version_items[-1]


    def get_latest_version_python(self):
        page = urlopen('https://www.python.org/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('a', attrs={'href': lambda L: L and L.startswith('/downloads/release/python-')}).text.strip().split()

        return version_items[1]


    def get_latest_version_SDL2(self):
        page = urlopen('https://www.libsdl.org/download-2.0.php')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h1').text.strip().split()
            
        return version_items[2]


    def get_latest_version_SDL2_image(self):
        page = urlopen('https://www.libsdl.org/projects/SDL_image/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_image-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text


    def get_latest_version_SDL2_mixer(self):
        page = urlopen('https://www.libsdl.org/projects/SDL_mixer/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_mixer-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text


    def get_latest_version_SDL2_ttf(self):
        page = urlopen('https://www.libsdl.org/projects/SDL_ttf/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_ttf-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text


    def get_latest_version_SFML(self):
        page = urlopen('https://www.sfml-dev.org/download.php')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('div', attrs={'class': 'title'}).text.strip().split()

        return version_items[-1]


    def get_latest_version_TortoiseGit(self):
        page = urlopen('https://tortoisegit.org/download/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('strong').text.strip().split()
        
        return version_items[-1]


    def get_latest_version_VisualStudio(self):
        page = urlopen('https://docs.microsoft.com/en-us/visualstudio/releasenotes/vs2017-relnotes')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('a', attrs={'href': re.compile('^#(\d+\.){1,2}(\d+)$')}).text.strip().split()

        version_text = ''
        for word in version_items:
            result = re.match('^(\d+\.){1,2}(\d+)$', word)
            if result:
                version_text = result.group()
                break

        return version_text


    def get_latest_version_WinSCP(self):
        page = urlopen('https://sourceforge.net/projects/winscp/files/WinSCP/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': re.compile('^/projects/winscp/files/WinSCP/[0-9]+\.[0-9]+[\.[0-9]+]*/$')}).text.strip()
        
        return version_text


    def get_latest_version_Xcode(self):
        page = urlopen('https://developer.apple.com/news/releases/')
        soup = BeautifulSoup(page, 'html.parser')

        h2_tag_contents = soup.findAll('h2')
        version_text_raw = None
        for h2_tag_content in h2_tag_contents:
            if 'Xcode' in h2_tag_content.text:
                version_text_raw = h2_tag_content.text

        version_items = version_text_raw.split()
        if len(version_items) >= 3 and version_items[2] == 'beta':
            version_text = ' '.join(version_items[1:])
        else:
            version_text = version_items[1]

        return version_text


    def get_latest_version_zlib(self):
        page = urlopen('https://zlib.net/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('font', attrs={'size': '+2'}).text.strip().split()
        
        return version_items[1]



def main():
    version_check = VersionCheck()
    
    version_check.compare_latest_to_current()

    if version_check.all_uptodate():
        if version_check.has_error() == False:
            print('Everything is up-to-date!')
            exit(0)
        else:
            exit(1)
    else:
        print('Do the upgrade(s) and update the latest version(s) at the top of this script.')
        exit(1)



if __name__ == "__main__":
    main()
