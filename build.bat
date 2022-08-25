@echo off

rmdir /s /q __pycache__
rmdir /s /q build
rmdir /s /q dist
del *.spec

pyinstaller --onefile --name=EscapePodToolkit --icon=icon.ico setup.py