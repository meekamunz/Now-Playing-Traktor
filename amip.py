from urllib.request import urlretrieve
from functions import wait, sleep, makeDir, focus
import os, zipfile

def getAmip(location):
    # create a sub folder to location
    path = os.path.join(location, 'AMIP')
    makeDir(path)

    # Use this version only!!!
    print('Downloading AMIP...')
    
    # set target file+directory
    target = os.path.join(path, 'amip_winamp.zip')
    url = 'http://amip.tools-for.net/ds/dl.php?f=/files/amip_winamp.zip'
    urlretrieve(url, target)
    print('Complete.')
    return target

# install amip
def installAmip(amipZip):
    print('Extracting NSSM...')
    
    # get the dir from target
    targetDir = amipZip.rsplit('\\', 1)[0]
    # extract the right version from the zip
    with zipfile.ZipFile(amipZip, 'r') as zip_ref:
        zip_ref.extractall(targetDir)
    print('Extracted AMIP.')

# amip file configurator
def amipConfig(location):
    # open the plugin.ini
    with open ('C:\Program Files (x86)\Winamp\Plugins\plugin.ini', 'r') as file:
        filedata = file.read()

    # Replace target parts
    filedata = filedata.replace('CFG_SFILE=""', 'CFG_SFILE="C:\A\LOCATION\now_playing.txt')
    filedata = filedata.replace('CFG_SPLAY="  np: %name"', 'CFG_SPLAY="%name"')
    filedata = filedata.replace('CFG_SPAUSE="  np: %name [paused]"', 'CFG_SPAUSE="ERROR 1"')
    filedata = filedata.replace('CFG_SEXIT="  np: (Winamp is not active ;-)"', 'CFG_SEXIT=""')
    filedata = filedata.replace('CFG_UPDATEFILE=0', 'CFG_UPDATEFILE=1')
    filedata = filedata.replace('CFG_SFILE=""', 'CFG_SFILE="'+location+'"')

    # Write over the plugin.ini with new data
    with open('C:\Program Files (x86)\Winamp\Plugins\plugin.ini', 'w') as file:
        file.write(filedata)