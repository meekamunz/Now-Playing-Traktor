@echo off

rmdir /s /q __pycache__
rmdir /s /q build
rmdir /s /q dist
del *.spec

pyinstaller --onefile --name=EscapePodToolkit --icon=icon.ico --add-data "icecast.py:." --add-data "nssm.py:." --add-data "winamp.py:." --add-data "amip.py:." --add-data "functions.py:." --add-data "cleanup.py:." --add-data "traktorSettings.py:." --add-data "operateThePod.py:." --add-data "logger_config.py:." --hidden-import urllib.request --hidden-import requests --hidden-import ctypes --hidden-import psutil --hidden-import pickletools --hidden-import bs4 --hidden-import keyboard --hidden-import pywin32 --hidden-import pygetwindow EscapePodToolKit.py