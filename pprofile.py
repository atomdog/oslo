
class profile():
    def __init__(self, ID):
        pronounslist = ["he", "him ", "his"], ["she", "her", "hers"], ["they", "them", "their"]
        prefix = [['Mister'], ['Miss'], []]
        self.ID = ID
        self.face = None
        self.namefirst = None
        self.namelast = None
        #pronouns
        self.pronouns = None
        self.prefix = None
        #attitude, politeness
        self.pScore = (None, None)
        #permissions
        self.trust = 0
        #presumed emotional state
        self.pES = 0
        #previous conversations attributed to this person
        self.prevConv = None
        self.phonenumber = None
        self.email = None
        self.appeal = None
        self.clusterID = None
        self.dateMet = None
        #add expiring and unknowns to unknown db
