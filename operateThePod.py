from nssm import nssm_start, nssm_stop
from functions import clear
import os, logger_config, sys, time, datetime, keyboard
from datetime import date

# Logging Configuration
logger_config.configure_logging() 

import logging

# Start Icecast via NSSM
# why is this called from the EscapePodToolKit only to call another method?
def start_icecast(location):
    logging.info('Starting Icecast via NSSM service...')
    nssm_start(location, 'Icecast')


# Stop Icecast via NSSM
# why is this called from the EscapePodToolKit only to call another method?
def stop_icecast(location):
    logging.info('Stopping Icecast via NSSM service...')
    nssm_start(location, 'Icecast')


# use CLEveR to load ogg.m3u into Winamp
def load_winamp_ogg(dj_name, path):
    logging.info('Loading local livestream...')
    # CLEveR.exe loadplay mike13000.ogg.m3u
    os.system(f'{path}\\{dj_name}.ogg.m3u')
   

global today
global trackList
today = str(date.today())
trackList = [''] * 11

# open the current track
def new_track(now_playing, last_10_file, version):
    with open(now_playing, 'r') as trackFile:
        newTrack = trackFile.readline()
        titleName = f'| Escape Pod Toolkit v{version} - Track Reader |'
        title = len(titleName)*'-'+'\n'+titleName+'\n'+len(titleName)*'-'
        print(title)
        print()
        print('Currently Playing: ' + newTrack)
        print()
        if newTrack == trackList[0]: pass
        else:
            trackCounter = 10
            tCounterLoop = True
            while tCounterLoop:
                trackList[trackCounter] = trackList[trackCounter - 1]
                trackCounter = trackCounter - 1
                if trackCounter == 0: tCounterLoop = False
            trackList[0] = newTrack
            # trigger new list
            output_file(last_10_file)
            # use the file path for now playing
            file_path = os.path.dirname(now_playing)
            # add the file to the total file list
            track_list_file(os.path.join(file_path, today + '.txt'), newTrack)
        trackFile.close()

# track list file operation
def track_list_file(file, track):
    # Get the current time
    current_time = datetime.datetime.now()
    # Format the current time as a string
    time_string = current_time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(file, 'a') as trListFile:
        trListFile.write(f'{time_string} - {track}' + '\n')
        trListFile.close()
        
# Output file
def output_file(file):
    # if file doesn't exist, create it!
    with open(file, 'w') as lastTen:
        lastCounter = 10
        lastLoop = True
        while lastLoop:
            lastTen.write(str(lastCounter) + ': ' + trackList[lastCounter] + '\n')
            lastCounter = lastCounter - 1
            if lastCounter == 0: lastLoop = False
        lastTen.close()

# Track List function here
def last_10_tracks(now_playing, last_10_tracks_file, stop_event, version):
    last10loop = True
    while last10loop and not stop_event.is_set():
        if keyboard.is_pressed('q') or stop_event.is_set():
            last10loop = False
        else:
            clear()  # Assuming clear is defined
            new_track(now_playing, last_10_tracks_file, version)  # Assuming new_track is defined
            with open(last_10_tracks_file) as list_file:
                for line in list_file:
                    print(line)
            print()
            print('Press \'q\' to view Main Menu.')
            time.sleep(10)
            clear()