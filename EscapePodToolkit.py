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
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s', force=True)

# Application version
__version__ = '0.1.0'

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
    titleName = '| Escape Pod Toolkit |'
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
            print(' [3] Remove Escape Pod Toolkit')
            print(' [.]')
            print(' [0] Exit Escape Pod Toolkit')
            print()
            
            mainMenuSelect = int(input('Select an option: '))
            if mainMenuSelect == 1:
                setup(menuTitle)
                
            elif mainMenuSelect == 2: operations()
            
            elif mainMenuSelect == 3:
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
    # create menu for services
    menuTitle = 'Operations Menu'
    titleName = '| Escape Pod Toolkit |'
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
            
            ops_menu_select = int(input('Select an option: '))
            if ops_menu_select == 1: start_broadcasting(path)
            elif ops_menu_select == 2: stop_broadcasting(path)
            elif ops_menu_select == 3:
                if track_reader_state != 'Running':
                    track_thread.start()
                    track_reader_state = 'Running'
                    logging.info('Track Reader feature started.')
                else:
                    stop_event.set()
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



#HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE HERE 


# Track Reader
def track_reader(track_reader_state, stop_event):
    logging.info(f'Track Reader State: {track_reader_state}')
    last_10_file_path = os.path.join(path, 'Streaming Data\last_10_tracks.txt')
    if track_reader_state == 'Unknown': 
        open(last_10_file_path, 'w').close()
    last_10_tracks(os.path.join(path, 'Streaming Data\\now_playing.txt'), last_10_file_path, stop_event)
    stop_event.set()  # Move this line after last_10_tracks
    logging.info('Track Reader feature stopped by exit.')

# Track Reader Threading
stop_event = threading.Event()
track_thread = threading.Thread(target=track_reader, args=(track_reader_state, stop_event,))

# initial setup
def setup(prevMenu):
    global path
    # not sure, maybe force a location? Yeah, do that!
    # define a temp location
    #print('Set an empty temporary directory...')
    #tempLocation = askdirectory()
    
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
    # Check AMIP installed
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

    #TODO
    # continue working on streaming services - need to add a 'kill application' command that partially matches a name (winamp can append the track to the process name)

    # create last ten tracks file - the trackname tool should be built in, and should create the files it needs during operation, and clean up at end of operation.

if __name__ == '__main__':
    logging.info(f'Starting Escape Pod Tool Kit version {__version__}')
    # get admin privileges
    if bootstrap() == True:
        logging.info('Admin privileges granted.')
        # Main Code
        focus('EscapePodToolkit')
        main()