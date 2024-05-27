from functions import focus, wait, sleep
import os, subprocess, logger_config

# Logging Configuration
#logger_config.configure_logging() 

import logging 

# remove Icecast program and files
def removeIcecast(location):
    dir = 'C:\\Program Files (x86)\\Icecast\\'
    logging.info('Uninstalling Icecast...')
    p = subprocess.run([dir+'Uninstall.exe'])
    if p.returncode != 0:
        logging.debug('Error uninstalling Icecast...')
        wait()
    else: logging.info('Icecast uninstalled.')
    logging.info('Removing Icecast folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\Icecast'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    logging.info('Icecast folders removed.')
    return True

# remove NSSM files
def removeNssm(location):
    logging.info('Removing NSSM...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\nssm'))
    logging.info('NSSM removed.')
    return True

# remove Escape Pod Tools folder
def cleanupEPTroot(location):
    logging.info('Removing Escape Pod Toolkit folders...')
    os.system('rmdir /S /Q "{}"'.format(location))
    logging.info('Escape Pod Toolkit folders removed.')
    return True

# remove winamp program
def removeWinamp(location):
    dir = 'C:\\Program Files (x86)\\Winamp\\'
    logging.info('Uninstalling Winamp...')
    p = subprocess.run([dir+'UninstWA.exe'])
    if p.returncode != 0:
        logging.debug('Error uninstalling Winamp...')
        wait()
    else: logging.info('Winamp uninstalled.')
    logging.info('Removing Winamp folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\Winamp'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    logging.info('Winamp folders removed.')
    return True

# remove amip program
def removeAmip(location):
    dir = 'C:\\Program Files (x86)\\Winamp\\Plugins\\'
    logging.info('Uninstalling AMIP...')
    p = subprocess.run([dir+'un_configurator.exe'])
    if p.returncode != 0:
        logging.debug('Error uninstalling AMIP...')
        wait()
        logging.debug('Attempting alternate uninstall path...')
        q = subprocess.run([dir+'amip_uninstall.exe'])
        if q.returncode != 0:
            logging.debug('Alternate uninstaller failed.  Aborting AMIP uninstall.')
            wait()
    else: logging.info('AMIP uninstalled.')
    logging.info('Removing AMIP folders...')
    os.system('rmdir /S /Q "{}"'.format(location+'\\AMIP'))
    os.system('rmdir /S /Q "{}"'.format(dir))
    logging.info('AMIP folders removed.')
    return True