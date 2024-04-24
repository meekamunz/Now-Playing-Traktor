from ast import pattern
from concurrent.futures import thread
import logging
from icecast import getIcecast, icecastXml, extract_dj_name_from_icecast
from nssm import getNssm, installNssm, nssmService
from winamp import getWinamp, start_winamp, getClever, stop_winamp
from amip import getAmip, installAmip, amipConfig
from functions import wait, makeDir, guiInstaller, focus, bootstrap, clear, djName, get_local_ip_addresses, prompt_select_ip, is_application_running
from cleanup import removeIcecast, removeNssm, cleanupEPTroot, removeWinamp, removeAmip
from traktorSettings import traktorMachine,  remoteTSI, localTSI
from operateThePod import load_winamp_ogg, start_icecast, stop_icecast, last_10_tracks
import tkinter as tk
from time import sleep
from tkinter.filedialog import askdirectory
import os, sys, logger_config, datetime, threading

# Logging Configuration
logger_config.configure_logging() 
#logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', force=True)

# Application version
__version__ = '0.2.0'

# hide the tk root window
root=tk.Tk()
root.withdraw()

# global variables
# use variable 'path' as a location for the services
global path
global broadcast_state
global track_reader_state
path = os.path.expandvars('%userprofile%\\Documents\\Escape Pod Toolkit')
broadcast_state={'state':'Unknown', 'duration': 'No broadcast yet'}
track_reader_state='Unknown'

# main code
def main():
    menuTitle = 'Main Menu'
    titleName = f'| Escape Pod Toolkit v{__version__} - Main Menu |'
    title = len(titleName)*'-'+'\n'+titleName+'\n'+len(titleName)*'-'
    menuLoop = True
    while menuLoop:
        try:
            clear()
            print(title)
            print()
            print(menuTitle)
            print()
            print(' [1] Setup Escape Pod Toolkit')
            print(' [2] Operate Escape Pod Toolkit')
            print(' [.]')
            print(' [9] Remove Escape Pod Toolkit')
            print(' [.]')
            print(' [0] Exit Escape Pod Toolkit')
            print()
            
            mainMenuSelect = int(input('Select an option: '))
            if mainMenuSelect == 1:
                setup(menuTitle)
                
            elif mainMenuSelect == 2: operations()
            
            elif mainMenuSelect == 9:
                # remove services & apps
                if removeIcecast(path) == True:
                    if removeNssm(path) == True:
                        if removeWinamp(path) == True:
                            if removeAmip(path) == True:
                                if cleanupEPTroot(path) == True:
                                    wait()
                                else: logging.debug('folder clean-up error.')
                            else: logging.debug('AMIP clean-up error.')
                        else: logging.debug('Winamp clean-up error.')
                    else: logging.debug('NSSM clean-up error.')
                else: logging.debug('Icecast clean-up error.')
            
            elif mainMenuSelect == 0:
                clear()
                logging.info('Exiting Escape Pod Tool Kit.')
                sys.exit()
                
        except (IndexError, ValueError) as e: # input error handling, can print(e) if required
            print()
            print ('Invalid selection.  Please use a number in the list.')
            print('Type [0] to exit')
            print()
            sleep(1)


# operate the pod
def operations(b_state='state', duration='duration', track_reader_state='Unknown'):
    global track_reader_thread, stop_event, track_reader_running
    # create menu for services
    menuTitle = 'Operations Menu'
    titleName = f'| Escape Pod Toolkit v{__version__} - Operations Menu |'
    title = len(titleName)*'-'+'\n'+titleName+'\n'+len(titleName)*'-'
    ops_menu_loop = True
    
    while ops_menu_loop:
        try:
            clear()
            print(title)
            print()
            print(menuTitle)
            print()
            print(' [1] Start Broadcasting')
            print(' [2] Stop Broadcasting')
            if track_reader_state != 'Running': print(' [3] Enable Track Reader')
            if track_reader_state == 'Running': print(' [3] Disable Track Reader')
            print(' [.]')
            print(' [0] Back')
            print()
            print(f'Broadcasting State: {broadcast_state[b_state]}')
            if broadcast_state[b_state] == 'On Air': print(f'Broadcast: on-going')
            else: print(f'Broadcast duration: {broadcast_state[duration]}')
            print(f'Track Reader State: {track_reader_state}')
            
            # Accept a number or 'q' to quit
            ops_menu_select = input('Select an option: ').strip().lower()
            if ops_menu_select.isdigit():
                ops_menu_select = int(ops_menu_select)  # Convert to int if it's a digit
            if ops_menu_select == 'q':
                pass
            
            # Process the operations menu
            if ops_menu_select == 1: start_broadcasting(path)
            elif ops_menu_select == 2: stop_broadcasting(path)
            elif ops_menu_select == 3:
                if not track_reader_running:  # If the track reader isn't running, start it
                    track_reader_thread, stop_event = create_track_reader_thread()
                    track_reader_thread.start()
                    track_reader_running = True  # Update the running flag
                    track_reader_state = 'Running'
                    logging.info('Track Reader feature started.')
                else:  # If the track reader is running, stop it
                    stop_event.set()  # Signal to stop
                    track_reader_thread.join()  # Ensure the thread has stopped
                    track_reader_running = False  # Update the running flag
                    track_reader_state = 'Stopped'
                    logging.debug('Track Reader feature stopped by menu.')
            elif ops_menu_select == 0:
                main()
            else: logging.debug('Error in OPs menu.')
                
        except (IndexError, ValueError) as e: # input error handling, can print(e) if required
            print()
            print ('Invalid selection.  Please use a number in the list.')
            print('Type [0] to exit')
            print()
            sleep(1)
            

def start_broadcasting(path):
    # Start Icecast via NSSM
    start_icecast(path)
    
    # User to start streaming from Traktor
    extracted_dj_name = extract_dj_name_from_icecast('C:\Program Files (x86)\Icecast\icecast.xml')
    print(f'Hey {extracted_dj_name}, start streaming in Traktor now!')
    wait()
    
    # start Winamp
    start_winamp()
    
    # use CLEveR to load ogg.m3u into Winamp
    load_winamp_ogg(extracted_dj_name, path)
    
    # set broadcasting_state
    broadcast_state.update({'state':'On Air', 'started': datetime.datetime.now()})
    logging.info('Broadcasting started.')
    

def stop_broadcasting(path):
    logging.debug('feature not complete.')
    
    # stop Icecast via nssm
    stop_icecast(path)
    
    # kill Winamp
    stop_winamp()
    
    # calculate broadcast duration
    duration = datetime.datetime.now() - broadcast_state['started']
    
    # set broadcasting_state
    broadcast_state.update({'state':'Off Air', 'stopped': datetime.datetime.now(), 'duration': duration})
    
    # Tell user that services are stopped
    logging.info('All broadcasting services are stopped.')
    logging.info(f'Broadcast duration was {duration}.')


# Track Reader
def track_reader(track_reader_state, stop_event):
    logging.info(f'Track Reader State: {track_reader_state}')
    last_10_file_path = os.path.join(path, 'Streaming Data\last_10_tracks.txt')
    if track_reader_state == 'Unknown': 
        open(last_10_file_path, 'w').close()
    # NEED TO ADD:
    # track_reader_state == 'Stopped':
    # do some restart without deleting the current last_10_tracks file
    last_10_tracks(os.path.join(path, 'Streaming Data\\now_playing.txt'), last_10_file_path, stop_event, __version__)
    stop_event.set()  # Move this line after last_10_tracks
    logging.info('Track Reader feature stopped by exit.')

# Track Reader Threading
# Initialize the stop_event and track_thread inside a function to allow for new instances
def create_track_reader_thread():
    stop_event = threading.Event()  # You can reset the event flag each time
    track_thread = threading.Thread(target=track_reader, args=(track_reader_state, stop_event))
    return track_thread, stop_event

# Global variables to manage the thread state
track_reader_thread = None
stop_event = None
track_reader_running = False  # Use this to track whether the thread is running


# initial setup
def setup(prevMenu):
    global path
    
    # Forced location
    logging.info('Creating \'Escape Pod Toolkit\'...')
    makeDir(path)
    makeDir(path+'\\Streaming Data')
    
    # download icecast
    icecast = getIcecast(path)
    # install ICECAST
    guiInstaller(icecast)
    
    # need to configure ICECAST
    icecastPassword=icecastXml(djName())
    
    # download nssm-2.24
    nssm = getNssm(path)
    # install nssm-2.24
    installNssm(nssm)
    # setup Icecast as a service using nssm
    nssmService(path, 'Icecast')
    
    # need to get winamp
    winamp = getWinamp(path)
    # need to install winamp
    guiInstaller(winamp)
    
    # need to get CLEveR (CommandLine EVEnt Renderer for WinAmp)
    getClever(path)
    
    # do AMIP stuff
    amip = getAmip(path)
    installAmip(amip)
    amipConfig(os.path.join(path, 'Streaming Data'))
    # add the last_10_tracks file:
    last_10_file_path = os.path.join(path, 'Streaming Data\last_10_tracks.txt')
    open(last_10_file_path, 'w').close()
    
    # Traktor Settings
    # Prompt user to close Traktor
    traktor_application_check = True
    while traktor_application_check:
        if is_application_running('Traktor'): 
            print('Please close your Traktor application.')
            wait()
        else: traktor_application_check = False
        
    # assume icecast is running on local host
    # select IP address that icecast is running on
    if get_local_ip_addresses:
        print('Please select the IP address for your network.')
        icecast_ip = prompt_select_ip(get_local_ip_addresses())
    else:
        logging.debug('ERROR: No local IP addresses found.')
        
    TSI_data=[icecastPassword[1], icecast_ip, icecastPassword[0]]
    TSI_updated = False, 'never set'
    TSI_check = True
    while TSI_check:
        if TSI_updated[0] == False:
            if traktorMachine() == 'local':
                if TSI_updated[1].startswith('INFORMATION: '): reminder = True, 'Don\'t forget to copy the \'Tracktor Settings.tsi\' file back to your remote PC.'
                else: reminder = False, None
                TSI_updated = localTSI(TSI_data[0], TSI_data[1], TSI_data[2])
                print(TSI_updated[1])
                if reminder[0]==True: print(reminder[1])
            else:
                TSI_updated = remoteTSI(TSI_data[0], TSI_data[1], TSI_data[2])
                print(TSI_updated[1])
                print()
                print('1. Get your \'Traktor Settings.tsi\' file from the following location on the remote PC:')
                print()
                print('   %userprofile%\\Documents\\Native Instruments\\Traktor <version_number>\\')
                print()
                print('2. Make a copy of the file locally, just in case I got the code wrong!')
                print('3. Copy it to this PC.  Make a note of the location you copy it to.')
                print('4. Choose \'Yes\' when asked if Traktor is installed locally')
                print('5. Use the file you saved when selecting \'Traktor Settings.tsi\'.')
                print('6. Once complete, copy the file back to the original PC, replacing the original file.')
                print()
        TSI_check = not TSI_updated[0]

if __name__ == '__main__':
    logging.info(f'Starting Escape Pod Tool Kit version {__version__}')
    # get admin privileges
    if bootstrap() == True:
        logging.info('Admin privileges granted.')
        # Main Code
        focus('EscapePodToolkit')
        main()