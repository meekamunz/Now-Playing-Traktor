from nssm import nssm_start, nssm_stop
import os

# Start Icecast via NSSM
def start_icecast(location):
    nssm_start(location, 'Icecast')

# use CLEveR to load ogg.m3u into Winamp
def load_winamp_ogg(dj_name, path):
    # CLEveR.exe loadplay mike13000.ogg.m3u
    os.system(f'{path}/{dj_name}.ogg.m3u')

# stop Icecast via nssm
# kill Winamp