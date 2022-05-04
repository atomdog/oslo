# philips-hue-blue
Extremely casual library to control philips hue BLE lights with a raspberry pi + bluez
Quick note: This eliminates the need for a BLE bridge.  Run huep.py to create a 'server' and lightinterface to communicate with that so you don't have to re-pair/connect every time you want to send a command, etc etc. 

# getting things going
import lightinterface into your code and then call sender(a,b,c,d) as you please. async is handled on the other side.
