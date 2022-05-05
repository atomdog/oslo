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
