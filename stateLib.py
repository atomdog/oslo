
import numpy as np
import I
import causalPointer
import perception
class state:
    def __init__(self, name, n):
        self.name = name
        self.tr = None
        self.init_transition_vector(n)
        self.rewardState = False
        self.action = False
        self.stimuli = False
        self.target_function = None
        self.VerbCloud = None
        self.ObjectCloud = None
        self.DescriptorCloud = None
        self.TI = None
        self.attachedPoints = []
        self.get_act = False
        self.potentiate_prior = None
        self.potentiate_factor = 10
        self.potentiate_counter = self.init_transition_vector(n)
    def isStimuli(self, boo):
        self.stimuli = boo
    def isAction(self, boo):
        self.action = boo

    def init_transition_vector(self, n):
        tsiv = (1/n) / 4
        self.tr = np.full((n, 4), tsiv, dtype = 'float128')
    def add_state(self, budget):
        n = budget/(len(self.tr))
        sum = 0
        for x in range(0, len(self.tr)):
            self.tr[x]= self.tr[x] * (1 - budget)
        self.tr = np.vstack([self.tr, np.full((1,4), budget/4, dtype = 'float128')])
        print(np.sum(self.tr))
        return(self.tr)
    def state_triggered(self):
        #open exp
        if(self.action == True):
            actp = perception.acted()
            actp.object = self.VerbCloud[random.randint(0,len(self.VerbCloud))] + " " + self.ObjectCloud[random.randint(0,len(self.ObjectCloud))]
            pload = perception.thaw_stack()
            pload.cognition_timeline_stack.append(actp)
            perception.freeze_stack(pload)
        pass
    def enact(self):
        pass
    def reward(self,):
        if(self.rewardState==True):
            pass
        else:
            pass
            #trigger reward in I
    def action_potentiate(self, rIndex):
        self.potentiate_counter = np.zeros(4, dtype = 'float128')
        self.potentiate_prior = self.tr[rIndex]
        self.tr[rIndex] = np.zeros(4, dtype = 'float128')
        #redistribute prob to other ones randomly
        pass
    def cycle_potentiate(self, rIndex):
        for x in range(0, len(self.potentiate_prior)):
            for y in range(0, 4):
                self.tr[rIndex][x] = np.float128(self.potentiate_prior[x]*(self.potentiate_counter[y]/self.potentiate_factor))
                print(self.potentiate_prior[x]*(self.potentiate_counter[y]/self.potentiate_factor))
                self.potentiate_counter[y]+=1

    def update(self):
        pass
    def pNS(self):
        pNS = np.amax(self.tr)
        return(pNS)
    def set_target_function(self, tf):
        self.target_function = tf
    def run_target_function(self):
        f = self.target_function()
        return(f)
    def updateVerbCloud(self, txt):
        self.VerbCloud = txt
    def updateObjectCloud(self, txt):
        self.ObjectCloud = txt
    def updateDescriptorCloud(self, txt):
        self.DescriptorCloud = txt
    def setTopicID(self, TI):
        self.TI = TI
