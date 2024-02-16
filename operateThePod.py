from nssm import nssm_start, nssm_stop
import os, logger_config

# Logging Configuration
logger_config.configure_logging() 

import logging

# Start Icecast via NSSM
def start_icecast(location):
    logging.info('Starting Icecast via NSSM service...')
    nssm_start(location, 'Icecast')

# use CLEveR to load ogg.m3u into Winamp
def load_winamp_ogg(dj_name, path):
    logging.info('Loading local livestream...')
    # CLEveR.exe loadplay mike13000.ogg.m3u
    os.system(f'{path}/{dj_name}.ogg.m3u')

# stop Icecast via nssm
# kill Winamp