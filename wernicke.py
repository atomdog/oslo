#wernicke.py

#non-native libraries
import sys
#import opennre
import hashlib
import time

#adjust system path to include Language folder
sys.path.insert(0, './Language/STClassifier')
sys.path.insert(0, './Language')

#import native generator libraries

import STGenerator
import spacyGenerator
import AdjectiveCorpex

def construct_empty_sentence_frame():
    sentence_frame = {
                        "sent_type_pred": None,
                        "plaintext": None,
                        "emotional_charge_vector": None,
                        "entities": None,
                        "tokens": None,
                        "chunks": None,
                        'speaker': None
                     }
    return(sentence_frame)

def resolveIndices(text, words):
    a = text.index(words[0])
    b = a + len(words[0])
    c = text.index(words[1])
    d = c + len(words[1])
    return([a,b,c,d])

#concatenate text and semantic form, encode, and then md5 hash
def create_hash_id(wtext, wform):
    q = hashlib.md5((wtext+wform).encode()).hexdigest()
    return(q)

def runnable():
    valid_corpexed = ['JJ', 'advmod', 'adj', 'WRB' 'JJ', 'JJR', 'JJS', 'advmod']
    print("< ------- Wernicke Area Initializing ------ >")
    #Initialize Sentence Type Generator
    STGen = STGenerator.STClassGen()
    #Wait until generator is alive
    while(next(STGen)!=True):
        time.sleep(0.1)
    print("< ------- Sentence Type Gen Online ------ >")


    #Initialize Spacy Generator
    spGen = spacyGenerator.chunkGenerator()

    #wait until generator is alive
    while(next(spGen)!=True):
        time.sleep(0.1)
    print("< ------- Spacy Gen Online ------ >")

    #Flush generator lines
    currentSTPred = next(STGen)
    currentspGen = next(spGen)
    yield(True)
    while(True):
        #insert sentence
        sentence = yield
        print(sentence)
        print("< ------- Wernicke Looping ------ >")
        sentence_frame = construct_empty_sentence_frame()
        if(sentence is not None):
            speaker = sentence[0]
            #get next from each generator
            next(STGen)
            next(spGen)

            f = sentence[1]

            #ship input to generators
            currentSTPred = STGen.send(f)
            currentspGen = spGen.send(f)
            #print(currentSTPred)

            #[entities, tokens, chunks]
            emotional_charge_vector = []
            if(currentspGen!=None):
                for x in range(0, len(currentspGen[1])):
                    if(currentspGen[1][x][1] == 'JJ' or currentspGen[1][x][1] == 'VBP' or currentspGen[1][x][1] == 'VBP'):
                        echarge = int(AdjectiveCorpex.binarySearch(currentspGen[1][x][0]))
                        emotional_charge_vector.append(echarge)
                    else:
                        emotional_charge_vector.append(0)
                    if(len(currentspGen[2])>=2):
                        q = resolveIndices(f, [str(currentspGen[2][0]), str(currentspGen[2][1])])
                    else:
                        pass
            #construct sentence frame
            #sentence_frame ["text"]

            if(currentspGen!=None and currentSTPred!=None):
                sentence_frame['sent_type_pred'] = currentSTPred[0]
                sentence_frame['emotional_charge_vector'] = emotional_charge_vector
                sentence_frame['plaintext'] = currentspGen[3]
                sentence_frame['entities'] = currentspGen[0]
                sentence_frame['tokens'] = currentspGen[1]
                #print(sentence_frame['tokens'])
                sentence_frame['chunks'] = currentspGen[2]
                sentence_frame['speaker'] = speaker
            yield(sentence_frame)
            print("<-- Wernicke Loop complete -->")
        else:
            pass



        #for adj in chnked text, apply AdjectiveCorpex






#tense, charge
#time spoken: y
#words: x
#tense: y


    #Initialize Spacy Generator
