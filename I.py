import numpy as np
class I:
    #
    def __init__(self):
        self.curiosity = 0.0
        self.sociability = 0.0
        self.survival = 0.0
        self.efficacy = 0.0
        self.pronouns = ["I", "my ", "mine"]
        self.sleepiness = 0.0
        self.decaylist = np.array([0.00001, 0.00001, 0.00001, 0.00001, 0.0001])
        #normalized between 0 and 1
        #values for states
        self.ceilingval = np.array([1.0, 1.0, 1.0, 1.0, 1.0])
        self.I = np.ndarray([self.curiosity, self.sociability, self.survival, self.efficacy])
    def refresh(self):
        self.I = np.ndarray([self.curiosity, self.sociability, self.survival, self.efficacy])
    def rewardCur(self):
        self.I[0]+=self.factorlist[0]
    def rewardSoc(self):
        self.I[1]+=self.factorlist[1]
    def rewardSur(self):
        self.I[2]+=self.factorlist[2]
    def rewardEff(self):
        self.I[2]+=self.factorlist[2]
    def rewardEff(self):
        self.I[2]+=self.factorlist[2]
    def decayrefresh(self):
        for x in range(0, len(1)):
            self.I[x]-=self.decaylist[x]
