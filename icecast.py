from urllib.request import urlretrieve, urlopen
from functions import remoteFileList, wait, sleep, makeDir, focus
import os, ssl

# getIcecast
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
        if 'icecast2_' not in file:
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
                # get around SSL failures
                ssl._create_default_https_context = ssl._create_unverified_context
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
def icecastXml(djName):
    #set password for icecast services
    icecastPassword='escapepod'
    # Read in the XML
    with open ('C:\Program Files (x86)\Icecast\icecast.xml', 'r') as file:
        filedata = file.read()

    # Replace target parts
    # does this work without wilcard for values - might need to use re.sub (as per traktorSettings.py)
    filedata = filedata.replace('<source-password>hackme</source-password>', f'<source-password>{icecastPassword}</source-password>')
    filedata = filedata.replace('<relay-password>hackme</relay-password>', f'<relay-password>{icecastPassword}</relay-password>')
    filedata = filedata.replace('<admin-password>hackme</admin-password>', f'<admin-password>{icecastPassword}</admin-password>')
    filedata = filedata.replace('<location>Earth</location>', f'<location>{djName}</location>')
    filedata = filedata.replace('<admin>icemaster@localhost</admin>', '<admin>the.escape.bot@gmail.com</admin>')

    # Write over the XML with new data
    with open('C:\Program Files (x86)\Icecast\icecast.xml', 'w') as file:
        file.write(filedata)
    return icecastPassword
        

# '<source-password>hackme</source-password>', '<source-password>escapepod</source-password>'
# '<relay-password>hackme</relay-password>', '<relay-password>escapepod</relay-password>'
# '<admin-password>hackme</admin-password>', '<admin-password>escapepod</admin-password>'
# '<location>Earth</location>', '<location>DJ?</location>'
# '<admin>icemaster@localhost</admin>', '<admin>the.escape.bot@gmail.com</admin>'