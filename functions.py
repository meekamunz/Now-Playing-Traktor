import msvcrt as m
import os, requests, subprocess, re, ctypes, enum, sys, socket, psutil
import pygetwindow as gw
from time import sleep
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

# check if application (application_name) is running
def is_application_running(application_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'].startswith(application_name):
            return True
    return False

# get local IP address
def get_local_ip_addresses():
    ip_addresses = []
    try:
        # Get all IP addresses associated with the local machine
        host_name = socket.gethostname()
        ip_addresses = socket.getaddrinfo(host_name, None, socket.AF_INET, socket.SOCK_STREAM)
        ip_addresses = [addr[4][0] for addr in ip_addresses]
    except Exception as e:
        print(f'Error getting local IP addresses: {str(e)}')
    return ip_addresses

# choose IP address from a list called 'ip_addresses'
def prompt_select_ip(ip_addresses):
    while True:
        print("Select an IP address:")
        for i, ip in enumerate(ip_addresses):
            print(f"{i + 1}. {ip}")
        choice = input("Enter the corresponding number: ")
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(ip_addresses):
                return ip_addresses[index]
        print("Invalid choice. Please try again.\n")

# open a file of type 'fileType'
def open_file_dialog(file_types, title):
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=file_types, title=title)
    return file_path

# yesNo question
def yesNo(question, default='yes'):
    # Ask a yes/no question via raw_input() and return their answer.
    # 'question' is a string that is presented to the user.
    # 'default' is the presumed answer if the user just hits <Enter>.
    #    It must be 'yes' (the default), 'no' or None (meaning
    #    an answer is required of the user).
    # The "answer" return value is True for 'yes' or False for 'no'.
    
    valid = {'yes': True, 'y': True, 'ye': True,
             'no': False, 'n': False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n')")

# DJ Name
def djName():
    djLoop = True
    while djLoop:
        try:
            illegalChars = [' ', ',', ';', ':', '@', '"', '!', '$', '%', '^', '&', '*', '(', ')', '?', '/', '\\', '|', '`', '\'', '#', '~', '[', ']', '{', '}', '_', '+', '=']
            djName = input('Enter DJ Name: ')
            if any(e in djName for e in illegalChars) == False:
                return djName
            else:
                print('Illegal characters in DJ Name.')
                illegalDj = [e for e in illegalChars if e in djName]
                iDj = ' '.join(illegalDj)
                print(f'{djName} contains: {iDj}')
                print('Replacing illegal characters...')
                for chars in illegalChars:
                    djName = djName.replace(chars, '.')
                return djName
        except Exception as e:
            pass

# clear screen
def clear():
    os.system('cls')

# wait for key press
def wait():
    print('Press any key to continue...')
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

# make a directory
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
    # subprocess.Popen or subprocess.run???
    # use subprocess.run in this instance as we want to wait for application to install
    p = subprocess.run([file], shell=True)
    if p.returncode != 0:
        print(f'Error installing {file}...')
        wait()
    else: print(f'{file} installed.')

# switch Windows focus
def focus(windowName):
    titles = gw.getAllTitles()
    search = re.compile('.*'+windowName+'.*')
    match = [string for string in titles if re.match(search, string)]
    window = gw.getWindowsWithTitle(match[0])[0]
    # pygetwindow activate the handle is invalid
    window.minimize()
    window.restore()

# bootstrap for admin privileges
class SW(enum.IntEnum):

    HIDE = 0
    MAXIMIZE = 3
    MINIMIZE = 6
    RESTORE = 9
    SHOW = 5
    SHOWDEFAULT = 10
    SHOWMAXIMIZED = 3
    SHOWMINIMIZED = 2
    SHOWMINNOACTIVE = 7
    SHOWNA = 8
    SHOWNOACTIVATE = 4
    SHOWNORMAL = 1


class ERROR(enum.IntEnum):

    ZERO = 0
    FILE_NOT_FOUND = 2
    PATH_NOT_FOUND = 3
    BAD_FORMAT = 11
    ACCESS_DENIED = 5
    ASSOC_INCOMPLETE = 27
    DDE_BUSY = 30
    DDE_FAIL = 29
    DDE_TIMEOUT = 28
    DLL_NOT_FOUND = 32
    NO_ASSOC = 31
    OOM = 8
    SHARE = 26

def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))