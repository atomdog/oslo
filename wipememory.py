#wipe_memory.py

import audiocortex
import semweblib
import time

def wipe_memory():
    print("<---- WIPING MEMORY IN 3... ---->")
    time.sleep(1)
    print("<---- WIPING MEMORY IN 2... ---->")
    time.sleep(1)
    print("<---- WIPING MEMORY IN 1... ---->")
    time.sleep(1)
    print("<---- WIPING MEMORY... ---->")
    semweblib.torch_web()
    audiocortex.wipe_log()
