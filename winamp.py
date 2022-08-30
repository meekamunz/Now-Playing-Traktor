from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, ssl

# download winamp to location
def getWinamp(location):
    # create a sub folder to location
    path = os.path.join(location, 'Winamp')
    makeDir(path)
    
    url = 'https://download.nullsoft.com/winamp/client/Winamp59_9999_rc4_full_en-us.exe'
    target = os.path.join(path, 'Winamp59_9999_rc4_full_en-us.exe')

    print('Downloading Winamp...')
    urlretrieve(url, target)
    print('Downloaded.')
    return target