#wipe_memory.py

import audiocortex
import semweblib

def wipe_memory():
    semweblib.torch_web()
    audiocortex.wipe_log()

wipe_memory()
