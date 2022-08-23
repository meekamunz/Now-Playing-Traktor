from urllib.request import urlretrieve
from functions import remoteFileList, wait, sleep
import os

def getIcecast(tempLocation):
    # create a sub folder to tempLocation
    path = os.path.join(tempLocation, 'Icecast')
    os.mkdir(path)

    # get list of versions of Icecast and sort
    print('Getting Icecast versions...')
    url = 'https://downloads.xiph.org/releases/icecast'
    ext = 'exe'
    icecastVersions = []
    #
    # need to strip out url and leave filename
    #
    for file in remoteFileList(url, ext):
        icecastVersions.append(file)
    icecastVersions.sort(reverse=True)
    
    versionLoop = True
    while versionLoop:
        try:
            # provide list to user, let user select version
            i=0
            while i< len(icecastVersions):
                print('[' + str(i+1) + '] ' + str(icecastVersions[i]))
                i=i+1
            print()

            icecastChoice = int(input('Choose Icecast Version: '))
            if 0 < icecastChoice <= len(icecastVersions):
                print('Downloading '+str(icecastVersions[icecastChoice-1])+'...')
                #
                # need to set download location
                #
                urlretrieve(icecastVersions[icecastChoice-1])
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

    # configure Icecast?