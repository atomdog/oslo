import numpy as np
import stateLib
import causalPointer
import actions
import agendaLib
import spotifyLib
import perception
import I
#make class!!!! done 

class model():
    def __init__(self):
        self.drives = I.I
        self.tm = []
        self.state_q = 25
        self.total_encountered = 0
        #occurence clone to measure number of occurences
        self.tm_occ_clone = []
        self.causalPointer_stack = causalPointer.queues()
        self.current_state = None
        for x in range(0, self.state_q):
            name = "S"+str(x)
            f = stateLib.state(name, self.state_q)
            self.tm.append(f)
            self.tm_occ_clone.append(np.full((self.state_q, 4), 0, dtype = 'float128'))

    def reload_prob(self):
        total_occur = 0
        for x in range(0, len(tm)):
            for y in range(0, len(tm[x])):
                for z in range(0, len(tm[x][y])):
                    total_occur+=self.tm_occ_clone[x][y][z]
            for y in range(0, len(tm[x])):
                for z in range(0, len[tm[x][y]]):
                    self.tm[x][y][z] = self.tm_occ_clone[x][y][z]/total_occ_clone
            total_occur = 0


    def manual_state_load(self):
        f = lambda a : actions.summarize(a)
        self.tm[0].updateVerbCloud(["find", "read", "look", "tell"])
        self.tm[0].set_target_function(f)
        self.tm[0].name = "summary"
        self.tm[0].isAction = True
        self.tm[0].get_act = True

        f1 = lambda: actions.getHeadlines()
        self.tm[1].updateObjectCloud(["headline", "news"])
        self.tm[1].updateVerbCloud(["get", "read", "tell"])
        self.tm[1].set_target_function(f1)
        self.tm[1].name = "news"
        self.tm[1].isAction = True
        self.tm[1].get_act = True

        f2 = lambda a, b : actions.send(a,b)
        self.tm[2].set_target_function(f2)
        self.tm[2].name = "send"
        self.tm[2].isAction = True


        f3 = lambda: actions.toggle_diffuser("0")
        self.tm[3].updateObjectCloud(["diffuser"])
        self.tm[3].updateVerbCloud(["turn", "switch"])
        self.tm[3].updateDescriptorCloud(["off"])
        self.tm[3].set_target_function(f3)
        self.tm[3].name = "disable diffuser"
        self.tm[3].isAction = True

        f4 = lambda: actions.toggle_diffuser("1")
        self.tm[4].updateObjectCloud(["diffuser"])
        self.tm[4].updateVerbCloud(["turn", "switch"])
        self.tm[4].updateDescriptorCloud(["on"])
        self.tm[4].set_target_function(f4)
        self.tm[4].name = "diffuser"
        self.tm[4].isAction = True

        f5 = lambda: actions.getPrecipitation("sc", "charleston")
        self.tm[5].updateObjectCloud(["weather"])
        self.tm[5].updateVerbCloud(["read", "tell", "whats"])
        self.tm[5].set_target_function(f5)
        self.tm[5].name = "weather"
        self.tm[5].isAction = True
        self.tm[5].get_act = True

        f6 = lambda a, b: actions.getCurrentTemp(a, b)
        self.tm[6].updateObjectCloud(["temperature"])
        self.tm[6].updateVerbCloud(["read", "tell", "whats"])
        self.tm[6].set_target_function(f6)
        self.tm[6].name = "temperature"
        self.tm[6].isAction = True
        self.tm[6].get_act = True

        f7 = lambda: agendaLib.getTasks()
        self.tm[7].updateObjectCloud(["tasks", "schedule", 'to-do'])
        self.tm[7].updateVerbCloud(["read", "tell", "whats", "get"])
        self.tm[7].set_target_function(f7)
        self.tm[7].name = "tasks"
        self.tm[7].isAction = True
        self.tm[7].get_act = True

        f8 = lambda a: spotifyLib.selectsong(a)
        self.tm[8].updateObjectCloud([""])
        self.tm[8].updateVerbCloud(["play", "put on", "get"])
        self.tm[8].set_target_function(f8)
        self.tm[8].name = "playSong"
        self.tm[8].isAction = True
        self.tm[8].get_act = False


        f9 = lambda a: spotifyLib.selectplaylist(a)
        self.tm[9].updateObjectCloud(["playlist"])
        self.tm[9].updateVerbCloud(["play", "put on", "get"])
        self.tm[9].set_target_function(f9)
        self.tm[9].name = "playPlaylist"
        self.tm[9].isAction = True
        self.tm[9].get_act = False

        f10 = lambda: spotifyLib.skipmusic()
        self.tm[10].updateObjectCloud(["song", "track"])
        self.tm[10].updateVerbCloud(["skip", "next"])
        self.tm[10].set_target_function(f10)
        self.tm[10].name = "skipSong"
        self.tm[10].isAction = True
        self.tm[10].get_act = False

        f11 = lambda: spotifyLib.backmusic()
        self.tm[11].updateObjectCloud(["song","track"])
        self.tm[11].updateVerbCloud(["rewind"])
        self.tm[11].set_target_function(f11)
        self.tm[11].name = "prevSong"
        self.tm[11].isAction = True
        self.tm[11].get_act = False

        f12 = lambda: spotifyLib.pausemusic()
        self.tm[12].updateObjectCloud(["song","music","track"])
        self.tm[12].updateVerbCloud(["pause", "stop"])
        self.tm[12].set_target_function(f12)
        self.tm[12].name = "pauseMusic"
        self.tm[12].isAction = True
        self.tm[12].get_act = False

        f13 = lambda: spotifyLib.resume()
        self.tm[13].updateObjectCloud(["song","music","track","spotify"])
        self.tm[13].updateVerbCloud(["resume", "play"])
        self.tm[13].set_target_function(f13)
        self.tm[13].name = "resumeMusic"
        self.tm[13].isAction = True
        self.tm[13].get_act = False

        f14 = lambda: actions.get_incidents(a, b, c)
        self.tm[14].updateObjectCloud(["incidents","crimes","accidents","problems"])
        self.tm[14].updateVerbCloud(["get", "show", "find"])
        self.tm[14].set_target_function(f14)
        self.tm[14].name = "getIncidents"
        self.tm[14].isAction = True
        self.tm[14].get_act = True

        f15 = lambda: actions.track_phone()
        self.tm[15].updateObjectCloud(["location","phone location"])
        self.tm[15].updateVerbCloud(["get", "show", "find", "track"])
        self.tm[15].set_target_function(f15)
        self.tm[15].name = "trackPhone"
        self.tm[15].isAction = True
        self.tm[15].get_act = True

        f16 = lambda: actions.networkscan()
        self.tm[16].updateObjectCloud(["network","wifi","network devices"])
        self.tm[16].updateVerbCloud(["get", "show", "find", "scan"])
        self.tm[16].set_target_function(f16)
        self.tm[16].name = "scanNetwork"
        self.tm[16].isAction = True
        self.tm[16].get_act = True

        f17 = lambda: actions.getTasks()
        self.tm[17].updateObjectCloud(["tasks","to do","tasks", "schedule", "deadlines"])
        self.tm[17].updateVerbCloud(["get", "show", "find", "give"])
        self.tm[17].set_target_function(f17)
        self.tm[17].name = "getToDo"
        self.tm[17].isAction = True
        self.tm[17].get_act = True


        f18 = lambda: self.drives.rewardSoc()
        self.tm[18].updateObjectCloud(["social reward"])
        self.tm[18].updateVerbCloud(["get", "reached", "achieved", "gained"])
        self.tm[18].set_target_function(f18)
        self.tm[18].name = "social reward"
        self.tm[18].rewardState = True
        self.tm[18].get_act = False
        self.tm[18].isAction = False

        f19 = lambda: self.drives.rewardCur()
        self.tm[19].updateObjectCloud(["curiosity"])
        self.tm[19].updateVerbCloud(["get", "reached", "achieved", "gained"])
        self.tm[19].set_target_function(f19)
        self.tm[19].name = "curiosity"
        self.tm[19].rewardState = True
        self.tm[19].get_act = False
        self.tm[19].isAction = False

        f20 = lambda: self.drives.rewardSur()
        self.tm[20].updateObjectCloud(["survival"])
        self.tm[20].updateVerbCloud(["get", "reached", "achieved", "gained"])
        self.tm[20].set_target_function(f20)
        self.tm[20].name = "survival"
        self.tm[20].rewardState = True
        self.tm[20].get_act = False
        self.tm[20].isAction = False

class perception_stack():
    def __init__(self):
        self.percep_stack = []
    def novel(self, CM, index):
        self.percep_stack()




CM = model()
CM.manual_state_load()
'''
for x in range(0, len(CM.tm)):
    for y in range(0, len(CM.tm[x].tr)):
        CM.tm[x].action_potentiate(y)

while(True):
    for x in range(0, len(CM.tm)):
        for y in range(0, len(CM.tm[x].tr)):
            CM.tm[x].cycle_potentiate(y)
        print(CM.tm[x].tr)

'''





#YOOOOO YOOO LET'S GOOOO BABY BIG W FINALLY KNOW HOW TO USE LAMBDA FUNCTIONS
#assign target functions manually to states with relevant functions
#assign states verb object descriptor clouds manually
