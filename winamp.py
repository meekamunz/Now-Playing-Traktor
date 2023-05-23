from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, ssl

# download winamp to location
def getWinamp(location):
    # create a sub folder to location
    path = os.path.join(location, 'Winamp')
    makeDir(path)
    
    url = 'https://download.winamp.com/winamp/winamp_latest_full.exe'
    target = os.path.join(path, 'winamp_latest_full.exe')

    print('Downloading Winamp...')
    urlretrieve(url, target)
    print('Downloaded.')
    return target