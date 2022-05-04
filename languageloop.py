#language loop


#main.py
#import I
#import pprofile
#import actions
#import ticket
import textflow
import audiocortex
import causal_model
import os
import re
import time
import sys
import profLib
sys.path.insert(0, './Language')
import spacyGenerator

#checks, field all info, push inputs to causal_model, return path, enact target function

#Initializing speech2text generator

class language_loop:

    def __init__(self):
        print("< ------- Text Flow Initializing ------ >")
        self.flow = textflow.stream().routine()
        self.seg_s = spacyGenerator.docprocgen()
        self.directory = profLib.profiles()
        while(next(self.flow)!=True):
            time.sleep(0.1)
        while(next(self.seg_s)!=True):
            time.sleep(0.1)
        print("< ------- Text Flow Online ------ >")
    def read_complete_audio_cortex(self):
        fullcontents = audiocortex.dump_text()
        spkcontents = audiocortex.dump_sfp()
        for x in range(0, len(fullcontents)):
            self.flow.send([spkcontents[x][0], fullcontents[x][0]])
        #while(True):
        #    f = input()
        #    self.flow.send([f, None])
    def process_file(self, fp):
        file = open(fp, 'r')
        Lines = file.readlines()
        count = 0
        currtot = []
        for line in Lines:
            curr = line
            count += 1
            curr = curr.lower()
            currtot.append(curr)
        currtot = " ".join(currtot)
        #next(self.seg_s)
        file.close()
        currtot = self.seg_s.send(currtot)
        if(currtot!=None):
            for x in range(0, len(currtot)):
                next(self.flow)
                name = str(fp.split('fp'))
                L = self.flow.send([name, str(currtot[x])])

    def update_knowledge_base(self):
        q = os.listdir("Language/corpora/knowledge_base/")
        q = sorted(q)
        for file in q:
            if file.endswith(".txt"):
                next(self.seg_s)
                self.process_file(os.path.join("Language/corpora/knowledge_base/", file))

    #IMPLEMENT TO CONNECT
    def read_perception():
        pass

    def topdown(self, comm):
        next(self.flow)

    def read_key_input(self):
        while(True):
            next(self.flow)
            print("<- DEBUG LANGUAGE MODEL ACCESS CONSOLE ->")
            f = input()
            L = self.flow.send(["Aidan", str(f)])
            #print(L)

    def feed(self, spk, txt):
        next(self.flow)
        replaced_id = self.directory.piece_to_id(spk)
        if(replaced_id != -1):
            spk = replaced_id
        response = self.flow.send([spk, txt])
        return(response)

#q = language_loop()
#q.update_knowledge_base()
#q.read_key_input()
