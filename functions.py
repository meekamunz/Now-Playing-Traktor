import msvcrt as m
import os, requests, subprocess, re
import pygetwindow as gw
from time import sleep
from bs4 import BeautifulSoup

#clear screen
def clear():
    os.system('cls')

#wait for key press
def wait():
    m.getch()
    #print('Where\'s the \'Any\' key?')

# check for IPv4 address
def isGoodIPv4(s):
    pieces = s.split('.')
    if len(pieces) != 4: return False
    try: return all(0<=int(p)<256 for p in pieces)
    except ValueError: return False

# get list of files on url
def remoteFileList(url, ext=''):
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').endswith(ext)]

def makeDir(path):
        try:
            os.mkdir(path)
            message = (path+' created.')
            return message
        except OSError:
            message = (path+' already exists.')
            return message

# run a GUI based installer (file) for the user to install
def guiInstaller(file):
    print(f'Installing {file}, please follow on screen instructions...')
    subprocess.Popen([file], shell=True)

    # split the path/file to get the filename
    name = file.split('\\')[-1]
    
    print(f'{file} installed.')

# switch Windows focus
def focus(windowName):
    titles = gw.getAllTitles()
    search = re.compile('.*'+windowName+'.*')
    match = [string for string in titles if re.match(search, string)]
    window = gw.getWindowsWithTitle(match[0])[0]
    # pygetwindow activate the handle is invalid
    window.minimize()
    window.restore()

# get admin privileges
def checkAdmin():
    if os.name == 'nt':
        try:
            # only windows users with admin privileges can read the C:\windows\temp
            temp = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        except:
            return (os.environ['USERNAME'],False)
        else:
            return (os.environ['USERNAME'],True)
    else:
        if 'SUDO_USER' in os.environ and os.geteuid() == 0:
            return (os.environ['SUDO_USER'],True)
        else:
            return (os.environ['USERNAME'],False)