import pyttsx3

def speak(text):
    print(text)
    engine = pyttsx3.init()
    if(text==None):
        print("Nothing to say...")
        engine.stop()
        return(0)
    engine.say(text)
    engine.runAndWait()
    engine.stop()
