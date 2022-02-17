#chunkGen.py
import spacy
from nltk import word_tokenize, pos_tag
from spacy.pipeline import Sentencizer


def only_nouns(txt):
    #takes string, nto list
    if(type(txt) is list):
        txt = " ".join(txt)

    doc = load_model()(txt)
    retval = []
    for np in doc.noun_chunks:
        retval.append(np.text)
    retval = " ".join(retval)
    return(retval)

def load_model():
    nlp = spacy.load("en_core_web_sm")
    return(nlp)

def load_model2():
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")
    return(nlp)


def sentsegment(txt, model):
    # Construction via add_pipe
    doc = model(txt)
    retval = []
    for sentr in doc.sents:
        retval.append(sentr)
    return(retval)


def docprocgen():
    model = load_model2()
    yield(True)
    while(True):
        val = yield
        #print(val)

        if(val is not None):
            pred = sentsegment(val, model)
            yield(pred)
        else:
            pass

# Cons  truction from class



def spaci(sentence, model):
    spacied = model(sentence)

    entities = []
    for ent in spacied.ents:
        entities.append([ent.text, ent.label_, ent.kb_id_])

    tokens = []
    plaintext = []
    for token in spacied:
        tokens.append([token.text, token.tag_, token.pos_, token.head.text, token.dep_])
        plaintext.append(token.text)

    chunks = []
    for chunk in spacied.noun_chunks:
        chunks.append(chunk.text)
    package = [entities, tokens, chunks, plaintext]
    return(package)

def chunkGenerator():
    model = load_model()
    yield(True)
    while(True):
        val = yield
        #print(val)
        if(val is not None):
            pred = spaci(val, model)
            #print(pred)
            yield(pred)
        else:
            pass
