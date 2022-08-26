from urllib.request import urlretrieve
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, zipfile

# get NSSM
def getNssm(location):
    # create a sub folder to location
    path = os.path.join(location, 'nssm')
    makeDir(path)
    
    # Use this version only!!!
    print('Downloading NSSM...')
    
    # set target file+directory
    target = os.path.join(path, 'nssm-2.24-101-g897c7ad.zip')
    url = 'https://nssm.cc/ci/nssm-2.24-101-g897c7ad.zip'
    urlretrieve(url, target)
    print('Complete.')
    return target

# install NSSM
def installNssm(nssmZip):
    print('Extracting NSSM...')
    
    # get the dir from target
    targetDir = nssmZip.rsplit('\\', 1)[0]
    # extract the right version from the zip
    with zipfile.ZipFile(nssmZip, 'r') as zip_ref:
        zip_ref.extractall(targetDir)
    print('Extracted NSSM.')

# NSSM Service Installer
def nssmService(location, service):
    # this is failing???
    workingDir=location+'\\nssm\\nssm-2.24-101-g897c7ad\\win32\\'
    cwd=os.getcwd()
    os.chdir(workingDir)
    try:
        # in case of previous install
        os.popen('nssm stop Icecast')
        os.popen('nssm remove Icecast')
    except Exception as e:
        print('No Existing service.')
    os.popen('nssm install '+service+' C:\\Program Files (x86)\\Icecast\\icecast.nat')
    #test
    os.popen('nssm start Icecast')
    wait()
    os.popen('nssm stop Icecast')
    os.chdir(cwd)