#startup.py

import configlib
import credLib
import audiocortex
import semweblib
import time
import perception

configlib.createBlankCred()
credLib.createBlankCred()
semweblib.torch_web()
audiocortex.wipe_log()
perception.torch_stack()
print("Welcome to OSLO...")
print("Make sure you enter credentials in memory/runtime/config.json to use with the codebase or edit the calls within main")
print("As input is integral to the main loop, everything will crash without them")
