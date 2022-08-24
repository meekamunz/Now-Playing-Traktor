from ast import Try
from icecast import getIcecast
from functions import wait, makeDir, guiInstaller
import tkinter as tk
from tkinter.filedialog import askdirectory
import os

# hide the tk root window
root=tk.Tk()
root.withdraw()

if __name__ == '__main__':

    # not sure, maybe force a location?
    # define a temp location
    #print('Set an empty temporary directory...')
    #tempLocation = askdirectory()

    # Forced location
    print('Creating \'Escape Pod Toolkit\'...')
    path = os.path.expandvars('%userprofile%\Documents\Escape Pod Toolkit')
    makeDir(path)
    
    # download icecast
    icecast = getIcecast(path)
    # need to install ICECAST
    guiInstaller(icecast)

    # need to configure ICECAST
    # need to install nssm-2.24
    # need to tell user to set Traktor settings for either local or remote streaming
    # need to tell user to start Traktor streaming
    # need to install AMIP
    # need to configure AMIP (use C:\Program Files (x86)\Winamp\Plugins\plugin.ini)
        # set CFG_SFILE="C:\A\LOCATION\now_playing.txt"
        # set CFG_IGNORE="(Connecting\.\.\.)|(Prebuffering :)"
        # set CFG_SPLAY="%name"
        # set CFG_SPAUSE="ERROR 1"
        # set CFG_SSTOP="ERROR 2"
        # set CFG_SEXIT=""
        # CFG_UPDATEFILE=1
    # create last ten tracks file