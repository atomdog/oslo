#symbolic_engine.py

def conversion(input_text_frame):
    return(False)
def resolve_relevancy(input_text_frame):
    pass
    #locate subj/obj/root
    #match to states
    #match to semweb
def inbound_resolve_profile(input_text_frame):
    for x in range(0, len(input_text_frame['plaintext'])):
        #second to first
        input_text_frame['plaintext'][x] = input_text_frame['plaintext'][x].lower()
        if(input_text_frame['tokens'][x] == 'PRP' or input_text_frame['tokens'][x] == 'PRON' or input_text_frame['tokens'][x] == 'NN'):
            if(input_text_frame['plaintext'][x] == 'you'):
                input_text_frame['plaintext'][x] = 'i'
            elif(input_text_frame['plaintext'][x] == 'your'):
                input_text_frame['plaintext'][x] = 'my'
            elif(input_text_frame['plaintext'][x] == "you're"):
                input_text_frame['plaintext'][x] = 'i am'
            elif(input_text_frame['plaintext'][x] == 'yours'):
                input_text_frame['plaintext'][x] = 'mine'
            #first to third
            elif(input_text_frame['plaintext'][x] == 'i'):
                input_text_frame['plaintext'][x] = str(input_text_frame['speaker'])
            elif(input_text_frame['plaintext'][x] == "i'm"):
                input_text_frame['plaintext'][x] = str(input_text_frame['speaker']) + " is"
            elif(input_text_frame['plaintext'][x] == 'me'):
                input_text_frame['plaintext'][x] = str(input_text_frame['speaker'])
            elif(input_text_frame['plaintext'][x] == 'my' or input_text_frame['plaintext'][x] == 'mine'):
                input_text_frame['plaintext'][x] = str(input_text_frame['speaker']) + "'s'"
    return(input_text_frame)

'''
def runnable():
    yield(True)
    while(True):
        val = yield
        if(val is not None):
            pred = inbound_resolve_profile(val)
            yield(pred)
        else:
            yield(False)
'''
#stan typed dep

#agent  An agent is the complement of a passive verb which is introduced by the preposition “by” and does the action
#cc  A coordination is the relation between an element of a conjunct and the coordinating conjunction word of the conjunct.
#conj A conjunct is the relation between two elements connected by a coordinating conjunction, such as “and”, “or”, etc. We treat conjunctions asymmetrically:
#det A determiner is the relation between the head of an NP and its determiner.
#dobj The direct object of a VP is the noun phrase which is the (accusative) object of the verb.
#expl This relation captures an existential “there”. The main verb of the clause is the governor
#neg negation modifier
#num numeric quantifier
#poss possesive modifier
#tmod temporal modifier

#dependency




#sentence type 4
#imperative: consider action/fufillment
#declarative: consider fallacy/agreement
#interrogative: evaluate objective / form response
#exclamatory: evaluate sentiment in context

#linkage type
# = pure link: is / are
# > posessive: has, posesses
# ! negative, inverts linkage
# V binding, joins points
# | conditional; represents conditions
# * time dependent; temporary or affected by time
# ~ attribute or quality
#   physical location


#word encoding: one word sentiment for emotional words
