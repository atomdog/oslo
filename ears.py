# ears.py
#!/usr/bin/env python3
# additional sources: vosk helper code

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import simpleaudio as sa
import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel

q = queue.Queue()


def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        #print(status, file=sys.stderr)
        pass
    q.put(bytes(indata))

def listen():
    try:
        device = 0
        modelfp = "model2"
        if not os.path.exists(modelfp):
            print("Model File Path Not Founds")
        micarraypres = -1
        airpodpres = -1
        for x in range(0, len(sd.query_devices())):
            print(sd.query_devices(x))
            if(sd.query_devices(x)['name'] == 'USB PnP Audio Device' and sd.query_devices(x)['max_input_channels'] > 0):
                micarraypres = x
            if(sd.query_devices(x)['name'] == 'Aidan’s AirPods' and sd.query_devices(x)['max_input_channels'] > 0):
                airpodpres = x
        if(airpodpres > 0):
            device_info = sd.query_devices(airpodpres, 'input')
            device = airpodpres
        if(micarraypres > 0):
            device_info = sd.query_devices(micarraypres, 'input')
            device = micarraypres
        else:
            device_info = sd.query_devices(None, 'input')
            device = None
        print(device_info)
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(modelfp)
        spk_model = SpkModel("model-spk")


        with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=device, dtype='int16', channels=1, callback=callback):
            print("< ------ Ear Initialization Complete ------ >")
            yield(True)
            #print('#' * 80)
            #print('Press Ctrl+C to stop the recording')
            #print('#' * 80)
            rec = KaldiRecognizer(model, spk_model, samplerate)
            #rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()

                yieldtriga = False
                yieldtrigb = False
                #print(data)
                #numpydata = np.frombuffer(data, dtype=np.int16)
                #numpydata = independentca.source_segment(numpydata)
                #data = numpydata.tobytes()
                if rec.AcceptWaveform(data):
                    spkfp = None
                    spoken_text = None
                    #print(rec.Result())
                    res = json.loads(rec.Result())
                    if("spk" in res):
                        spkfp = res["spk"]
                        yieldtriga = True
                    if("text" in res):
                        spoken_text = res["text"]
                        yieldtrigb = True
                    if(yieldtriga == True and yieldtrigb == True):
                        yield([spkfp, spoken_text])

                    #print(str(spkfp) + "\n" + str(spoken_text))
                    #print(rec.PartialResult())
                    pass

    except KeyboardInterrupt:
        print('\n')

    except Exception as e:
        print("< ------ Exception in Audio  ------ >")
        print(type(e).__name__ + ': ' + str(e))
