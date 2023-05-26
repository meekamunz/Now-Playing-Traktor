from functions import yesNo
import re, tempfile, os


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




# testpath
testpath='C:\\Users\\meeka\\Documents\\temp\\Traktor Settings.tsi'
# read Traktor Settings.tsi and overwrite
def TraktorSettings(traktorSettingsFile, djName, icecastIP, icecastPassword):
    # create a tempfile
    tempPath = tempfile.gettempdir()
    with open(f'{tempPath}\Traktor Settings.tsi', 'w', encoding="utf-8'") as newfile:
        # Read in the XML
        with open (traktorSettingsFile, 'r') as file:
            # create list of replacement searches (oldData)
            oldData=[]
            oldData+=['<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Bitrate" Type="1" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.MountPath" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Password" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Port" Type="1" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Samplerate" Type="1" Value="(.*)"></Entry>']
            newData=[]
            newData+=[f'<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="{djName} - The Escape Pod"></Entry>', f'<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="{icecastIP}"></Entry>', '<Entry Name="Broadcast.IcecastServer.Bitrate" Type="1" Value="192000"></Entry>', f'<Entry Name="Broadcast.IcecastServer.MountPath" Type="3" Value="{djName}.ogg"></Entry>', f'<Entry Name="Broadcast.IcecastServer.Password" Type="3" Value="{icecastPassword}"></Entry>', '<Entry Name="Broadcast.IcecastServer.Port" Type="1" Value="8000"></Entry>', '<Entry Name="Broadcast.IcecastServer.Samplerate" Type="1" Value="44100"></Entry>'] # TODO: get data for value    
            print('Writing new data to \'Traktor Settings.tsi\'...')
            i=0
            #while i<len(oldData):
            for line in file:
                # search for matching lines, replace with data
                if i < len(oldData):
                    # if old data at position i matches the current line
                    if re.compile(oldData[i]).match(line):
                        # replace old data at position i with new data at postion i
                        line=(re.sub(oldData[i], newData[i], line))
                        i=i+1
                newfile.write(line)
            file.close()
    newfile.close()
    # remove the old file and replace with the temp
    os.replace(tempPath+'\\Traktor Settings.tsi', traktorSettingsFile)
    # remove the temp file
    os.remove(newfile)

TraktorSettings(testpath, 'a DJ', '192.168.1.254', 'my_password')

# file permission error