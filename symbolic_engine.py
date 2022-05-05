#symbolic_engine.py
import moment
import inflect
from difflib import SequenceMatcher
from datetime import datetime, timedelta
def patch_dates_times(itf):
    alter = {"right now": "at " + datetime.now().strftime("%d/%b/%Y%H:%M:%S")}
    print("<----- Patching Dates and Times ----->")
    ents = itf['entities']
    parsed = None
    otl = itf['plaintext']
    mu = moment.utilities()
    #mu.string_to_val(itf['plaintext'])
    found_relevant = []
    fr_i_d = []
    fr_i_t = []
    counter = 0
    for key in ents:
        if(ents[counter][1]=="DATE" or ents[counter][1]=="TIME"):
            splitkey = ents[counter][0].replace('-', '/')
            splitkey = splitkey.replace("'", ' ')
            splitkey = splitkey.replace(',', ' ')
            splitkey = splitkey.lower()
            splitkey = splitkey.split(" ")
            for x in range(0, len(splitkey)):
                print(' - ' + str(splitkey[x]) + " (" + ents[counter][1] + ")")
                found_relevant.append(splitkey[x])
                splitkey[x] = splitkey[x].replace('/', ' ')
                splitkey[x] = splitkey[x].split(" ")
                for y in range(0, len(splitkey[x])):
                    if(splitkey[x][y] in itf['plaintext']):
                        if(ents[counter][1]=="TIME"):
                            fr_i_t.append(itf['plaintext'].index(str(splitkey[x][y])))
                        if(ents[counter][1]=="DATE"):
                            fr_i_d.append(itf['plaintext'].index(str(splitkey[x][y])))
        counter+=1
    if(len(found_relevant)>0):
        print("<----- entity permissible patch found ----->")
        parsed = mu.string_to_val(found_relevant)
    else:
        print("<----- no permissible entities, attempting rough time patch  ----->")
        parsed = mu.string_to_val(itf['plaintext'])

    subbed_index = None
    time_subs = []
    if(len(fr_i_t)>=1):
        t_sub_spread = 0
        prev_ind = fr_i_t[0]
        for x in range(0, len(fr_i_t)):
            if(fr_i_t[x] == prev_ind+1):
                time_subs.append([prev_ind,fr_i_t[x]])
            t_sub_spread += (fr_i_t[x] - prev_ind)
            prev_ind = fr_i_t[x]
        t_sub_spread = t_sub_spread/len(fr_i_t)
        #print("//time entity sub spread averaging to: " + str(t_sub_spread))

    date_subs = []
    if(len(fr_i_d)>=1):
        d_sub_spread = 0
        prev_ind = fr_i_d[0]
        for x in range(0, len(fr_i_d)):
            if(fr_i_d[x] == prev_ind+1):
                date_subs.append([ prev_ind,fr_i_d[x]])
            d_sub_spread += (fr_i_d[x] - prev_ind)
            prev_ind = fr_i_d[x]
        d_sub_spread = d_sub_spread/len(fr_i_d)
        #print("//date entity sub spread averaging to: " + str(d_sub_spread))
    if(parsed != None):
        for x in range(0, len(fr_i_d)):
            otl[fr_i_d[x]] = parsed.strftime("%d/%m/%Y")
        for y in range(0, len(fr_i_t)):
            otl[fr_i_t[y]] = parsed.strftime("%H:%M:%S")

        #print(time_subs)

        control_replace = True
        control_replace_count = 0

        timec = parsed.strftime("%H:%M:%S")
        timem = parsed.strftime("%d/%m/%Y")

        timecc = 0
        timemc = 0

        while(control_replace):
            if(control_replace_count >= len(otl)):
                control_replace = False
            else:
                if(timecc>0 and otl[control_replace_count]==timec):
                    otl.pop(control_replace_count)
                elif(timemc>0 and otl[control_replace_count]==timem):
                    otl.pop(control_replace_count)
                elif(timecc==0 and otl[control_replace_count]==timec):
                    timecc+=1
                    control_replace_count+=1
                elif(timemc==0 and otl[control_replace_count]==timem):
                    timemc+=1
                    control_replace_count+=1
                else:
                    control_replace_count+=1
        if(len(fr_i_d)==0 or len(fr_i_t)==0):
            otl.append(",")
            otl.append(timem)
            otl.append(" at ")
            otl.append(timec)

    #print("//time patch-parsed to: ")

    return(" ".join(otl))

def patch_inflect(itf):
    pass

def patch_pro(itf):
    print("<----- Patching Pronouns and Profiles ----->")
    for x in range(0, len(itf['plaintext'])):
        #second to first
        #print(itf['tokens'][x], itf['plaintext'][x])
        itf['plaintext'][x] = itf['plaintext'][x].lower()
        if(itf['tokens'][x] == 'PRP' or itf['tokens'][x] == 'PRON' or itf['tokens'][x] == 'NN'):
            if(itf['plaintext'][x] == 'you'):
                itf['plaintext'][x] = 'i'
            elif(itf['plaintext'][x] == 'your'):
                itf['plaintext'][x] = 'my'
            elif(itf['plaintext'][x] == "you're"):
                itf['plaintext'][x] = 'i am'
            elif(itf['plaintext'][x] == 'yours'):
                itf['plaintext'][x] = 'mine'
            #first to third
            elif(itf['plaintext'][x] == 'i'):
                itf['plaintext'][x] = str(itf['speaker'])
            elif(itf['plaintext'][x] == "i'm"):
                itf['plaintext'][x] = str(itf['speaker']) + " is"
            elif(itf['plaintext'][x] == 'me'):
                itf['plaintext'][x] = str(itf['speaker'])
            elif(itf['plaintext'][x] == 'my' or itf['plaintext'][x] == 'mine'):
                itf['plaintext'][x] = str(itf['speaker']) + "'s'"
    print("//pronoun patch-parsed to: ")
    #print(itf)
    return(itf)


def patch(itf):
    itf_original = itf
    patched_pron = patch_pro(itf)
    #print(patched_pron)
    found_date_ob = patch_dates_times(itf)
    #print(found_date_ob)
    return(found_date_ob)


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

#conflicting sentences induce forgetfullness ie  hat is the maximum flow & hat is not the maximum flow


#word encoding: one word sentiment for emotional words
