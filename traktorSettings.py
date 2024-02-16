from functions import yesNo, open_file_dialog
import re, tempfile, os, logger_config

# Logging Configuration
logger_config.configure_logging() 

import logging

# need to tell user to set Traktor settings for either local or remote streaming

# first question, does the user have Traktor on the local PC?


# traktor settings
# location=%userprofile%\\Documents\\Native Instruments\\Traktor <version_number>
# sometimes Windows is a cunt; the Documents folder might be under a OneDrive location

# traktorMachine
def traktorMachine():
    # Ask the user where has Traktor installed - local PC or other PC?
    if yesNo('Is Traktor installed on this PC?', default='yes') == True: location = 'local'
    else: location = 'remote'
    return location

# check TSI file
def check_tsi_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if '<TraktorSettings>' in line:
                return True
    return False

# remote TSI
def remoteTSI(djName, icecastIP, icecastPassword):
    # not yet done!!
    return False, 'INFORMATION: Feature incomplete, refer to instructions below:'

# local option
def localTSI(djName, icecastIP, icecastPassword):
    file_types = [("Traktor Settings files", "*.tsi"), ("All files", "*.*")]
    tsiFile=open_file_dialog(file_types, "Select your Traktor Settings file...")
    if tsiFile:
        # is this a Traktor TSI file?
        ok_to_update = check_tsi_file(tsiFile)
        if ok_to_update:
            # got the file and it is a Traktor TSI file, now update the file
            TraktorSettings(tsiFile, djName, icecastIP, icecastPassword)
            return True, 'Finished editing \'Traktor Settings.tsi\'.'
        else: return False, 'ERROR: This is not a Traktor Settings file!'
    else: return False, 'ERROR: No TSI file found.'

# testpath
testpath='C:\\Users\\meeka\\Documents\\temp\\Traktor Settings.tsi'
# read Traktor Settings.tsi and overwrite
def TraktorSettings(traktorSettingsFile, djName, icecastIP, icecastPassword):
    # create a tempfile
    tempPath = tempfile.gettempdir()
    with open(f'{tempPath}\\Traktor Settings.tsi', 'w', encoding="utf-8'") as newfile:
        # Read in the XML
        with open (traktorSettingsFile, 'r') as file:
            # create list of replacement searches (oldData)
            oldData=[]
            oldData+=['<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Bitrate" Type="1" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.MountPath" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Password" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Port" Type="1" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Samplerate" Type="1" Value="(.*)"></Entry>']
            newData=[]
            newData+=[f'<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="{djName} - The Escape Pod"></Entry>', f'<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="{icecastIP}"></Entry>', '<Entry Name="Broadcast.IcecastServer.Bitrate" Type="1" Value="192000"></Entry>', f'<Entry Name="Broadcast.IcecastServer.MountPath" Type="3" Value="{djName}.ogg"></Entry>', f'<Entry Name="Broadcast.IcecastServer.Password" Type="3" Value="{icecastPassword}"></Entry>', '<Entry Name="Broadcast.IcecastServer.Port" Type="1" Value="8000"></Entry>', '<Entry Name="Broadcast.IcecastServer.Samplerate" Type="1" Value="44100"></Entry>'] # TODO: get data for value    
            logging.info('Writing new data to \'Traktor Settings.tsi\'...')
            i=0
            #while i<len(oldData):
            for line in file:
                # search for matching lines, replace with data
                if i < len(oldData):
                    # if old data at position i matches the current line
                    if re.compile(oldData[i]).match(line):
                        # replace old data at position i with new data at postion i
                        line=(re.sub(oldData[i], newData[i], line))
                        logging.info(f'Setting :{newData[i]} in {traktorSettingsFile}...')
                        i=i+1
                newfile.write(line)
            file.close()
    newfile.close()
    # remove the old file and replace with the temp (replace removes from source location, so no need to remove)
    os.replace(tempPath+'\\Traktor Settings.tsi', traktorSettingsFile)