#qanet.py
#https://huggingface.co/deepset/roberta-base-squad2

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import knowledge_graph
import semweblib

#work on
#REWRITE TO USE KNOWLEDGE GRAPH -> NO, USE semWeb
#TRIED TO REINVENT THE WHEEL WITH THE KNOWLEDGE GRAPH

#depreciated
def required_reading(question, model):
    print("< ------- QUERYING SAGE ------ >")
    context = []
    most_confident_score = -100000000000
    most_confident = None
    know_gr = knowledge_graph.thaw_graph()
    variant = False
    if(know_gr.clustered == True and variant == False):
        context = know_gr.postcluster2(question)
        context = " ".join(context)
        if(context != " " and len(context)!=0 and context!=""):
            answeredq = answer(question, context, model)
            return(answeredq)
        else:
            context = []
            variant = False
    elif variant == False:
        contheld = []
        for x in range(0, len(know_gr.matrix)):
            for y in range(0, len(know_gr.matrix[x].statement_array)):
                contheld.append(know_gr.matrix[x].statement_array[y])
            contheld = " ".join(contheld)
            context.append(contheld)
            context = " ".join(context)
            answeredq = answer(question, context, model)
            context = []
            contheld = []
            if(float(answeredq['score'])>float(most_confident_score)):
                most_confident = answeredq
    return(most_confident)

def consider(question, context, model):
    print("< ------- Considering Context ------ >")
    #follow traces -> aggregate conversation
    #context_a = web.aggregate_by_traces_typed(index,type,degree)
    response = answer(question, context, model)
    return(response)
def load_model():
    model_name = "deepset/xlm-roberta-large-squad2"
    #model_name = "google/electra-base-discriminator"
    nlp = pipeline(model=model_name, tokenizer=model_name, task="question-answering")
    return(nlp)
def answer(q, cont, model):
    a = None
    QA_input = {'question': q, 'context': cont}
    a = model(QA_input)
    return(a)
def sage():
    print("< ------- Loading Sage ------ >")
    model = load_model()
    yield(True)
    print("< ------- Sage Online ------ >")
    while(True):
        question = yield
        if(question is not None):
            print("< ------- QUESTIONING  ------ >")
            #pred = required_reading(question, model)
            pred = None
            yield(pred)
        else:
            pass

#takes a plaintext question and a semweb
def sage_mark2():
    print("< ------- Loading Sage Mk 2 ------ >")
    model = load_model()
    yield(True)
    print("< ------- Sage Mk 2 Online ------ >")
    while(True):
        questionpluscontext = yield
        #plaintext of question
        #load passed semweb so thawing isn't necessary
        if(questionpluscontext is not None):
            context = questionpluscontext[1]
            question = questionpluscontext[0]
            print("< ------- QUESTIONING  ------ >")
            #pred = required_reading(question, model)
            pred = consider(question, context, model)
            yield(pred)
        else:
            pass
