#icloud access
from pyicloud import PyiCloudService
import credLib

def getLocation(device_index):
    api = PyiCloudService(credLib.returnbykey("phone", "phoneU"), credLib.returnbykey("phone", "phoneP"))
    return(api.devices[device_index].location())
def get_status(device_index):
    api = PyiCloudService(credLib.returnbykey("phone", "phoneU"), credLib.returnbykey("phone", "phoneP"))
    return(api.devices[device_index].status())
def get_devices():
    api = PyiCloudService(credLib.returnbykey("phone", "phoneU"), credLib.returnbykey("phone", "phoneP"))
    devicelist = []
    for device in api.devices:
        devicelist.append(device)
    return(devicelist)
def play_sound(device_index):
    api = PyiCloudService(credLib.returnbykey("phone", "phoneU"), credLib.returnbykey("phone", "phoneP"))
    counter = 0
    for device in api.devices:
        if device.get('name') == device_index or counter == device_index:
            device.play_sound()
        counter+=1
