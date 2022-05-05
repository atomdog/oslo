#main.py
#import I
#import pprofile
#import actions
#import ticket


import languageloop
#import audioloop
import causal_model
import ears
import pickle
#import actions
import audiocortex
import actions
#import speechLib
from threading import Thread
import threading
import time
import queue
from datetime import datetime, timedelta
#checks, field all info, push inputs to causal_model, return path, enact target function

#Initializing speech2text generator

class executive_loop:
    def __init__(self):
        print("< ------- Executive Loop intializing... ------ >")
        self.pq = queue.Queue()
        self.cm = causal_model.model()
        self.run()

    def chores(self):
        while(True):
            time.sleep(35)
            print("< ------- Doing Chores ------ >")
            #update some information
            #0.01549275362
            currentlatlong = actions.track_device(0)
            currentaddress = actions.latlonglookup(currentlatlong[0], currentlatlong[1])
            weather = actions.getPrecipitation(currentaddress[2], currentaddress[1])
            collectiontime = datetime.now()
            self.pq.put(["Weather Underground", "The forecast at " + collectiontime.strftime("%H:%M:%S") + " on "+   collectiontime.strftime("%d/%m/%Y") + " is " + weather])
            temp = actions.getCurrentTemp(currentaddress[2], currentaddress[1])
            self.pq.put(["Weather Underground", "The temperature at " + collectiontime.strftime("%H:%M:%S") + " on "+   collectiontime.strftime("%d/%m/%Y") +" is " + temp])
                    #when, from, contents
            #headlines = actions.getHeadlines()
            #for x in range(0, len(headlines)):
            #    self.pq.put(["Reuters", "Today: " + headlines[x]])
            nearbyincidents = actions.get_incidents(currentlatlong[0], currentlatlong[1], 0.01549275362)
            for x in range(0, len(nearbyincidents)):
                self.pq.put(["Citizen", "At " + str(nearbyincidents[x][1]) + " Citizen reported a code " + str(nearbyincidents[x][5])+ " incident: "+ nearbyincidents[x][0]])
            print("< ------- Chores Done ------ >")
            time.sleep(18000)

    def audio(self):
        print("< ------- Loading Audio Loop ------ >")
        print("< ------ Initializing Ear ------ >")
        ear = ears.listen()
        while(next(ear)!=True):
            time.sleep(0.01)
        print("< ------- Loaded Audio Loop ------ >")
        print("< -- Initializing Audio Cortex -- >")
        audcortex = audiocortex.audio_cortex()
        print("< -------- Audio Cortex Loaded ------- >")
        while(True):
            #check for audio
            #fingerprint, text
            current_audio_output = next(ear)
            self.pq.put(current_audio_output)
            audcortex.passIn(current_audio_output[1], current_audio_output[0])
            #next(creng)
            #current_voice_val = creng.send(current_audio_output[0])
    def texts(self):
        while(True):
            #check for texts
            texts = actions.getMail()
            if(len(texts)>0):
                for x in range(0, len(texts)):
                    #when, from, contents
                    self.pq.put([texts[x][1], texts[x][2]])
            time.sleep(1)

    def run(self):
        listen = threading.Thread(target=self.audio,args=())
        text = threading.Thread(target=self.texts,args=())
        chore = threading.Thread(target=self.chores,args=())
        listen.start()
        text.start()
        chore.start()
        print("< ------- Loading Language Loop ------ >")
        lang = languageloop.language_loop()
        print("< -------- Language Loop Loaded ------ >")
        print("< ------- Loading Causal Model ------ >")
        #cm = causal_model.model()
        print("< -------- Causal Model Loaded ------ >")
        print("   ")
        print("   ")
        print("   ")
        print("   ")
        #print("#̷̨͕̝͚̬͋~̷͇͔̿͊̅̓̿̈͗͋#̵̬̭̲̞̺͆͆̄̿͛͐̇͋̎~̴̨̘̔́͑̌#̶̧̡̨̰͉̣̣́͘~̴̡͙̒̎̇̌̃͛ͅ#̷̛̱̰̒̇̋̿͠ ̷̨̨͍̠͎̤͉̱͎̦͆͌̄͊͑͘̚Ê̴̘̬͕̰͔n̴̠̲͈̠̺̥̜̹̙̲̓͆͋̆̉̏͂́͆̂t̶͖͓̪̭͖͕̄é̸̢̯̖̼͇r̷̨̙͓̽̾̿̕ͅí̷͇͙̞͍̘̣̰̠̦̒͂̔n̴̢̮͖̮̦͍̈̍̈͋̂̃͌̚g̷͕͖̟͒̆̈͌͊ ̵̡͎̙̻̰̎́͠T̴̞͖͔̮̿̀͒̆̀̒̊̄̋͠h̷̢̨̨̡͉̹̖̖͚̋̆́ͅe̴̢͚̤̫͍̝̤̠͑̓͒̋͒̕͜͜͠ ̵̬̦̍͂̅͐͝L̵̻̫̯̱͕͗̓̇́͊̚͝ợ̴͙̫̩̽̌̐̊̍̆o̶̢̼̭͎͉͇̭̠̼͗̈́̊͋̒̓ͅp̸̪̖̻̼͕͔̭̮͎̱͐͐ ̶͇̫̣̹̥̖̽͒̉̔̅ͅ#̷̢͆̇̋͊͒̊̕̚~̷̤̗̱̯̘̿͐̃̀͊͝#̵͚̘̼̝̱̼͙̻̘̗͛̑͗̓̾͘͠͝~̵̯̱̖͙̣͌̅̿̓̐̿͝#̶̡̼̬̰͇̙͐̾̈́̅͜~̷̭̼͛̍̇̋̎̌̿͂͊͝#̵̲̙͚̠͍̈́̂͛͜")
        print("   ")
        print("   ")
        print("   ")
        print("   ")
        print("< -------- Entering Executive Loop ------ >")
        while(True):
            #<-input block->

            #<-end input block->

            #<-processing block->

            #language processing
            cur = self.pq.get()
            print(cur)
            if(cur!=False):
                response = lang.feed(cur[0], cur[1])
                answer = response[0]
                commands = response[1]
                print("< -------- Executive Loop Received ------ >")
                print(response)
            #<-end processing block->

            #<-decision block->

            #<-end decision block->

            #<-action block->

            #<-end action block->
        listen.join()
        text.join()
        chore.join()

q = executive_loop()
q.run()
        #listen for sensor info
