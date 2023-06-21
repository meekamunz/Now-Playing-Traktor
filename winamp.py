from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, ssl, subprocess

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

# download CLEveR to location
def getClever(location):
    # create a subfolder to location
    path = os.path.join(location, 'CLEveR')
    makeDir(path)
    # The winamp heritage site is probably doing a javescript funny...
    #url = 'https://winampheritage.com/plugin/58602/CLEveR.exe'
    url = 'http://www.etcwiki.org/dl/CLEveR.exe'
    target = os.path.join(path, 'CLEveR.exe')
    #
    print('Downloading CLEveR...')
    urlretrieve(url, target)
    print('Downloaded.')
    return target

# start winamp
def start_winamp():
    winamp_path = 'C:\\Program Files (x86)\\Winamp\\winamp.exe'
    command = [winamp_path]
    try:
        subprocess.Popen(command)
        focus('EscapePodToolkit')
        return 'Winamp started successfully.'
    except FileNotFoundError:
        return 'ERROR: Failed to start Winamp.'