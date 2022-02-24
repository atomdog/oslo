#semantic node, ie word plus semantic meaning representation
import hashlib
import _pickle as pickle
import inspect
import dateLib
import matplotlib.pyplot as plt
import networkx as nx

def freeze_web(web_cl):
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)
def torch_web():
    web_cl = semWeb()
    fh = open("memory/serialized-instances/chillyWeb.obj", 'wb')
    pickle.dump(web_cl, fh)

def thaw_web():
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

        self.qual = "node"
        #semantic hash initialization
        self.semHash = None
        self.semHasher()

        #profile link
        #allows for direct resolution of subjects to other pieces of information
        self.profileLink = None
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
        self.subj = None
        self.obj = None
        self.relation = None
    def resolve_chunk_indices(self):
        #print(self.frame['chunks'])
        ci =  []
        chunks = self.frame['chunks']
        print(chunks)
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
class semWeb:
    def __init__(self):
        #composed of semantic row adjacency vectors
        self.semWeb = []
        #composed of semantic column adjacency vectors
        self.semTrack = []
        #total nodes, for arbitrary querying
        self.nodeList  = []
        self.traces = []
        self.relationLabel = []
    def recent_entry(self):
        if(len(self.semWeb)==0):
            return 0
        elif(len(self.semWeb)>=1):
            return(len(self.semWeb)-1)

    def drawVis(self):
        g = nx.DiGraph()
        for row in range(0, len(self.semWeb)):
            for nodec in range(0, len(self.semWeb[row].track)):
                if(self.semWeb[row].track[nodec].qual == "node"):
                    g.add_node(self.semWeb[row].track[nodec].text, **{'xy': [nodec,row]})
                    if(nodec!=0):
                        g.add_edge(self.semWeb[row].track[nodec].text, self.semWeb[row].track[nodec-2].text)
        #nodevislist = nx.get_node_attributes(g, 'xy')
        for x in range(0, len(self.traces)):
            #print(str(self.traces[x].ax) + " , " + str(self.traces[x].ay) + " -> " + str(self.traces[x].bx) + " , " + str(self.traces[x].by))
            nodeAtA = [v for v,h in g.nodes(data=True) if h['xy'][0]==self.traces[x].ax]
            nodeAtB = [v2 for v2,h in g.nodes(data=True) if h['xy'][0]==self.traces[x].bx]
            if(len(nodeAtA)>0 and len(nodeAtB)>0):
                g.add_edge(nodeAtA[0], nodeAtB[0])
        plt.clf()
        nx.draw_spectral(g, with_labels=False, node_size=1,width=1 )
        #plt.show()
        plt.savefig("wordweb.png")
        #plt.show()
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
        #slide in vector to web
        self.semWeb.append(vectorized)
        #clear semTrack
        self.semTrack = []
    #resolve relevancies
    #match to 'pool' of relevant information in profiles, states, previous webs
    #vertically insert
    #find occurence of each node's hash in web

    #try iterating upwards until find nearest matching node and then connecting the two
    #rather than connecting all at once
    def spintrace(self):
        self.traces = []
        for iterator in range(0, len(self.nodeList)):
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
                    self.semWeb[ay].track[ax].individual_traces.append(sem_trace(ax,ay,bx,by))

    def aggregate_by_traces_typed(self,index,form,degree):
        #self.drawVis()
        if(degree==None):
            degree = 1000
        #follow traces to produce plain text context. degree denotes expansion, ie
        #do we aggregate the connected indices of the web's as well.
        aggregated = []
        degree_counter = 0
        #queued to aggregate indices
        queued_to_aggregate = []
        invariant = False
        rowindex = index
        while(invariant==False):
            # print(queued_to_aggregate)
            for x in range(0, len(self.semWeb[rowindex].track)):
                if(isinstance(self.semWeb[rowindex].track[x], sem_node)):
                    #print(len(self.semWeb[rowindex].track[x].individual_traces))
                    for y in range(0, len(self.semWeb[rowindex].track[x].individual_traces)):
                        #if form matches
                        #print(y)
                        if(self.semWeb[rowindex].track[x].form == form):
                            #append y value (row index) to queue of indices to aggregate
                            queued_to_aggregate.append(self.semWeb[rowindex].track[x].individual_traces[y].by)
                        elif(form==None):
                            #if no form specified
                            queued_to_aggregate.append(self.semWeb[rowindex].track[x].individual_traces[y].by)
                    #append text to aggregated text
                if(self.semWeb[rowindex].track[x].qual == "node"):
                    aggregated.append(self.semWeb[rowindex].track[x].text)
            if(len(queued_to_aggregate) == 0 or degree_counter>degree):
                invariant = True
            else:
                if(queued_to_aggregate[0] != rowindex):
                    rowindex = queued_to_aggregate.pop(0)
                degree_counter+=1
        return(" ".join(aggregated))

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
        print(aggregatedplaintext)
        if(len(aggregatedplaintext)<10):
            aggregatedplaintext += " ".join(self.semWeb[row_index].text)
        print(aggregatedplaintext)
        return(aggregatedplaintext)


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
