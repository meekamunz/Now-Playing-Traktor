#from calendar import c
from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus, kill_process
import os, ssl, subprocess, pickletools, logger_config, win32gui, win32api, win32con

# Logging Configuration
#logger_config.configure_logging() 

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
    if not os.path.exists(winamp_path):
        logging.error('Winamp executable not found.')
        return 'ERROR: Winamp executable not found.'
    
    command = [winamp_path]
    try:
        process = subprocess.Popen(command)
        logging.info('Winamp started successfully.')
        
        # Wait briefly to ensure Winamp starts properly
        sleep(2)
        
        # Focus on the EscapePodToolkit window (ensure this function is correctly implemented)
        focus('EscapePodToolkit')
        
        return 'Winamp started successfully.'
    except Exception as e:
        logging.error(f'Failed to start Winamp: {e}')
        return f'ERROR: Failed to start Winamp: {e}'
    
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
    
# Send Winamp command
def send_winamp_command(command):
    win32api.SendMessage(winamp_window, WM_COMMAND, command, 0)

WINAMP_VOLUME_DOWN = 40059

# winamp_mute
def winamp_mute():
    # check winamp is running
    winamp_window = win32gui.FindWindow("Winamp v1.x", None)
    if winamp_window == 0:
        logging.debug('Winamp not running.')
    else:
        logging.info('Winamp is running.')
    for _ in range(100):  # Adjust as necessary
        send_winamp_command(WINAMP_VOLUME_DOWN)