import socket
import time
from smtplib import SMTP_SSL, SMTP_SSL_PORT
from imap_tools import MailBox, AND
import email
import credLib
from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import html2text
import wikipedia
import speechLib
import roku
import shodan
import os
import json
#import speedtest as st
from roku import Roku
from mac_vendor_lookup import MacLookup
import icloudaccess
#def check_ispeed():
#    test = st.Speedtest()
#    down = test.download()
#    up   = test.upload()
#    return([down/(1024*1024), up/(1024*1024)])
def networkscan():
    devices = []
    for device in os.popen('arp -a'):
        devices.append(device)
    return(devices)
def checkemail():
    inbox = []
    with MailBox('imap.gmail.com').login(credLib.returnbykey('email','emailU'), credLib.returnbykey('email','emailP'), 'INBOX') as mailbox:
    # get unseen emails from INBOX folder
        for msg in mailbox.fetch(AND(seen=False)):

            mtext = msg.html
            b = mtext.find("<td>")
            e = mtext.find("</td>")
            mtext = mtext[b+4:e]
            cutter = False
            counter = -1
            unpad = len(mtext)-48
            mtext = mtext.replace("\n", "")
            mtext = mtext.replace("\r", "")
            mtext = mtext.lstrip()
            mtext = mtext.rstrip()
            inbox.append([msg.from_values["email"], mtext])
            print(inbox)
    return(inbox)
def send(text, endpoint):
    SMTP_HOST = 'smtp.gmail.com'
    SMTP_USER = credLib.returnbykey('email','emailU')
    SMTP_PASS = credLib.returnbykey('email','emailP')
    from_email = credLib.returnbykey('email','emailU')  # or simply the email address
    to_emails = endpoint
    print("Sending: " + text + " to " + endpoint)
    email_message = text
    smtp_server = SMTP_SSL(SMTP_HOST, port=SMTP_SSL_PORT)
    #smtp_server.set_debuglevel(1)  # Show SMTP server interactions
    smtp_server.login(SMTP_USER, SMTP_PASS)
    smtp_server.sendmail(from_email, to_emails, email_message)
    smtp_server.quit()

    return("COMP")
def sendUDP(ip, message):
    UDP_IP = "155.41.60.87"
    if(ip != ""):
        UDP_IP = ip
    UDP_PORT = 5005
    MESSAGE = message
    sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    return("COMP")

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
def getHeadlines():
    headlines = []
    url = "https://www.reuters.com/world"
    req = Request(url, headers ={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    webpage= str(webpage)
    webpage = html2text.html2text(webpage)
    print(webpage)
    for x in range(0, 11):
        x = webpage.find('class="MediaStoryCard__playlist___3Zn6uF story-card"')
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
def toggle_diffuser(state):
    if(state=="off"):
        sendUDP("alfred-server.local", "30")
        return("COMP")
    if(state=="on"):
        sendUDP("alfred-server.local", "31")
        return("COMP")
def toggle_fancy_lamp(state):
    if(state=="off"):
        sendUDP("alfred-server.local", "03")
        return("COMP")
    if(state=="on"):
        sendUDP("alfred-server.local", "13")
        return("COMP")
def summarize(endpoint):
    return(wikipedia.summary(endpoint))

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



def shodanHostQuery(host):
    SHODAN_API_KEY = "Uw6GbgsWH9CmLSUapnH6VYEhkJirdoY7"
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

def bigBrother(distance):
    necessary = False
    cLoc = icloudaccess.getLocation()
    if(distance == None):
        distance = 0.01549275362
    if(cLoc !=None):
        incidents = get_incidents(cLoc['latitude'], cLoc['longitude'], distance)
        string = "Nearby Incidents: \r\r\n"
        now = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime())
        for x in range(0, len(incidents)):
            if now[0:10] == incidents[x][1][0:10]:
                string += " " + incidents[x][1] + "    " + incidents[x][0] + "\r\r\n"
                print(string)
                necessary = True
        if(necessary):
            send(string, "8438197750@mms.att.net")


def track_phone():
    cLoc = icloudaccess.getLocation()
    return([cLoc['latitude'], cLoc['longitude']])

def get_webcams(lat, long, radius):
    #radius in kilometers
    url = "https://api.windy.com/api/webcams/v2/list/nearby="
    url += lat+","+long+","+radius
    headers = {
        'x-windy-key': "SpRGv9uv6toyNNavXR0nMHuADibnKFqw"
        }
    response = requests.request("GET", url, headers=headers)
    return(response.text)

def get_web_image(id):
    url = "https://api.lookr.com/embed/player/" + id + "/live"
    response = requests.request("GET", url)
    return(response)


#simplisafe jam for band
