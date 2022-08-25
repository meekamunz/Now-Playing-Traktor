from urllib.request import urlretrieve
from functions import remoteFileList, wait, sleep, makeDir, focus
import os

def getIcecast(location):
    # create a sub folder to location
    path = os.path.join(location, 'Icecast')
    makeDir(path)
    
    # get list of versions of Icecast and sort
    print('Getting Icecast versions...')
    print()
    url = 'https://downloads.xiph.org/releases/icecast'
    ext = 'exe'
    icecastVersions = []
    
    for file in remoteFileList(url, ext):
        icecastVersions.append(file)
    icecastVersions.sort(reverse=True)

    # split each entry to just show the filename
    i=0
    versions=[]
    splitLoop = True
    while splitLoop:
        if i<len(icecastVersions):
            versions.append(icecastVersions[i].split('/')[-1])
        else: splitLoop = False
        i=i+1

    # list of versions is just the file name, not the full link
    versionLoop = True
    while versionLoop:
        try:
            # provide list to user, let user select version
            i=0
            while i< len(versions):
                print('[' + str(i+1) + '] ' + str(versions[i]))
                i=i+1
            print()
            
            # pyinstaller --onefile or tk.root causes focus to shift from active window
            focus('EscapePodToolkit')

            # select icecast version
            icecastChoice = int(input('Choose Icecast Version: '))
            if 0 < icecastChoice <= len(versions):
                print('Downloading '+str(versions[icecastChoice-1])+'...')
                
                # set target file+directory
                target = os.path.join(path, versions[icecastChoice-1])
                # use icecastVersions for full link
                urlretrieve(icecastVersions[icecastChoice-1], target)
                versionLoop = False
            else:
                print ('Invalid selection.  Please use a number in the list.')
                sleep(1)
                pass

        except (IndexError, ValueError) as e: # input error handling, can print(e) if required
            print()
            print ('Invalid selection.  Please use a number in the list.')
            sleep(1)

    print('Complete.')
    return target

# Configure Icecast
