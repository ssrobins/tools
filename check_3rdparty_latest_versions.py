from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re



thirdparty_version = {
    'cmake':           {'installed': '3.10.1'},
    'freetype':        {'installed': '2.8.1'},
    'git':             {'installed': '2.15.1'},
    'glew':            {'installed': '2.1.0'},
    'googletest':      {'installed': '1.8.0'},
    'libpng':          {'installed': '1.6.34'},
    'Notepad++':       {'installed': '7.5.3'},
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



def get_latest_version_cmake():
    cmake_page = 'https://cmake.org/download/'
    page = urlopen(cmake_page)
    soup = BeautifulSoup(page, 'html.parser')

    cmake_items = soup.find('h3').text.strip().split()
    
    cmake_text = cmake_items[2].strip('()')
    
    return cmake_text



def get_latest_version_freetype():
    freetype_page = 'https://sourceforge.net/projects/freetype/files/freetype2/'
    page = urlopen(freetype_page)
    soup = BeautifulSoup(page, 'html.parser')

    freetype_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('/projects/freetype/files/freetype2/')}).text.strip()

    return str(freetype_text)



def get_latest_version_git():
    req = Request('https://git-scm.com/download', headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req).read()
    soup = BeautifulSoup(page, 'html.parser')

    git_text = soup.find('span', attrs={'class': 'version'}).text.strip()

    return str(git_text)



def get_latest_version_glew():
    glew_page = 'http://glew.sourceforge.net/'
    page = urlopen(glew_page)
    soup = BeautifulSoup(page, 'html.parser')

    glew_text = soup.find('a', attrs={'href': lambda L: L and L.startswith('https://sourceforge.net/projects/glew/files/glew/')}).text

    return str(glew_text)



def get_latest_version_googletest():
    googletest_page = 'https://github.com/google/googletest/releases'
    page = urlopen(googletest_page)
    soup = BeautifulSoup(page, 'html.parser')

    googletest_text_raw = soup.find('span', attrs={'class': 'tag-name'}).text.strip()

    googletest_text = googletest_text_raw.split('-')

    return googletest_text[1]



def get_latest_version_libpng():
    libpng_page = 'http://www.libpng.org/pub/png/libpng.html'
    page = urlopen(libpng_page)
    soup = BeautifulSoup(page, 'html.parser')

    libpng_text = soup.find('font', attrs={'size': '+1'}).text.strip()
    
    return libpng_text



def get_latest_version_NotepadPlusPlus():
    NotepadPlusPlus_page = 'https://notepad-plus-plus.org/download'
    page = urlopen(NotepadPlusPlus_page)
    soup = BeautifulSoup(page, 'html.parser')

    NotepadPlusPlus_items = soup.find('h1').text.strip().split()
    
    return NotepadPlusPlus_items[-1]



def get_latest_version_python():
    python_page = 'https://www.python.org/'
    page = urlopen(python_page)
    soup = BeautifulSoup(page, 'html.parser')

    python_text_items = soup.find('a', attrs={'href': lambda L: L and L.startswith('/downloads/release/python-')}).text.strip().split()

    return python_text_items[1]



def get_latest_version_SDL2():
    sdl2_page = 'https://www.libsdl.org/download-2.0.php'
    page = urlopen(sdl2_page)
    soup = BeautifulSoup(page, 'html.parser')

    header_items = soup.find('h1').text.strip().split()

    header_items_count = len(header_items)
    header_items_expected_count = 4
    if(header_items_count == header_items_expected_count):
        if(header_items[0] == 'SDL' and header_items[1] == 'version'):
            sdl2_version = header_items[2]
    else:
        print('Header count is ' + str(header_items_count) + ' but should be ' + str(header_items_expected_count))
        exit(1)
        
    return sdl2_version



def get_latest_version_SDL2_image():
    sdl2_image_page = 'https://www.libsdl.org/projects/SDL_image/'
    page = urlopen(sdl2_image_page)
    soup = BeautifulSoup(page, 'html.parser')

    sld2_image_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_image-')}).text.strip()

    sld2_image_items = re.findall(r"[\w']+", sld2_image_text_raw)
    sld2_image_text = sld2_image_items[1] + '.' + sld2_image_items[2] + '.' + sld2_image_items[3]

    return sld2_image_text



def get_latest_version_SDL2_mixer():
    sdl2_mixer_page = 'https://www.libsdl.org/projects/SDL_mixer/'
    page = urlopen(sdl2_mixer_page)
    soup = BeautifulSoup(page, 'html.parser')

    sld2_mixer_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_mixer-')}).text.strip()

    sld2_mixer_items = re.findall(r"[\w']+", sld2_mixer_text_raw)
    sld2_mixer_text = sld2_mixer_items[1] + '.' + sld2_mixer_items[2] + '.' + sld2_mixer_items[3]

    return sld2_mixer_text



def get_latest_version_SDL2_ttf():
    sdl2_ttf_page = 'https://www.libsdl.org/projects/SDL_ttf/'
    page = urlopen(sdl2_ttf_page)
    soup = BeautifulSoup(page, 'html.parser')

    sld2_ttf_text_raw = soup.find('a', attrs={'href': lambda L: L and L.startswith('release/SDL2_ttf-')}).text.strip()

    sld2_ttf_items = re.findall(r"[\w']+", sld2_ttf_text_raw)
    sld2_ttf_text = sld2_ttf_items[1] + '.' + sld2_ttf_items[2] + '.' + sld2_ttf_items[3]

    return sld2_ttf_text



def get_latest_version_TortoiseGit():
    TortoiseGit_page = 'https://tortoisegit.org/download/'
    page = urlopen(TortoiseGit_page)
    soup = BeautifulSoup(page, 'html.parser')

    TortoiseGit_items = soup.find('strong').text.strip().split()
    
    return TortoiseGit_items[-1]



def get_latest_version_VisualStudio():
    VisualStudio_page = 'https://www.visualstudio.com/en-us/news/releasenotes/vs2017-relnotes'
    page = urlopen(VisualStudio_page)
    soup = BeautifulSoup(page, 'html.parser')

    VisualStudio_text_raw = soup.find('h2', attrs={'id': re.compile('^[0-9]+.[0-9]+.[0-9]$')}).text.strip().split()
    
    return VisualStudio_text_raw[-1]



def get_latest_version_WinSCP():
    WinSCP_page = 'https://winscp.net/eng/download.php'
    page = urlopen(WinSCP_page)
    soup = BeautifulSoup(page, 'html.parser')

    WinSCP_items = soup.find('h3').text.strip().split()
    
    return WinSCP_items[-1]



def get_latest_version_zlib():
    zlib_page = 'https://zlib.net/'
    page = urlopen(zlib_page)
    soup = BeautifulSoup(page, 'html.parser')

    zlib_text_items = soup.find('font', attrs={'size': '+2'}).text.strip().split()
    
    return zlib_text_items[1]



def main():
    thirdparty_version['cmake']['latest'] = get_latest_version_cmake()
    thirdparty_version['freetype']['latest'] = get_latest_version_freetype()
    thirdparty_version['git']['latest'] = get_latest_version_git()
    thirdparty_version['glew']['latest'] = get_latest_version_glew()
    thirdparty_version['googletest']['latest'] = get_latest_version_googletest()
    thirdparty_version['libpng']['latest'] = get_latest_version_libpng()
    thirdparty_version['Notepad++']['latest'] = get_latest_version_NotepadPlusPlus()
    thirdparty_version['python']['latest'] = get_latest_version_python()
    thirdparty_version['SDL2']['latest'] = get_latest_version_SDL2()
    thirdparty_version['SDL2_image']['latest'] = get_latest_version_SDL2_image()
    thirdparty_version['SDL2_mixer']['latest'] = get_latest_version_SDL2_mixer()
    thirdparty_version['SDL2_ttf']['latest'] = get_latest_version_SDL2_ttf()
    thirdparty_version['TortoiseGit']['latest'] = get_latest_version_TortoiseGit()
    thirdparty_version['VisualStudio']['latest'] = get_latest_version_VisualStudio()
    thirdparty_version['WinSCP']['latest'] = get_latest_version_WinSCP()
    thirdparty_version['zlib']['latest'] = get_latest_version_zlib()
    
    uptodate = True
    
    for lib in thirdparty_version:
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
