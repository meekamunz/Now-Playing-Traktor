from urllib.request import urlretrieve
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, zipfile, subprocess

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
    nssmServiceRemove(location, service)
    os.popen('nssm install '+service+' C:\\Program Files (x86)\\Icecast\\icecast.bat')
    #test
    os.popen('nssm start Icecast')
    wait()
    os.popen('nssm stop Icecast')
    os.chdir(cwd)

# NSSM Service remover
def nssmServiceRemove(location, service):
    workingDir=location+'\\nssm\\nssm-2.24-101-g897c7ad\\win32\\'
    cwd=os.getcwd()
    os.chdir(workingDir)
    try:
        # in case of previous install
        print('Stopping '+service+'...')
        if os.popen('nssm stop '+service) != 'Can\'t open service!':
            print(service+' stopped.  Removing '+service+'...')
            os.popen('nssm remove '+service)
            print(service+' removed.')
    except Exception as e:
        print('No Existing service.')
    wait()
    os.chdir(cwd)

# nssm_start
def nssm_start(location, service_name):
    nssm_path=location+'\\nssm\\nssm-2.24-101-g897c7ad\\win32\\nssm.exe'
    command = [nssm_path, 'start', service_name]
    #
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(f"Service '{service_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start service '{service_name}': {e.output.decode()}")

# nssm_stop
def nssm_stop(location, service_name):
    nssm_path=location+'\\nssm\\nssm-2.24-101-g897c7ad\\win32\\nssm.exe'
    command = [nssm_path, 'stop', service_name]
    #
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
        print(f"Service '{service_name}' stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop service '{service_name}': {e.output.decode()}")