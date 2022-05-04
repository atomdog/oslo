
def load_model():
    model = library.load("model_name")
    return(model)

def conversion(input_text_frame):
    return(False)

def example_gen():
    model = load_model()
    yield(True)
    while(True):
        val = yield
        if(val is not None):
            pred = conversion(val)
            yield(pred)
        else:
            pass

exg = example_gen()
genImp = True
while(True):
    flush = next(exg)
    genOut = exg.send(genImp)
