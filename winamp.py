from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus, kill_process
import os, ssl, subprocess, pickletools, logger_config

# Logging Configuration
logger_config.configure_logging() 

import logging 

# download winamp to location
def getWinamp(location):
    # create a subfolder to location
    path = os.path.join(location, 'Winamp')
    makeDir(path)
    
    url = 'https://download.winamp.com/winamp/winamp_latest_full.exe'
    target = os.path.join(path, 'winamp_latest_full.exe')

    logging.info('Downloading Winamp...')
    urlretrieve(url, target)
    logging.info('Winamp downloaded.')
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
    logging.info('Downloading CLEveR...')
    urlretrieve(url, target)
    logging.info('CLEveR downloaded.')
    return target

# start winamp
def start_winamp():
    winamp_path = 'C:\\Program Files (x86)\\Winamp\\winamp.exe'
    command = [winamp_path]
    try:
        subprocess.Popen(command)
        focus('EscapePodToolkit')
        logging.info('Winamp started successfully')
        return 'Winamp started successfully.'
    except FileNotFoundError:
        logging.debug('Winamp failed to start.')
        return 'ERROR: Failed to start Winamp.'
    
# stop winamp
def stop_winamp():
    winamp_process = "winamp.exe"
    try:
        kill_process(winamp_process)
        focus('EscapePodToolkit')
        logging.info('Winamp stopped successfully')
        return 'Winamp stopped successfully.'
    except FileNotFoundError:
        logging.debug('Winamp failed to stop.')
        return 'ERROR: Failed to stop Winamp.'