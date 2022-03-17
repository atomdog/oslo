#semantic node, ie word plus semantic meaning representation
import hashlib
import _pickle as pickle
import inspect#needed?
import dateLib
import json
import nltk
from nltk.corpus import stopwords

#-------------- aidan's notes --------------------
#layer of action TRACKS in web *****!!!
#sem_edges have hash of two connecting words creating unique key for pairs of words
#perhaps a higher level edge for a->root->b
#-------------------------------------------------

def freeze_web(web_cl):
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)

def torch_web():
    web_cl = sw()
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)

def thaw_web():
    torch_web()
    fh = open("memory/serialized-instances/chillyWeb.obj", 'rb')
    wewb = pickle.load(fh)
    return(wewb)


class sem_node:
    #'semantic hash' function
    #uniquely represents BOTH text and semantic form/meaning
    #superior to text as words which take different forms have different meanings
    def semHasher(self):
        self.semHash = hashlib.md5((self.text+self.form).encode()).hexdigest()

    def __init__(self, stringinit, POS, opos):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        #semantic POS
        self.form = POS
        self.alt_form = opos
        self.entity_tag = 'none'
        self.qual = "node"
        self.bind = None
        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #profile link
        #allows for direct resolution of subjects to other pieces of information
        self.profileLink = None
        self.individual_traces = []

class live_node:
    def semHasher(self):
        self.semHash = hashlib.md5((self.type).encode()).hexdigest()
    def __init__(self, stringinit, type):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        self.qual = "live_node"
        self.type = type
        self.entity_tag = self.type

        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #semantic POS (not relevant here)
        self.form = "live"
        self.alt_form = "none"
        self.profileLink = None
        #individual_traces
        self.individual_traces = []

class entity_node:
    def semHasher(self):
        self.semHash = hashlib.md5((self.type).encode()).hexdigest()
    def __init__(self, stringinit, type):
        self.inbound_edges  = []
        self.outbound_edges = []
        self.node_x = None
        self.node_y = None
        #textual representation
        self.text = stringinit
        self.qual = "entity_node"
        self.type = type
        self.entity_tag = self.type

        #semantic hash initialization
        self.semHash = None
        self.semHasher()
        #semantic POS (not relevant here)
        self.form = "entity"
        self.alt_form = "none"
        self.profileLink = None
        #individual_traces
        self.individual_traces = []

#carries meta-data for vector,
class sem_vector:
    def __init__(self):
        self.speaker = None
        self.frame = None
        #time metadata
        self.t = 0.0
        #sentence type
        self.type = None
        #actual vector
        self.track = []
        self.text = None
        self.chunk_indices = None
        self.entity_indices = None
        self.subj = None
        self.obj = None
        self.relation = None

    def resolve_chunk_indices(self):
        #print(self.frame['chunks'])
        ci =  []
        chunks = self.frame['chunks']
        for x in range(0, len(chunks)):
            cheld = chunks[x].split(' ')
            for y in range(0, len(cheld)):
                chunks.append(cheld[y])
        if(self.frame['chunks']==None):
            self.chunk_indices = ci
        elif(self.chunk_indices != None):
            if(len(self.chunk_indices)==0 or len(self.resolve_chunk_indices) >= 1):
                return(self.chunk_indices)
        else:
            for x in range(0, len(self.track)):
                if(self.track[x].qual == 'node'):
                    if(self.track[x].text in chunks):
                        ci.append(x)
            self.chunk_indices = ci
        print(chunks)
        return(self.chunk_indices)

    def entify(self):
        #type_lookup = {"CARDINAL":0,"DATE":2,"EVENT":4,"FAC":6, "GPE":8, "LANGUAGE":10, "LAW":12, "LOC":14, "MONEY":16, "NORP":18, "ORDINAL":20, "ORG":22, "PERCENT":24, "PERSON":26, "PRODUCT":28, "QUANTITY":30, "TIME":32, "WORK_OF_ART":34}
        sep =  []
        cp = -1
        self.entity_indices = []
        ets = self.frame['entities']
        for x in range(0, len(ets)):
            eheld = ets[x][0].split(' ')
            sep.append([ets[x][1]])
            cp+=1
            for y in range(0, len(eheld)):
                sep[cp].append(eheld[y])
        for y in range(0, len(sep)):
            for x in range(0, len(self.track)):
                if(self.track[x].qual == 'node'):
                    totie = []
                    for z in range(1, len(sep[y])):
                        if(self.track[x].text == sep[y][z]):
                            self.track[x].entity_tag = sep[y][0]
                            totie.append(x)
                            self.entity_indices.append(x)
            if(len(totie)>0):
                q = entity_bind()
                q.points = totie
                for x in range(0, len(totie)):
                    self.track[x].bind = q
        return(self.entity_indices)


#semantic edge, ie connection between two semantic nodes
#carries sentiment charge, negation charge, semantic meaning type, and a weight
#weight is updated by encounter frequency

class sem_edge:
    def __init__(self):
        self.sentiment_charge = 0.0
        self.negation = 0.0
        self.type = None
        self.weight = 0.0
        self.qual = "edge"

class entity_bind:
    def __init__(self):
        self.points = []
        self.qual = "entity_bind"

#vertical traces across time/meaning
class noided:
    def __init__(self):
        self.end = True
        self.qual = "noid"

class sem_trace:
    def __init__(self, ax, ay, bx, by):
        #starting point
        #x is column, y is row
        self.ax = ax
        self.ay = ay
        #ending point
        self.bx = bx
        self.by = by

#semantic web
class sw:
    def __init__(self):
        #composed of semantic row adjacency vectors
        self.semWeb = []
        #composed of semantic column adjacency vectors
        self.semTrack = []
        #total nodes, for arbitrary querying
        self.nodeList  = []
        self.traces = []
        self.relationLabel = []
        self.init_special_nodes()
        self.e_types = [    "CARDINAL", "DATE",  "EVENT",  "FAC",        "GPE",       "LANGUAGE", "LAW",   "LOC",       "MONEY",    "NORP",   "ORDINAL",  "ORG",           "PERCENT",   "PERSON", "PRODUCT", "QUANTITY",     "TIME",  "WORK_OF_ART"]
        self.type_lookup = {"CARDINAL":0,"DATE":2,"EVENT":4,"FAC":6, "GPE":8, "LANGUAGE":10, "LAW":12, "LOC":14, "MONEY":16, "NORP":18, "ORDINAL":20, "ORG":22, "PERCENT":24, "PERSON":26, "PRODUCT":28, "QUANTITY":30, "TIME":32, "WORK_OF_ART":34}
        self.root_rep = []


    def init_special_nodes(self):
        types = [    "CARDINAL", "DATE",  "EVENT",  "FAC",        "GPE",       "LANGUAGE", "LAW",   "LOC",       "MONEY",    "NORP",   "ORDINAL",  "ORG",           "PERCENT",   "PERSON", "PRODUCT", "QUANTITY",     "TIME",  "WORK_OF_ART"]
        types_name = ["numbers", "dates", "events", "facilities", "countries", "language", "laws",  "locations", "monetary", "groups", "order",    "organization", "percentage", "people", "objects", "measurements", "times", "titles"]

        ctrack = []
        #make node for each type

        for ind in range(0, len(types)):
            q = entity_node(types_name[ind], types[ind])
            q.node_x = 0
            q.node_y = len(self.semWeb)
            #insert into nodelist
            self.nodeList.append(q)
            #insert into track for semvector
            ctrack.append(self.nodeList[ind])
            #add an edge
            co = sem_edge()
            ctrack.append(co)
            #noid
        end = noided()
        ctrack.append(end)
        #wrap in semvector
        forweb = sem_vector()
        forweb.text = types_name
        forweb.track = ctrack
        #insert into semweb
        self.semWeb.append(forweb)

    def state_insert(self, snf):
        #for creation of a 'live' state node

        pass

    def update_root_rep(self):
        bookmark = self.semWeb[self.recent_entry()].track
        current_root_rep = []
        for x in range(0, len(bookmark)):
            if(bookmark[x].qual == "node"):
                current_root_rep.append(bookmark[x].text)
        self.root_rep.append(current_root_rep)
        print(self.root_rep)


    def recent_entry(self):
        if(len(self.semWeb)==0):
            return 0
        elif(len(self.semWeb)>=1):
            return(len(self.semWeb)-1)


    def export_to_json(self):
        json_node_form = {}
        for row in range(0, len(self.semWeb)):
            for nodec in range(0, len(self.semWeb[row].track)):
                if(self.semWeb[row].track[nodec].qual == "node" or self.semWeb[row].track[nodec].qual == "entity_node"):
                    #self.semWeb[row].track[nodec].text
                    json_slot = str(row)+'-'+str(nodec)
                    json_node_form[json_slot] = {"text": None, "hash": None}
                    json_node_form[json_slot]["text"] = self.semWeb[row].track[nodec].text
                    json_node_form[json_slot]["hash"] = self.semWeb[row].track[nodec].semHash
        json_edge_form = {}
        for x in range(0, len(self.traces)):
            json_edge_form[x] = {"startkey": None, "endkey": None}
            json_edge_form[x]["startkey"] = str(self.traces[x].ax) +'-'+str(self.traces[x].ay)
            json_edge_form[x]["endkey"] = str(self.traces[x].bx) +'-'+str(self.traces[x].by)
        json_node_form['edges'] = json_edge_form
        with open('interface/assets/imprisoned_web.json', 'w') as outfile:
            json.dump(json_node_form, outfile)

    def hash_word_combo(self, wordText, pos_tag):
        return(hashlib.md5((wordText+pos_tag).encode()))

    #find by hash
    def find_web_index_by_hash(self, to_locate_hash):
        #O(n) time
        indices = []
        rev_nodeList = self.nodeList
        rev_nodeList.reverse()
        for x in range(0, len(rev_nodeList)):
            if(rev_nodeList[x].semHash == to_locate_hash):
                #print(rev_nodeList[x].text)
                indices.append([rev_nodeList[x].node_x, rev_nodeList[x].node_y])
        return(indices)

    #find by text
    def find_web_index_by_text(self, to_locate_text):
        #O(n) time
        indices = []
        rev_nodeList = self.nodeList
        rev_nodeList.reverse()
        for x in range(0, len(rev_nodeList)):
            if(rev_nodeList[x].text == to_locate_text):
                indices.append([rev_nodeList[x].node_x, rev_nodeList[x].node_y])
        return(indices)

    #nodeEncounter, add semnode
    def nodeEncounter(self, frame, current):
        #get relevant information out of the sentence frame
        wordText = frame['plaintext'][current]
        pos_tag = frame['tokens'][current][1]
        opos_tag = frame['tokens'][current][4]
        ents = frame['entities']
        #check if text is within an entity
        #initialize node index as None
        currentNodeIndex = None
        #create node hash
        tenativeN = hashlib.md5((wordText+pos_tag).encode())
        self.nodeList.append(sem_node(wordText, pos_tag, opos_tag))
        #attach x,y coordinates to the node
        #we haven't appended to the semtrack or semweb so length is correct
        currentNodeIndex = len(self.nodeList)
        #if length of the nodeList is greater than 1 we can correct for off by 1 error
        if(len(self.nodeList)>=1):
            currentNodeIndex = currentNodeIndex-1
        self.nodeList[currentNodeIndex].node_x = len(self.semTrack)
        self.nodeList[currentNodeIndex].node_y = len(self.semWeb)
        """
        for eiter in range(0, len(ents)):
            if(wordText in ents[eiter][0]):
                self.nodeList[currentNodeIndex].entity_tag = ents[eiter][1]
        """
        #print(self.nodeList[currentNodeIndex].node_x, self.nodeList[currentNodeIndex].node_y)
        #return node index
        return(currentNodeIndex, frame['emotional_charge_vector'][current])



    def track_construction(self, sentFrame, current, sentcharge):
        #toss node into semtrack
        self.semTrack.append(self.nodeList[current])
        outbound_edge = sem_edge()
        if(self.nodeList[current].alt_form=="neg"):
            outbound_edge.negation = 1.0
        else:
            outbound_edge.negation = 0
        outbound_edge.sentiment_charge = sentcharge
        outbound_edge.type = None
        outbound_edge.weight = None
        self.semTrack.append(outbound_edge)


    def track_stop(self):
        q = noided()
        self.semTrack.append(q)

    #encounter sentence, words into nodes, create
    def sentenceEncounter(self, sentFrame, sourceFrame):
        if(sentFrame == None):
            return False
        #print(sentFrame['plaintext'])
        for x in range(0, len(sentFrame['plaintext'])):
            current_nodeXval, sentcharge = self.nodeEncounter(sentFrame, x)
            #print(sentFrame['tokens'][x])
            if(current_nodeXval!=None):
                self.track_construction(sentFrame, current_nodeXval, sentcharge)
        #noid track
        self.track_stop()
        #init vector carrier
        vectorized = sem_vector()
        #pass track to vector
        vectorized.track = self.semTrack
        vectorized.frame = sentFrame
        vectorized.text = sentFrame['plaintext']
        vectorized.t = dateLib.getNow()
        #if we have a sentence type prediction, fill it in
        if(sentFrame['sent_type_pred']!=None):
            vectorized.type = sentFrame['sent_type_pred']
        vectorized.entify()
        #slide in vector to web
        self.semWeb.append(vectorized)
        self.update_root_rep()
        #clear semTrack
        self.semTrack = []



    #resolve relevancies
    #match to 'pool' of relevant information in profiles, states, previous webs
    #vertically insert
    #find occurence of each node's hash in web

    #try iterating upwards until find nearest matching node and then connecting the two
    #rather than connecting all at once

    #stop connecting stopwords



    def spintrace(self):
        self.traces = []
        for iterator in range(0, len(self.nodeList)):
            cx = self.nodeList[iterator].node_x
            cy = self.nodeList[iterator].node_y
            self.nodeList[iterator].individual_traces = []
            self.semWeb[cy].track[cx].individual_traces = []
            if(self.nodeList[iterator].text in nltk.corpus.stopwords.words('english') or self.nodeList[iterator].text == " "):
                pass
            else:
                totracelist = self.find_web_index_by_hash(self.nodeList[iterator].semHash)
                for iterator2 in range(0, len(totracelist)):
                    self.semWeb[totracelist[iterator2][1]].track[totracelist[iterator2][0]].individual_traces = []
                    for iterator3 in range(0, len(totracelist)):
                        if(iterator2!=iterator3 and len(totracelist[iterator2])>1 and len(totracelist[iterator3])>1):
                            ax = totracelist[iterator2][0]
                            ay = totracelist[iterator2][1]
                            bx = totracelist[iterator3][0]
                            by = totracelist[iterator3][1]
                            self.traces.append(sem_trace(ax, ay, bx, by))
                            self.semWeb[by].track[bx].individual_traces.append(sem_trace(bx,by,ax,ay))
                            self.semWeb[ay].track[ax].individual_traces.append(sem_trace(ax,ay,bx,by))
            if(self.nodeList[iterator].entity_tag!='none' and self.nodeList[iterator].qual != 'entity_node'):
                targetx = self.type_lookup[self.nodeList[iterator].entity_tag]
                #print(targetx)
                cnode = self.nodeList[iterator]
                #print(self.semWeb[0].track[targetx].entity_tag + ": " + cnode.text)
                #print(str(cnode.node_x) + ", " + str(cnode.node_y) + "--->" + str(targetx) + ', 0')
                self.semWeb[cnode.node_y].track[cnode.node_x].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, 0))
                self.semWeb[0].track[targetx].individual_traces.append(sem_trace(targetx, 0, cnode.node_x, cnode.node_y))
                self.nodeList[iterator].individual_traces.append(sem_trace(cnode.node_x, cnode.node_y, targetx, 0))
                self.traces.append(sem_trace(cnode.node_x,cnode.node_y, targetx, 0))


    def aggregate_by_noun_chunks(self, row_index):
        print("<--- Retrieving relevant sentences via noun chunks for:   -->")
        print(" ".join(self.semWeb[row_index].text))
        print("<------------------------------------------------------------> ")
        chunkindices = self.semWeb[row_index].resolve_chunk_indices()
        targeted_nodes = []
        aggregatedplaintext = []
        for x in range(0, len(chunkindices)):
            q = self.semWeb[row_index].track[chunkindices[x]]
            for x2 in range(0, len(q.individual_traces)):
                if(' ' in self.semWeb[q.individual_traces[x2].by].text):
                    self.semWeb[q.individual_traces[x2].by].text.remove(' ')
                aggregatedplaintext.append(" ".join(self.semWeb[q.individual_traces[x2].by].text))
        aggregatedplaintext = ". ".join(aggregatedplaintext)

        if(len(aggregatedplaintext)<10):
            aggregatedplaintext += " ".join(self.semWeb[row_index].text)
        print(aggregatedplaintext)
        return(aggregatedplaintext)


    def get_by_entity(self, type):
        key = self.type_lookup[type]
        elist = self.semWeb[0].track[key].individual_traces
        print(key)
        print(elist)
        aggregated =[]
        for x in range(0, len(elist)):
            print(elist[x].by)
            aggregated.append(self.semWeb[elist[x].by].track[elist[x].bx].text)
        return(aggregated)

    def aggregate_recent_conversation(self):
        aggregated = []
        return(aggregated)

    def aggregate_by_occurence(self, hash):
        aggregated =[]
        return(aggregated)

    def aggregate_by_speaker(self,spkid):
        aggregated =[]
        return(aggregated)







#need a handler to pass different types of statements in, ie add speaker if it was a spoken request
#automatically load and pass in commands

def handler(take_in):
    pass









#init vector with nodes,
#graph; time is y, word is X, thus we have a vector of length n, where n is number
#of known words (exposed semantic vocabulary)?

#connecting things between y axis? perhaps subjects, etc

#edges carry several charges across them
