import socket
import time
from smtplib import SMTP, SMTP_SSL, SMTP_SSL_PORT
import smtplib, ssl
from imap_tools import MailBox, AND
import email
import credLib
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import html2text
import wikipedia
import roku
import shodan
import os
import json
from email.message import EmailMessage
from roku import Roku
from mac_vendor_lookup import MacLookup
import icloudaccess
import sys
from pygooglenews import GoogleNews
#screen /dev/cu.raspberrypi-SerialPort 115200
sys.path.insert(0, './wyze_sdk_main')
sys.path.insert(0, './gmailapi')
import wisewrapper
import gmailfunctions


#network functions
def networkscan():
    devices = []
    for device in os.popen('arp -a'):
        devices.append(device)
    return(devices)

def sendUDP(ip, message):
    UDP_IP = "127.0.0.1"
    if(ip != ""):
        UDP_IP = ip
    UDP_PORT = 5005
    MESSAGE = message
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    return("COMP")

def TV_SCAN():
    return(Roku.discover())

def TV_POWR(TV):
    roku = Roku(TV)
    #print(roku)
    roku.power()
    return("COMP")

def TV_APP_INIT(TVIP):
    roku = Roku(TVIP)
    applist = roku.apps
    return(applist)

def TV_SEARCH(TVIP, APPSTRING):
    roku = Roku(TVIP)
    roku.search()
    retval = roku.literal(APPSTRING)

#end network functions

#weather functions
def getCurrentTemp(state,city):
    url = "https://www.wunderground.com/weather/us/" + state + "/" + city
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage= str(webpage)
    y = (webpage.find('wu-value-to" style="color:#feae3c;">'))
    z = len('wu-value-to" style="color:#feae3c;">')+y
    webpage = webpage[z:]
    y2 = webpage.find('</span>&nbsp;<span _n')
    currenttemp=webpage[y2-2:y2]
    return(currenttemp)

def getPrecipitation(state,city):
    url = "https://www.wunderground.com/precipitation/us/" + state + "/" + city
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage= str(webpage)
    x = webpage.find('class="statement-text"')
    x = x + 23
    webpage=webpage[x:]
    y = webpage.find("</span>")
    webpage = webpage[:y]
    return(webpage)
#end weather functions

#communications
def getMail():
    mail = gmailfunctions.readMail(credLib.returnbykey("email","emailU"))
    return(mail)
def sendTextMail(message, endpoint):
    return(gmailfunctions.sendTextMail(message,endpoint, credLib.returnbykey("email","emailU")))
#end communications

#news and queries
def brokengetHeadlines():
    headlines = []
    url = "https://www.reuters.com/world/"
    req = Request(url, headers ={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage= str(webpage)
    webpage = html2text.html2text(webpage)
    for x in range(0, 11):
        x = webpage.find('media-story-card')
        webpage = webpage[x+len('class="MediaStoryCard__playlist___3Zn6uF story-card"')+1:]
        f = webpage
        findex = f.find('</span>')
        f = f[:findex]
        f = f.replace("\\n", "")
        f = f. replace("&#x27", "")
        f = f. replace(";", "")
        f = f.replace("\\t", "")
        f = f.replace("\\xe2", "")
        f = f.replace("\\x99s", "")
        f = f.replace("x99", "")
        f = f.replace("x98", "")
        f = f.replace("\\x80", "")
        f = f.replace("\\", "")
        f = f.replace("\\n", "")
        f = f.replace("\\t", "")
        webpage = webpage[findex:len(webpage)]
        headlines.append(f)
    return(headlines)
def getHeadlines():
    gn = GoogleNews(lang = 'en', country = 'US')
    top = gn.top_news()
    return(top)
def summarize(endpoint):
    return(wikipedia.summary(endpoint))

#end news and queries

def shodanHostQuery(host):
    SHODAN_API_KEY = ""
    api = shodan.Shodan(SHODAN_API_KEY)
    host = api.host(host)
    # Print general info
    print("""IP: {}Organization: {}Operating System: {}""".format(host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))
    for item in host['data']:
        print("""
                Port: {}
                Banner: {}
        """.format(item['port'], item['data']))
        # Print all banners


#locale functions
#distance = 0.01549275362

def latlonglookup(lat,long):
    us_state_to_abbrev = {"Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR","California": "CA","Colorado": "CO","Connecticut": "CT","Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID","Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS","Kentucky": "KY","Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS","Missouri": "MO","Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York": "NY","North Carolina": "NC","North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC","South Dakota": "SD","Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV","Wisconsin": "WI","Wyoming": "WY","District of Columbia": "DC","American Samoa": "AS","Guam": "GU","Northern Mariana Islands": "MP","Puerto Rico": "PR","United States Minor Outlying Islands": "UM","U.S. Virgin Islands": "VI"}
    print(str(lat))
    print(str(long))
    response = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/"+str(long)+","+str(lat)+".json?limit=1&types=country%2Cregion%2Caddress%2Cplace%2Clocality%2Cpoi&language=en&access_token=pk.eyJ1IjoiY2xlb21hcCIsImEiOiJjbDF0cjN0ZmswNGRtM2pwYWJmcnBxNnRuIn0.PI9vXaY42dMAGkNU0JBBWA")
    address = response.json()['features'][0]['place_name_en']
    for key in us_state_to_abbrev:
        if(key in address):
            address = address.replace(key, us_state_to_abbrev[key])
    print(address)
    addressfirst = address.split(",")
    country = addressfirst[len(addressfirst)-1]
    statezipsplit = addressfirst[len(addressfirst)-2].split(" ")
    print(statezipsplit)
    faddress = addressfirst[0], addressfirst[1].replace(" ", ""), statezipsplit[1].replace(" ", ""), statezipsplit[2].replace(" ", ""), country
    return(faddress)
    #print(response.content['features']['place_name_en'])

def load_map(lat, long, zoom):
    response = requests.get("https://api.mapbox.com/styles/v1/cleomap/cl1tw9s9n002t14r6mu7t1b3v/static/"+str(long)+","+str(lat)+","+str(zoom)+",0/300x300@2x?access_token=pk.eyJ1IjoiY2xlb21hcCIsImEiOiJjbDF0cjN0ZmswNGRtM2pwYWJmcnBxNnRuIn0.PI9vXaY42dMAGkNU0JBBWA")
    from io import BytesIO
    from PIL import Image
    img = Image.open(BytesIO(response.content))
    img.show()
def get_incidents(lat, long, radius):
    incidents = []
    url = "https://citizen.com/api/incident/trending?lowerLatitude=" + str(lat-radius) + "&lowerLongitude=" + str(long-radius) + "&upperLatitude=" + str(lat+radius) + "&upperLongitude=" + str(long+radius)+ "&fullResponse=true&limit=20"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req)
    data = json.loads(webpage.read().decode(webpage.info().get_param('charset') or 'utf-8'))
    for i in data["results"]:
        text = i["raw"]
        timestamp = i["ts"]
        rawloc = i["rawLocation"]
        lat = i["latitude"]
        long = i["longitude"]
        severity = i["severity"]
        key = i["key"]
        police = i["police"]
        timestamp = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(timestamp/1000))
        incidents.append([text, timestamp, rawloc, lat, long, severity, key, police])
    return(incidents)

def get_atlas_obscura(lat,long,page):
    areas_of_interest = {}
    url = "https://www.atlasobscura.com/search?utf8=%E2%9C%93&q=&location=&nearby=true&lat="+str(lat)+"&lng="+str(long)+"&page="+str(page)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage= str(webpage, 'utf-8')

    webpage = html2text.html2text(webpage)
    webpage = webpage[webpage.find('Nearby Places'):webpage.find("#### Get Our Email Newsletter")]
    webpage = webpage[webpage.find('######'):]
    invariant = False
    intervals = []
    webslice = webpage
    x = 0
    while(invariant==False):
        if(webslice.find('######',x+1)==-1):
            invariant=True
        else:
            #slice up webpage and pull the pieces
            slice_interval_a = webslice.find('######',x)
            slice_interval_b = webslice.find('######',x+1)
            intervals.append(webslice[slice_interval_a:slice_interval_b])
            webslice=webslice[slice_interval_b:]
            #flesh out the intervals into areas of interest
            #take title
            select_from_intervals = intervals[len(intervals)-1]
            title_start = select_from_intervals.find('######')+6
            title_end = select_from_intervals.find('\n')+2
            title = select_from_intervals[title_start+1:title_end]
            title = title.rstrip("\n")
            areas_of_interest[title]={}
            #cut title
            select_from_intervals[select_from_intervals.find(title)+len(title):]
            #take url
            #print(select_from_intervals)
            url_start = select_from_intervals.find("/places/")
            url_end = select_from_intervals.find(")")
            url = select_from_intervals[url_start:url_end]
            urlsaver = url
            url = "https://www.atlasobscura.com" + url.replace("\n", '')
            areas_of_interest[title]["url"]=url
            #collect more information
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            current_page = urlopen(req).read()
            current_page= str(current_page, 'utf-8')
            current_page = html2text.html2text(current_page)
            #print(current_page)
            print("============================")
            c_slice_interval_a = current_page.find(title)
            current_page = current_page[c_slice_interval_a:]
            c_slice_interval_a = current_page.find("* * *",3)
            c_slice_interval_b = current_page.find("Near This Place")
            current_page = current_page[c_slice_interval_a:c_slice_interval_b]
            c_slice_interval_a=current_page.find("[See All _ _ ]")
            c_slice_interval_b=current_page.find("View on Google Maps")
            current_page = current_page[c_slice_interval_a:c_slice_interval_b]
            c_slice_interval_a=current_page.find(")")+1
            c_slice_interval_b = current_page.find("######")
            description = current_page[c_slice_interval_a:c_slice_interval_b]
            print(title)
            print("      ")
            print(current_page)
            print("============================")


def track_device(device_index):
    cLoc = icloudaccess.getLocation(device_index)
    return([cLoc['latitude'], cLoc['longitude']])
def get_device_info(device_index):
    return(icloudaccess.get_status(device_index))
def get_devices():
    return(icloudaccess.get_devices())
#end locale functions


#home functions
#[B0,B1,B2,...,Bn]
#[on/off, color, brightness, temp]
def wyze_command(command):
    if(credLib.returnbykey('wyze', 'email')!="" and credLib.returnbykey('wyze', 'password')!=""):
        client = wisewrapper.lights_ww(email=credLib.returnbykey('wyze', 'email'), password=credLib.returnbykey('wyze', 'password'))
        for x in range(0, len(command_list)):
            if(command[x]=='off'):
                client.all_off()
            if(command[x]=='on'):
                client.all_on()


#end home functions
def testbench():
    #returns a list of devices
    print(networkscan())
    print("##################")
    print("##################")
    #should return an int
    print(getCurrentTemp("MA", "Brookline"))
    print("##################")
    print("##################")
    #should return a string
    print(getPrecipitation("MA", "Brookline"))
    print("##################")
    print("##################")
    #should return device list
    device_list = get_devices()
    print(device_list)
    print("##################")
    print("##################")
    for x in range(0, len(device_list)):
            #should return information json
            location = track_device(x)

            print(location)
            #should return lat long
            print(get_device_info(x))
            print(latlonglookup(location[0], location[1]))
            load_map(location[0], location[1], 15)
            print("##################")
            print("##################")

#testbench()
#print(getHeadlines())
#get_phone_info()
#get_devices()
#print(getHeadlines())
#location = track_phone()
#print(get_incidents(location[0],location[1],0.01549275362))
#get_atlas_obscura(location[0],location[1],1)
#simplisafe jam for band
