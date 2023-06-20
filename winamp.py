from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, ssl

# download winamp to location
def getWinamp(location):
    # create a subfolder to location
    path = os.path.join(location, 'Winamp')
    makeDir(path)
    
    url = 'https://download.winamp.com/winamp/winamp_latest_full.exe'
    target = os.path.join(path, 'winamp_latest_full.exe')

    print('Downloading Winamp...')
    urlretrieve(url, target)
    print('Downloaded.')
    return target

# download CLEver to location
def getClever(location):
    # create a subfolder to location
    path = os.path.join(location, 'CLEveR')
    makeDir(path)
    #
    url = 'https://winampheritage.com/plugin/58602/CLEveR.exe'
    target = os.path.join(path, 'CLEveR.exe')
    #
    print('Downloading CLEveR...')
    urlretrieve(url, target)
    print('Downloaded.')
    return target