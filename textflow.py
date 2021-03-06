#textflow.py
import semweblib
import sageLibrary
import wernicke
import symbolic_engine
import re
import time
import nprop
import copy
import nltk

class stream():
    def __init__(self):
        self.recent_entities = []
        self.recent_chunks = []
        self.webo = None
        self.npcalc = nprop.npropengine()
    def split_sentences(self,blocktext):
        pass
    def resolve_source(self,voi):
        pass
    def unknown_resolve(self,voi):
        pass
    def subject_swap(self):
        pass
    #insert something from upper chain
    def trigger_state_insertion(self, snf):
        print("<--- Creating Semantic State Layers for: --->")
        #self.webo.state_insert(snf)
        pass
    #trigger rumination using x
    def trigger_rumination(self, x):
        print("<--- Rumination Triggered: --->")
        print(x)
        print("<----------------------------->")
        #self.webo.ruminate(x)
        pass
    def spawn_definitions(self, track, x):
        syn = wordnet.synsets(track[x].text)
        print("Word and Type : " + syn[1].name())
        print("Synonym of teaching is: " + syn[1].lemmas()[0].name())
        print("The meaning of the teaching : " + syn[1].definition())
        print("Example of teaching : " + str(syn[1].examples()))

    #create semantic web from upper levels
    def force_init(self):
        pass

    def routine(self):
        print("<--- Thawing Semantic Web --->")
        self.webo = semweblib.thaw_web()
        print("<--- Semantic Web Thawed --->")
        #instantiate coroutines
        print("<--- Preparing Flows --->")
        self.wern = wernicke.runnable()
        while(next(self.wern)!=True):
            time.sleep(0.1)
        print("<--- Flow to Wernicke Initialized --->")
        self.q_answer = sageLibrary.sage_mark2()
        while(next(self.q_answer)!=True):
            time.sleep(0.1)
        print("<--- Flow to Sage Initialized --->")

        #init coroutines

        self.currentSF = next(self.wern)
        self.currentQO = next(self.q_answer)


        #enter loop
        yield(True)
        while(True):
            response = { "plaintext": None,
                "confidence": None,
                "target": None,
                "type": None
                }
            #next(self.wern)
            #next(self.q_answer)
            fpack = yield
            print("<-- Text Flow Processing Input -->")
            #print(fpack)
            #fpack example:


            if(fpack is not None):
                #fpack[1] = text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|", "", fpack[1])

                #send to wernicke
                speaker = fpack[0]

                next(self.wern)
                next(self.q_answer)

                self.symengout = None
                self.currentSF = self.wern.send(fpack)

                #print(self.currentSF)
                top = copy.deepcopy(self.currentSF)

                patched = symbolic_engine.patch(top)
                print("//////////////////////////////////")
                print("///symbolic engine patched: //////")
                print(patched)
                print("//////////////////////////////////")
                print("//////////////////////////////////")
                if(patched == None):
                    print("<---- !ERR: SYMBOLIC ENGINE OFFLINE! ---->")
                #self.currentSF2 = self.wern.send(fpack)

                next(self.wern)
                self.currentSF = self.wern.send([speaker, patched])
                nom = self.currentSF

                if(nom == None):
                    print("<---- !ERR: WERNICKE OFFLINE! ---->")
                #check if wernicke returned a viable processed sentence frame
                if(nom!= True and nom != None and nom['plaintext']!= None and len(nom['plaintext'])!=0):
                    #encounter in semantic web
                    print("////////////////////////////")
                    print("////// proc now... /////////")
                    print(nom['plaintext'])
                    print(nom['speaker'])
                    print("////////////////////////////")
                    print("////////////////////////////")
                    self.webo.sentenceEncounter(nom)
                    #spin traces in semantic web
                    self.webo.spintrace()

                    #semweblib.freeze_web(self.webo)
                    #if current is declarative
                    if(self.webo.semWeb[len(self.webo.semWeb)-1].type == 3 or self.webo.semWeb[len(self.webo.semWeb)-1].type == 2):
                        #print(self.currentSF['plaintext'])
                        #send to symbolic engine, returns sentence frame with swapped personal pronouns
                        pass

                        #process the personal pronoun swapped statement, store for reading up on later

                        #knowledge graph struck from codebase for redundancy
                        #self.know_gr.process_catalyzed(self.symengout, len(self.webo.semWeb)-1)
                        #knowledge_graph.freeze_graph(self.know_gr)
                    #rewrite symbolic engine
                    #if current is interrogative
                    if(self.webo.semWeb[len(self.webo.semWeb)-1].type == 1):
                        #send to symbolic engine, returns sentence frame with swapped personal pronouns
                        #self.symengout = symbolic_engine.inbound_resolve_profile(self.currentSF)
                        #send plaintext to question
                        #switch to bfs
                        #get chunks, entities,
                        webbedcontext = self.webo.aggregate_by_noun_chunks(self.webo.recent_entry())
                        self.currentQO = self.q_answer.send([' '.join(self.currentSF['plaintext']), webbedcontext])
                        response['plaintext'] = self.currentQO['answer']
                        response['confidence'] = self.currentQO['score']
                        response['type'] = "answertoquestion"

                        #for x in range(0, len(self.webo.e_types)):
                            #print("<------->")
                            #print(self.webo.e_types[x])
                            #print(self.webo.get_by_entity(self.webo.e_types[x]))
                            #print("<------->")
                        if(self.currentQO == None):
                            print("<---- !ERR: SAGE OFFLINE! ---->")
                        else:
                            print(self.currentQO)
                    #self.webo.export_to_json()
                    print("<-- passing to n prop -->")
                    commands = self.npcalc.convert(self.webo.semWeb[self.webo.recent_entry()])
                    print("<--- n prop complete --->")

                    print("<---  Text Flow Cycle Completed --->")
                    yield(response, commands)
                else:
                    pass
