#dateLib.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#converts seconds to minutes
def secToMin(second):
    return(second / 60)

#converts minutes to hours
def minToHour(min):
    return(min / 60)

#get current time
def getNow():
    d = datetime.now()
    return(dtToList(d))

#normal time to military
def normtomil(d):
    if("P" in d):
        base = 12
    else:
        base = 0
    d0 = d.split(":")[0]
    d0 = int(d0) + base
    d2 = str(d0) + ":" + d.split(":")[1]
    d2 = d2.split(" PM")[0]
    return(str(d2))

#military time to normal time
def miltonorm(d):
    d0 = d.split(":")[0]
    if(int(d0)>12):
        appval = "PM"
    if(int(d0)<12):
        appval = "AM"
    d0 = int(d0) % 12
    d2 = str(d0)+d.split(":")[1]
    return(str(d))

#agenda to date list
def agendaToDateList(timestr, datestr):
    d = getNow()
    timestr = normtomil(timestr)
    #THERE IS A BUG HERE BUT IT WON"T IMPACT ME UNTIL LATE DECEMBER / JANUARY
    #super buggy in september
    return([int(datestr.split("/")[1]),int(datestr.split("/")[0]),int(d[2]),int(timestr.split(":")[0]),int(timestr.split(":")[1]),0])

# date time to list
def dtToList(d):
    return([d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")])

#add time in seconds from now, only takes seconds
def addTime_seconds(second):
    sec = timedelta(seconds=second)
    d = datetime.now() + sec
    now = datetime.now()
    now_list = dtToList(now)
    d_list =  dtToList(d)
    return([now_list, d_list])

#gets then, returns a second countdown
def secondCountdown(then):
    current=getNow()
    if(current==then):
        return(0)
    for x in range(0, len(then)):
        then[x] = int(then[x])
    if(then[3]==24):
        then[3]=0
    td = datetime(then[2], then[1], then[0], then[3], then[4], then[5])
    td2 = datetime.now()
    td3 = td-td2
    td3 = td3.total_seconds()
    return(td3)

#determines if a timeList is past due
def isLate(timeList):
    if(secondCountdown(timeList)<0):
        return(True)
    else:
        return(False)

class temporal_object:
    def __init__(self):
        self.time_object = None
