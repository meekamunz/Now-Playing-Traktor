from nssm import nssm_start, nssm_stop


# Start Icecast via NSSM
def start_icecast(location):
    nssm_start(location, 'Icecast')
# start Winamp
# use CLEveR to load ogg.m3u into Winamp
# stop Icecast via nssm
# kill Winamp