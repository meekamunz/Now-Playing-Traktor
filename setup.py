from icecast import getIcecast
from functions import wait
import tkinter as tk
from tkinter.filedialog import askdirectory
import os, shutil

# hide the tk root window
root=tk.Tk()
root.withdraw()

if __name__ == '__main__':
    # define a temp location
    print('Set an empty temporary directory...')
    tempLocation = askdirectory()
    #print('Emptying directory...')
    #for filename in os.listdir(tempLocation):
    #    file_path = os.path.join(tempLocation, filename)
    #    try:
    #        if os.path.isfile(file_path) or os.path.islink(file_path):
    #            print('Deleting '+file_path+'...')
    #            os.unlink(file_path)
    #        elif os.path.isdir(file_path):
    #            print('Deleting '+file_path+'...')
    #            shutil.rmtree(file_path, onerror=onerror)
    #    except Exception as e:
    #        print('Failed to delete %s. Reason: %s' % (file_path, e))
    # need to install ICECAST
    getIcecast(tempLocation)

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