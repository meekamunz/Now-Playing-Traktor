from functions import focus, wait, sleep
import os, subprocess

# remove Icecast program and files
def removeIcecast(location):
    dir = 'C:\\Program Files (x86)\\Icecast\\'
    print('Uninstalling Icecast...')
    p = subprocess.run([dir+'Uninstall.exe'])
    if p.returncode != 0:
        print('Error uninstalling Icecast...')
        wait()
    else: print('Icecast uninstalled.')
    print('Removing Icecast folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\Icecast'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    print('Icecast folders removed.')
    return True

# remove NSSM files
def removeNssm(location):
    print('Removing NSSM...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\nssm'))
    print('NSSM removed.')
    return True

# remove Escape Pod Tools folder
def cleanupEPTroot(location):
    print('Removing Escape Pod Toolkit folders...')
    os.system('rmdir /S /Q "{}"'.format(location))
    print('Escape Pod Toolkit folders removed.')
    return True

# remove winamp program
def removeWinamp(location):
    dir = 'C:\\Program Files (x86)\\Winamp\\'
    print('Uninstalling Winamp...')
    p = subprocess.run([dir+'UninstWA.exe'])
    if p.returncode != 0:
        print('Error uninstalling Winamp...')
        wait()
    else: print('Winamp uninstalled.')
    print('Removing Winamp folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\Winamp'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    print('Winamp folders removed.')
    return True

# remove amip program
def removeAmip(location):
    dir = 'C:\\Program Files (x86)\\Winamp\\Plugins\\'
    print('Uninstalling AMIP...')
    p = subprocess.run([dir+'un_configurator.exe'])
    if p.returncode != 0:
        print('Error uninstalling AMIP...')
        wait()
        print('Attempting alternate uninstall path...')
        q = subprocess.run([dir+'amip_uninstall.exe'])
        if q.returncode != 0:
            print('Alternate uninstaller failed.  Aborting AMIP uninstall.')
            wait()
    else: print('AMIP uninstalled.')
    print('Removing AMIP folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\AMIP'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    print('AMIP folders removed.')
    return True