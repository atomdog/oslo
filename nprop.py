#nprop.py
import json
import profLib

class npropengine:
    # sAeB[value]
    # sAeB[value]
    #pA[c<v]
    def __init__(self):
        print("//initializing propositional calculus")
        with open("./memory/runtime/state_language.json") as json_file:
            self.state_language = json.load(json_file)
        print("//initialized propositional calculus")
        print("")
        print("//initializing directory")
        self.directory = profLib.profiles()
        print("//initialized directory")
        pass
    def best_match(self,rep):
        tally = {}
        #list of dicts of of lists
        for x in range(0, len(rep)):
            for key in rep[x]:
                for y in range(0, len(rep[x][key][1])):
                    clist = rep[x][key][1]
                    if(len(clist) >= 1 and key!="ppairing"):
                        if clist[y] in tally:
                            tally[clist[y]] += 1
                        elif(not (clist[y] in tally)):
                            tally[clist[y]] = 1
        print(tally)
        return(tally)

    def convert(self,swtrack):
        rep = []
        cstring = []
        cstringvals = []
        ni = []
        for x in range(0, len(swtrack.track)):
            if(swtrack.track[x].qual == "node"):
                rep.append(self.tag_node_voep(swtrack.track[x]))
                ni.append(x)

        df = self.best_match(rep)
        max_df = 0
        mdi = -1
        mpercent = {}
        for mi in df:
            if(df[mi]>max_df):
                max_df = df[mi]
                mdi = mi
            mpercent[mi] = df[mi]/len(swtrack.track)
        #for each word in sentence
        for repx in range(0, len(rep)):
            #for each set of possible types
            for key in rep[repx]:
                cy = []
                #value
                for y in range(0, len(rep[repx][key][1])):
                    il = rep[repx][key][1]
                    cy.append("s_"+str(il[y])+ "_" + str(key[0]) +"_"+ str(rep[repx][key][0][y]))
                    cstringvals.append(ni[repx])
                cstring.append(cy)

        print(cstring)
        commands = self.can_apply(cstring)
        print(commands)
        #print(mpercent)
        return(commands)
    def tag_node_voep(self, node):
        v_i_v = []
        k_i_v = []

        v_i_o = []
        k_i_o = []

        v_i_d = []
        k_i_d = []

        v_i_e = []
        k_i_e = []
        v_i_p = []
        k_i_p = []
        word = node.text
        types = ["CARDINAL", "DATE",  "EVENT",  "FAC",        "GPE",       "LANGUAGE", "LAW",   "LOC",       "MONEY",    "NORP",   "ORDINAL",  "ORG",           "PERCENT",   "PERSON", "PRODUCT", "QUANTITY",     "TIME",  "WORK_OF_ART"]
        types_name = ["numbers", "dates", "events", "facilities", "countries", "language", "laws",  "locations", "monetary", "groups", "order",    "organization", "percentage", "people", "objects", "measurements", "times", "titles"]

        for key in self.state_language:
            if(self.state_language[key]["verbs"]!=None):
                if(word in self.state_language[key]["verbs"]):
                    v_i_v.append(self.state_language[key]["verbs"].index(word))
                    k_i_v.append(key)
            if(self.state_language[key]["objects"]!=None):
                if(word in self.state_language[key]["objects"]):
                    v_i_o.append(self.state_language[key]["objects"].index(word))
                    k_i_o.append(key)
            if(self.state_language[key]["descriptors"]!=None):
                if(word in self.state_language[key]["descriptors"]):
                    v_i_d.append(self.state_language[key]["descriptors"].index(word))
                    k_i_d.append(key)
            if(self.state_language[key]["param-entities"]!=None):
                if(node.entity_tag in types):
                    for xpe in range(0, len(self.state_language[key]["param-entities"])):
                        #print(self.state_language[key]["param-entities"][xpe])
                        #print(types_name[types.index(node.entity_tag)])
                        if(types_name[types.index(node.entity_tag)] in self.state_language[key]["param-entities"][xpe] or types_name[types.index(node.entity_tag)] == self.state_language[key]["param-entities"][xpe]):
                            v_i_e.append(xpe)
                            k_i_e.append(key)
            if(node.entity_tag in types):
                if(len(self.directory.piece_to_id_pair(word))!=0):
                    r = self.directory.piece_to_id_pair(word)
                    v_i_p.append(r[0])
                    k_i_p.append(r[1])
        #v is the index of the word in the state, k is the state
        tags = {"verbs": [v_i_v, k_i_v], "objects": [v_i_o, k_i_o], "descriptors": [v_i_d, k_i_d], "entities_parameter": [v_i_e, k_i_e], "ppairing": [v_i_p, k_i_p]}
        return(tags)
    def can_apply(self, cst):
        ca = []
        cap = {}
        for key in self.state_language:
            criteria_p = len(self.state_language[key]["param-entities"])
            filledp = []
            params = []
            for n in range(0, criteria_p):
                filledp.append(False)
                params.append([])

            criteria_f = self.state_language[key]['form']
            filledf = []
            findexer = 0
            if(self.state_language[key]['descriptors']!=None):
                criteria_d = len(self.state_language[key]['descriptors'])<1
            else:
                criteria_d = True
            if(self.state_language[key]['objects']!=None):
                criteria_o = len(self.state_language[key]['objects'])<1
            else:
                criteria_o =True
            if(self.state_language[key]['verbs']!=None):
                criteria_v = len(self.state_language[key]['verbs'])<1
            else:
                criteria_v = True
            for x in range(0, len(cst)):
                for y in range(0, len(cst[x])):
                    csplit = cst[x][y].split("_")
                    if(csplit[1]==key):
                        if(csplit[2]=="e"):
                            indexer = int(csplit[3])
                            print(indexer)
                            filledp[indexer] = True
                            #cap.append(cst[x])
                            params[indexer].append(cst[x])
                        if(len(criteria_f)>=1 and findexer<len(criteria_f)):
                            if(csplit[2]==criteria_f[findexer]):
                                findexer+=1
                        if(csplit[2]=="v"):
                            criteria_v = True
                        if(csplit[2]=="d"):
                            criteria_d = True
                        if(csplit[2]=="o"):
                            criteria_o = True
            if(not(False in filledp) and findexer==len(criteria_f) and criteria_o and criteria_d and criteria_v):
                ca.append(key)
                cap[key] = params
        return(cap)







        pass
    def boil(self):
        pass
