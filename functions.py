import msvcrt as m
import os, requests, subprocess, re, ctypes, enum, sys, socket, psutil, logger_config, glob
import pygetwindow as gw
from time import sleep
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog

# Logging Configuration
#logger_config.configure_logging() 

import logging

# check if application (application_name) is running
def is_application_running(application_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'].startswith(application_name):
            return True
    return False

# kill application
def kill_process(process_name):
    os.system(f'taskkill /f /im {process_name}')

# get local IP address
def get_local_ip_addresses():
    ip_addresses = []
    try:
        # Get all IP addresses associated with the local machine
        host_name = socket.gethostname()
        ip_addresses = socket.getaddrinfo(host_name, None, socket.AF_INET, socket.SOCK_STREAM)
        ip_addresses = [addr[4][0] for addr in ip_addresses]
    except Exception as e:
        logging.debug(f'Error getting local IP addresses: {str(e)}')
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
                logging.debug('Illegal characters in DJ Name.')
                illegalDj = [e for e in illegalChars if e in djName]
                iDj = ' '.join(illegalDj)
                logging.debug(f'{djName} contains: {iDj}')
                logging.debug('Replacing illegal characters...')
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
    logging.info(f'Installing {file}, please follow on screen instructions...')
    # subprocess.Popen or subprocess.run???
    # use subprocess.run in this instance as we want to wait for application to install
    p = subprocess.run([file], shell=True)
    if p.returncode != 0:
        logging.debug(f'Error installing {file}...')
        wait()
    else: logging.info(f'{file} installed.')

def guiInstaller_pattern(file_pattern):
    logging.info(f'Installing files matching pattern "{file_pattern}", please follow on-screen instructions...')
    files = glob.glob(file_pattern)
    if not files:
        logging.debug(f'No files found matching pattern "{file_pattern}"')
        return
    for file in files:
        logging.info(f'Installing {file}...')
        p = subprocess.run([file], shell=True)
        if p.returncode != 0:
            logging.debug(f'Error installing {file}...')
            wait()
        else:
            logging.info(f'{file} installed.')

# switch Windows focus
def focus(windowName=None):
    try:
        if windowName:
            titles = gw.getAllTitles()
            search = re.compile('.*' + windowName + '.*')
            match = [string for string in titles if re.match(search, string)]
            if match:
                window = gw.getWindowsWithTitle(match[0])[0]
                # pygetwindow activate the handle is invalid
                try:
                    window.minimize()
                    window.restore()
                    logging.info(f'Successfully focused on window: {windowName}')
                except Exception as e:
                    logging.error(f'Error minimizing/restoring window: {e}')
            else:
                logging.debug(f"No window with name '{windowName}' found.")
        else:
            active_window = gw.getActiveWindow()
            if active_window:
                try:
                    active_window.minimize()
                    active_window.restore()
                    logging.info('Successfully focused on active window.')
                except Exception as e:
                    logging.error(f'Error minimizing/restoring active window: {e}')
            else:
                logging.debug("No active window found.")
    except Exception as e:
        logging.error(f'Error in focus function: {e}')


# Create m3u DJ Name file:
def dj_name_playlist(path, name):
    with open(f'{path}\\{name}.ogg.m3u', 'w') as playlist_file:
        print(f'http://127.0.0.1:8000/{name}.ogg')
        playlist_file.close()

# bootstrap for admin privileges
SW_SHOWNORMAL = 1

ERROR_FILE_NOT_FOUND = 2
ERROR_PATH_NOT_FOUND = 3
ERROR_ACCESS_DENIED = 5

def bootstrap():
    """
    Elevates privileges if the script is not already running with administrator rights.
    """
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Try to elevate privileges
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW_SHOWNORMAL
        )
        # Check if elevation failed
        if hinstance <= 32:
            # Raise a RuntimeError with the appropriate error code
            error_code = hinstance if hinstance in [ERROR_FILE_NOT_FOUND, ERROR_PATH_NOT_FOUND, ERROR_ACCESS_DENIED] else 'Unknown error'
            raise RuntimeError(f"Elevation failed. Error code: {error_code}")

        
if __name__ == '__main__':
    print('here')
    logging.debug('testing functions...')
    bootstrap()
    print('working?')
    wait()