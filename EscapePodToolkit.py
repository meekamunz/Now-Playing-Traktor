from icecast import getIcecast, icecastXml
from nssm import getNssm, installNssm, nssmService
from winamp import getWinamp
from amip import getAmip, installAmip, amipConfig
from functions import wait, makeDir, guiInstaller, focus, bootstrap, clear, djName
from cleanup import removeIcecast, removeNssm, cleanupEPTroot, removeWinamp, removeAmip
import tkinter as tk
from time import sleep
from tkinter.filedialog import askdirectory
import os, sys

# hide the tk root window
root=tk.Tk()
root.withdraw()

# global variables
path = os.path.expandvars('%userprofile%\\Documents\\Escape Pod Toolkit')

# main code
def main():
    global path
    focus('EscapePodToolkit')
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
                
            elif mainMenuSelect == 2:
                # run scripts inc;
                # now-playing,
                # last-10-tracks
                pass
            
            elif mainMenuSelect == 3:
                # remove services & apps
                if removeIcecast(path) == True:
                    if removeNssm(path) == True:
                        if removeWinamp(path) == True:
                            if removeAmip(path) == True:
                                if cleanupEPTroot(path) == True:
                                    wait()
                                else: print('folder clean-up error.')
                            else: print('AMIP clean-up error.')
                        else: print('Winamp clean-up error.')
                    else: print('NSSM clean-up error.')
                else: print('Icecast clean-up error.')
            
            elif mainMenuSelect == 0:
                clear()
                sys.exit()
                
        except (IndexError, ValueError) as e: # input error handling, can print(e) if required
            print()
            print ('Invalid selection.  Please use a number in the list.')
            print('Type [0] to exit')
            print()
            sleep(1)

# initial setup
def setup(prevMenu):
    global path
    # not sure, maybe force a location?
    # define a temp location
    #print('Set an empty temporary directory...')
    #tempLocation = askdirectory()
    
    # Forced location
    print('Creating \'Escape Pod Toolkit\'...')
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

    # do AMIP stuff
    amip = getAmip(path)
    installAmip(amip)
    amipConfig(path+'\\Streaming Data')

    # Traktor Settings
    # Traktor installation path
    #
    # Traktor Settings (use icecastPassword)
    #TraktorSettings(path, djName, icecastIP, icecastPassword)

    #TODO
    # currently working on Traktor Settings

    # need to tell user to start Traktor streaming

    # create last ten tracks file - the trackname tool should be built in, and should create the files it needs during operation, and clean up at end of operation.

if __name__ == '__main__':
    # get admin privileges
    if bootstrap() == True: main()