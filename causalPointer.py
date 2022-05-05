#causalPointering system
import time
#queues, checking
from datetime import datetime
from moment import utilities as mu
import stateLib

class queues:
    def __init__(self):
        self.short = []
        self.mid = []
        self.long = []
        self.vlong = []
    def validate(self, id):
        pass
    def state_trig(self, id):
        #check to see if any causalPointers were targeting the triggered state
        #if they were, call validate on them
        svalidated = []
        mvalidated = []
        lvalidated = []
        vlongvalidated = []
        for x in range(0, len(self.short)):
            if self.short[x].statet == id:
                validate(x)
        for x in range(0, len(self.mid)):
            if self.mid[x].statet == id:
                validate(x)
        for x in range(0, len(self.long)):
            if self.long[x].statet == id:
                validate(x)
        for x in range(0, len(self.vlong)):
            if self.vlong[x].statet == id:
                validate(x)
        #initialize new round of causalPointers for every state, for every clock
        self.short.append(id)

    def toss_expired(self):
        #check for expired causalPointers, pop those which are
        for x in range(0, len(self.short)):
            if(self.short[x].expiry):
                pass
        pass




class cPointer:
    def calc_expiry(self, type, dt):
        for x in range(0, len(dt)):
            dt[x] = int(dt[x])
        print(dt)
        print(len(dt))
        dtc = dt

        #constant in minutes
        # * 60
        shorttermconstant = 1
        #in minutes
        # * 60
        midtermconstant = 15
        #in hour
        # * 3600
        longtermconstant = 1
        #in days
        # * 3600*24
        elongtermconstant = 1

        #short term addition
        if(type==0):
            dtc = mu.addTime_seconds(shorttermconstant*60)
        #midterm addition
        if(type==1):
            dtc = mu.addTime_seconds(midtermconstant*60)
        #long term addition
        if(type==2):
            dtc = mu.addTime_seconds(longtermconstant*3600)
        #v long term addition
        if(type==3):
            dtc = mu.addTime_seconds(elongtermconstant*3600*24)
        return(dtc)

    def __init__(self, states, statet, type):
        #passed constructors
        #states = index of state start
        #statet = index of state targeted by causalPointer
        #if statet is triggered, close causalPointer validating minimum clock that satisifies time passed
        self.states = states
        self.statet = statet
        self.type = type
        #time
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        d_list =  [now.strftime("%d"),now.strftime("%m"),now.strftime("%Y"),now.strftime("%H"),now.strftime("%M"),now.strftime("%S")]

        self.conception = dt_string
        #calculate expiry
        self.expiry = self.calc_expiry(self.type, d_list)
        #print causalPointer creation
        print("At time " + dt_string + " state " + str(states) + " triggered, causalPointer created targeting "+ str(statet) + ". Expiry: " + str(self.expiry))
