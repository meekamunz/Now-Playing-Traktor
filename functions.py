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
    subprocess.run([file], shell=True)
    # switch focus to the app
    # need threading?
    # split the path/file to get the filename
    name = file.split('/')[-1]
    focus(name)
    print(f'{file} installed.')

# switch Windows focus
def focus(windowName):
    titles = gw.getAllTitles()
    search = re.compile(windowName+'.')
    match = [string for string in titles if re.match(search, string)]
    window = gw.getWindowsWithTitle(match[0])[0]
    window.restore()