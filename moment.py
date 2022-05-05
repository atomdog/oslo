#moment.py
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from recurrent.event_parser import RecurringEvent
import inflect
from word2number import w2n
#timeline [moment0, moment1, ]
class moment:
    def __init__(self):
        self.id = None

        self.mil_hour = None
        self.norm_hour = None

        self.norm_suffix = None
        self.minute = None
        self.second = None

        self.day = None
        self.weekday = None
        self.month = None
        self.year = None

        self.tag = None
        self.text = None
        self.bins = []
        self.drep = {
        'mhour': self.mil_hour,
        'hour': self.norm_hour,
        'suffix': self.norm_suffix,
        "minute": self.minute,
        "second": self.second,
        "day": self.day,
        "weekday": self.weekday,
        "month": self.month,
        "year": self.year}
    def load_from_array(self, array):
        pass

class timeslice:
    def __init__(self):
        self.start_moment = None
        self.end_moment = None

        self.tag = None
        self.text = None


    def inside_bool(self):
        pass

class timeline:
    def __init__(self):
        self.moment_container = []
        self.slices = []

#strings:
#today, tonight, tomorrow, yesterday, last,this,next (M,T,W,T,F,S,S), this morning,

class utilities:
    def __init__(self):
        pass


    def string_to_val(self,strtime):
        print("// moment standardizing: ")
        print(strtime)


        convertibleordinals = {
        "first": "1st",
        "second": "2nd",
        "third": "3rd",
        "fourth": "4th",
        "fifth": "5th",
        "sixth": "6th",
        "seventh": "7th",
        "eighth": "8th",
        "ninth": "9th",
        "tenth": "10th",
        "eleventh": "11th",
        "twelveth": "12th",
        "thirteenth": "13th",
        "fourtheenth": "14th",
        "fifteenth": "15th",
        "sixteenth": "16th",
        "seventeenth": "17th",
        "eighteenth": "18th",
        "nineteenth": "19th",
        "twentieth": "20th",
        "thirtieth": "30th",
        "fortieth": "40th",
        "fiftieth": "50th",
        "sixtieth": "60th",
        "seventieth": "70th",
        "eightieth": "80th",
        "ninetieth": "90th",
        "hundredth": "00th",
        "thousandth": "000th",
        "millionth": "000000th",
        "billionth": "000000000th",
        "trillionth": "000000000000th",
        "quadrillionth": "000000000000000th"
        }
        rn = self.getNow()
        #p = inflect.engine()
        r = RecurringEvent(now_date=datetime.now())

        #combine ordinals etc
        prev = -1
        prevflag = False
        topop = []
        woworked = False
        for x in range(0, len(strtime)):
            prevflag = woworked
            woworked = False
            if(strtime[x] in convertibleordinals):
                if(prev != -1 and prevflag != False):
                    if(prev>=20 and prev<100):
                        strtime[x] = str(prev)[len(str(prev))-2]+convertibleordinals[strtime[x]]
                        topop.append(x-1)
                    if(prev>=100):
                        q = int(convertibleordinals[strtime[x]][0:len(convertibleordinals[strtime[x]])-2])
                        if(q <= 90):
                            strtime[x] = str(prev)[len(str(prev))-3]+convertibleordinals[strtime[x]]
                        topop.append(x-1)
                else:
                    strtime[x] = convertibleordinals[strtime[x]]
            else:
                try:
                    woworked = w2n.word_to_num(strtime[x])
                except:
                    pass
                if(woworked!=False):
                    #print(woworked)
                    strtime[x] = str(woworked)
                    prev = woworked
        for x in range(0, len(topop)):
            strtime.pop(topop[x])


        strtimejoined = " ".join(strtime)

        print("//words to numbers conversion yielded...")
        print(strtimejoined)
        print("//attempting extraction...")
        ext_time = r.parse(strtimejoined)
        #if(ext_time!=None):
            #print(ext_time)
            #print(r.is_recurring)
            #print(r.get_params())
        oplist = []
        print("//moment found:")
        print(r.get_params(), r.is_recurring)
        return(ext_time)

    #converts seconds to minutes
    def secToMin(self,second):
        return(second / 60)

    #converts minutes to hours
    def minToHour(self,min):
        return(min / 60)

    #get current time
    def getWeekday(self, d):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        wd = dt.weekday()
        return(wd)

    def getNow(self):
        d = datetime.now()
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        for x in range(0, len(d)):
            d[x] = int(d[x])
        return(d)

    #normal time to military
    def normtomil(self,d):
        if("P" in d):
            base = 12
        else:
            base = 0
        d0 = d.split(":")[0]
        d0 = int(d0) + base
        d2 = str(d0) + ":" + d.split(":")[1]
        d2 = d2.split(" PM")[0]
        return(str(d2))

    def miltonorm(self,d):
        d0 = d.split(":")[0]
        if(int(d0)>12):
            appval = "PM"
        if(int(d0)<12):
            appval = "AM"
        d0 = int(d0) % 12
        d2 = str(d0)+d.split(":")[1]
        return(str(d))


    def addSeconds(self, t0, s):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        sec = timedelta(seconds=s)
        d = dt + sec
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addMinutes(self, t0, m):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        minutes = timedelta(minutes=m)
        d = dt + minutes
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addHours(self, t0, h):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        hours = timedelta(hours=h)
        d = dt + hours
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addDays(self,t0,D):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        days = timedelta(days=D)
        d = dt + days
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addWeeks(self,t0, w):
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        weeks = timedelta(weeks=w)
        d = dt + weeks
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addMonths(self,t0, M):
        M = M*4
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        weeks = timedelta(weeks=M)
        d = dt + weeks
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

    def addYears(self, t0, Y):
        Y = Y*52
        dt = datetime(t0[2], t0[1], t0[0], t0[3], t0[4], t0[5])
        weeks = timedelta(weeks=Y)
        d = dt + weeks
        d = [d.strftime("%d"),d.strftime("%m"),d.strftime("%Y"),d.strftime("%H"),d.strftime("%M"),d.strftime("%S")]
        return(d)

#mu = utilities()
#sentencetoconvert = ['on', 'feb', '4', 'remind', 'me', 'to', 'feed', 'the', 'dog', 'at', '3:30 PM']
#print(sentencetoconvert)
#mu.string_to_val(sentencetoconvert)
