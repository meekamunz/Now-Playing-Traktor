from functions import yesNo
import re


# need to tell user to set Traktor settings for either local or remote streaming

# first question, does the user have Traktor on the local PC?


# traktor settings
# location=%userprofile%\\Documents\\Native Instruments\\Traktor <version_number>
# sometimes Windows is a cunt; the Documents folder might be under a OneDrive location
# Traktor Settings.tsi
# set these:
# <Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="mike13000 - The Escape Pod"></Entry>
# <Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="192.168.1.180"></Entry>
# <Entry Name="Broadcast.IcecastServer.Bitrate" Type="1" Value="192000"></Entry>
# <Entry Name="Broadcast.IcecastServer.MountPath" Type="3" Value="mike13000.ogg"></Entry>
# <Entry Name="Broadcast.IcecastServer.Password" Type="3" Value="Dookie99"></Entry>
# <Entry Name="Broadcast.IcecastServer.Port" Type="1" Value="8000"></Entry>
# <Entry Name="Broadcast.IcecastServer.Samplerate" Type="1" Value="44100"></Entry>




# traktorMachine
def traktorMachine():
    # Ask the user where has Traktor installed - local PC or other PC?
    if yesNo('Is Traktor installed on this PC?', default='yes') == True: location = 'local'
    else: location = 'remote'
    return location

# read Traktor Settings.tsi and overwrite
def TraktorSettings(path):
    # Read in the XML
    #with open (path, 'r') as file:
    newfile = open('C:\\Users\\meeka\\Documents\\temp\\Traktor Settings_new.tsi', 'w')
    with open('C:\\Users\\meeka\\Documents\\temp\\Traktor Settings.tsi', 'r') as file: # temp for testing
        # create list of replacement searches (oldData)
        oldData=[]
        oldData+=['<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="(.*)"></Entry>', '<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="(.*)"></Entry>']
        newData=[]
        newData+=['<Entry Name="Broadcast.IcecastMetadata.Name" Type="3" Value="your_name_here"></Entry>', '<Entry Name="Broadcast.IcecastServer.Address" Type="3" Value="your_IP_here"></Entry>'] # TODO: get data for value    
        print('Writing new data to \'Traktor Settings.tsi\'...')
        # use a counter for single piece of code
        i=0
        #while i<len(oldData):
        for line in file:
            # search for matching lines, replace with data
            if i < len(oldData):
                if re.compile(oldData[i]).match(line):
                    #print(f'Old data: {line}')
                    line=(re.sub(oldData[i], newData[i], line))
                    i=i+1
            newfile.write(line)
        file.close()
        newfile.close

        # need to replace old with new next
