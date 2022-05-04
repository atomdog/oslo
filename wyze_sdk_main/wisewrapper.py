#wisewrapper.py
import os
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError



class lights_ww:
    def __init__(self, email, password):
        self.client = Client(email=email, password=password)
        self.appliance_list = {}
        self.bulblist = []
        self.returnablestatus = []
        try:
            response = self.client.devices_list()
            for device in self.client.devices_list():
                self.appliance_list[device.mac] = [device.nickname, device.is_online, device.product.model]
        except WyzeApiError as e:
            print(f"Got an error: {e}")
        self.bulbs()
    def bulbs(self):
        for key in self.appliance_list:
            try:
                self.bulblist.append(self.client.bulbs.info(device_mac=key))
                c = len(self.bulblist)-1
                self.returnablestatus.append([self.bulblist[c].is_on,self.bulblist[c].is_online])
                #print(f"power: {self.bulblist[c].is_on}")
                #print(f"online: {self.bulblist[c].is_online}")
                #print(f"temp: {self.bulblist[c].color_temp}")
                #print(f"color: {self.bulblist[c].color}")
            except WyzeApiError as e:
                # You will get a WyzeApiError if the request failed
                print(f"Got an error: {e}")
    def brightness(self, index, x):
        pm = self.appliance_list[self.bulblist[index].mac][2]
        self.client.bulbs.set_brightness(device_mac=self.bulblist[index].mac, device_model=pm , brightness=x)
    def color(self, index, x):
        pm = self.appliance_list[self.bulblist[index].mac][2]
        self.client.bulbs.set_color(device_mac=self.bulblist[index].mac, device_model=pm , color=x)
    def temp(self, index, x):
        pm = self.appliance_list[self.bulblist[index].mac][2]
        self.client.bulbs.set_color_temp(device_mac=self.bulblist[index].mac, device_model=pm , color_temp=x)
    def off(self, index):
        pm = self.appliance_list[self.bulblist[index].mac][2]
        self.client.bulbs.turn_off(device_mac=self.bulblist[index].mac, device_model=pm)
    def on(self, index):
        pm = self.appliance_list[self.bulblist[index].mac][2]
        self.client.bulbs.turn_on(device_mac=self.bulblist[index].mac, device_model=pm)
    def all_on(self):
        for x in range(0, len(self.bulblist)):
            self.on(x)
    def all_off(self):
        for x in range(0, len(self.bulblist)):
            self.off(x)
    def all_color(self, color):
        for x in range(0, len(self.bulblist)):
            self.color(x, color)
    def all_temp(self, temp):
        for x in range(0, len(self.bulblist)):
            self.temp(x, temp)
    def all_brightness(self, bright):
        for x in range(0, len(self.bulblist)):
            self.brightness(x, bright)
