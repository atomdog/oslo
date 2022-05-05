#perception.py
#knowledge_graph.py
import pickle
def freeze_stack(web_cl):
    fh = open("memory/serialized-instances/perception.obj", 'wb')
    pickle.dump(web_cl, fh)

def torch_stack():
    web_cl = timeline()
    fh = open("memory/serialized-instances/perception.obj", 'wb')
    pickle.dump(web_cl, fh)

def thaw_stack():
    fh = open("memory/serialized-instances/perception.obj", 'rb')
    wewb = pickle.load(fh)
    return(wewb)


class timeline:
    def __init__(self):
        self.container = []
        #self.cognition_timeline_stack = []
        #self.visual_timeline_stack = []

def inittimeline():
    stack = timeline()
    freeze_stack(stack)
#add to stack
def add_stack(ws):
    stack = thaw_stack()
    stack.container.append(ws)
    freeze_stack(stack)

#read from stack
def get_stack():
    stack = thaw_stack()
    return(stack)

#external active participation
class heard:
    def __init__(self):
        self.descriptor = " heard "
        self.object = None
        self.subject = None
class saw:
    def __init__(self):
        self.descriptor = " saw "
        self.object = None
        self.subject = None
class noted:
    def __init__(self):
        self.descriptor = " noted that "
        self.object = None
#internal active participation
class acted:
    def __init__(self):
        self.descriptor = " acted to "
        self.subject = "I"
        self.object = None
class said:
    def __init__(self):
        self.descriptor = " said "
        self.subject = "I"
        self.object = None
#internal passive participation
class concluded:
    def __init__(self):
        self.descriptor = " concluded that "
        self.object = "I"
        self.subject = None
