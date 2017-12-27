from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re



thirdparty_version = {
    'cmake':           {'installed': '3.10.1'},
    'freetype':        {'installed': '2.8.1'},
    'git':             {'installed': '2.15.1'},
    'glew':            {'installed': '2.1.0'},
    'googletest':      {'installed': '1.8.0'},
    'grepWin':         {'installed': '1.7.1'},
    'libpng':          {'installed': '1.6.34'},
    'NotepadPlusPlus': {'installed': '7.5.3'},
    'python':          {'installed': '3.6.4'},
    'SDL2':            {'installed': '2.0.7'},
    'SDL2_image':      {'installed': '2.0.2'},
    'SDL2_mixer':      {'installed': '2.0.2'},
    'SDL2_ttf':        {'installed': '2.0.14'},
    'TortoiseGit':     {'installed': '2.5.0'},
    'VisualStudio':    {'installed': '15.5.2'},
    'WinSCP':          {'installed': '5.11.3'},
    'zlib':            {'installed': '1.2.11'},
}



class VersionCheck:
    def get_latest_version_cmake():
        page = urlopen('https://cmake.org/download/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h3').text.strip().split()
        
        version_text = version_items[2].strip('()')
        
        return version_text



    def get_latest_version_freetype():
        page = urlopen('https://sourceforge.net/projects/freetype/files/freetype2/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('/projects/freetype/files/freetype2/')}).text.strip()

        return str(version_text)



    def get_latest_version_git():
        req = Request('https://git-scm.com/download', headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('span', attrs={'class': 'version'}).text.strip()

        return str(version_text)



    def get_latest_version_glew():
        page = urlopen('http://glew.sourceforge.net/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('https://sourceforge.net/projects/glew/files/glew/')}).text

        return str(version_text)



    def get_latest_version_googletest():
        page = urlopen('https://github.com/google/googletest/releases')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('span', attrs={'class': 'tag-name'}).text.strip()

        version_text = version_text_raw.split('-')

        return version_text[1]



    def get_latest_version_grepWin():
        page = urlopen('http://grepwin.sourceforge.net/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('small').text.strip().split('-')

        return version_items[1]



    def get_latest_version_libpng():
        page = urlopen('http://www.libpng.org/pub/png/libpng.html')
        soup = BeautifulSoup(page, 'html.parser')

        version_text = soup.find('font', attrs={'size': '+1'}).text.strip()
        
        return version_text



    def get_latest_version_NotepadPlusPlus():
        page = urlopen('https://notepad-plus-plus.org/download')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h1').text.strip().split()
        
        return version_items[-1]



    def get_latest_version_python():
        page = urlopen('https://www.python.org/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('a', attrs={'href': lambda L: L and L.startswith('/downloads/release/python-')}).text.strip().split()

        return version_items[1]



    def get_latest_version_SDL2():
        page = urlopen('https://www.libsdl.org/download-2.0.php')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h1').text.strip().split()
            
        return version_items[2]



    def get_latest_version_SDL2_image():
        page = urlopen('https://www.libsdl.org/projects/SDL_image/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_image-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text



    def get_latest_version_SDL2_mixer():
        page = urlopen('https://www.libsdl.org/projects/SDL_mixer/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_mixer-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text



    def get_latest_version_SDL2_ttf():
        page = urlopen('https://www.libsdl.org/projects/SDL_ttf/')
        soup = BeautifulSoup(page, 'html.parser')

        version_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_ttf-')}).text.strip()

        version_items = re.findall(r"[\w']+", version_text_raw)
        version_text = version_items[1] + '.' + version_items[2] + '.' + version_items[3]

        return version_text



    def get_latest_version_TortoiseGit():
        page = urlopen('https://tortoisegit.org/download/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('strong').text.strip().split()
        
        return version_items[-1]



    def get_latest_version_VisualStudio():
        page = urlopen('https://www.visualstudio.com/en-us/news/releasenotes/vs2017-relnotes')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h2', attrs={'id': re.compile('^[0-9]+.[0-9]+.[0-9]$')}).text.strip().split()
        
        return version_items[-1]



    def get_latest_version_WinSCP():
        page = urlopen('https://winscp.net/eng/download.php')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('h3').text.strip().split()
        
        return version_items[-1]



    def get_latest_version_zlib():
        page = urlopen('https://zlib.net/')
        soup = BeautifulSoup(page, 'html.parser')

        version_items = soup.find('font', attrs={'size': '+2'}).text.strip().split()
        
        return version_items[1]



def main():
    uptodate = True
    
    for lib in thirdparty_version:
        thirdparty_version[lib]['latest'] = getattr(VersionCheck, 'get_latest_version_' + lib)()
        if(thirdparty_version[lib]['latest'] == thirdparty_version[lib]['installed']):
            print(lib + ' ' + thirdparty_version[lib]['installed'] + ' is up-to-date.')
        else:
            print(lib + ' ' + thirdparty_version[lib]['installed'] + ' can be upgraded to ' + thirdparty_version[lib]['latest'] + '.')
            uptodate = False
    
    print()

    if uptodate:
        print('Everything listed above is up-to-date!')
        exit(0)
    else:
        print('One or more things listed above can be upgraded.  Do the upgrade and update the latest version at the top of this script.')
        exit(1)



if __name__ == "__main__":
    main()
