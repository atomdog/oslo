import ears
import pickle
import actions
import audiocortex
import speechLib
import clusterResolve
#import textflow

#checks, field all info, push inputs to causal_model, return path, enact target function

#Initializing speech2text generator

class audio_loop:
    print("< ------- Loading CM  ------ >")

    print("< ------- CM Loaded -------- >")

    print("< ------ Initializing Ear ------ >")
    ear = ears.listen()
    while(next(ear)!=True):
        time.sleep(0.1)

    print("< -- Initializing Audio Cortex -- >")
    audcortex = audiocortex.audio_cortex()
    print("< -- Audio Cortex Initialized --- >")

    print("< ------- Loading Voice Engine ------ >")
    creng = clusterResolve.voice_engine()
    while(next(creng)!=True):
        time.sleep(0.1)
    print("< ------- Voice Engine Online ------ >")
    print("   ")
    print("   ")
    print("   ")
    print("   ")
    print("#̷̨͕̝͚̬͋~̷͇͔̿͊̅̓̿̈͗͋#̵̬̭̲̞̺͆͆̄̿͛͐̇͋̎~̴̨̘̔́͑̌#̶̧̡̨̰͉̣̣́͘~̴̡͙̒̎̇̌̃͛ͅ#̷̛̱̰̒̇̋̿͠ ̷̨̨͍̠͎̤͉̱͎̦͆͌̄͊͑͘̚Ê̴̘̬͕̰͔n̴̠̲͈̠̺̥̜̹̙̲̓͆͋̆̉̏͂́͆̂t̶͖͓̪̭͖͕̄é̸̢̯̖̼͇r̷̨̙͓̽̾̿̕ͅí̷͇͙̞͍̘̣̰̠̦̒͂̔n̴̢̮͖̮̦͍̈̍̈͋̂̃͌̚g̷͕͖̟͒̆̈͌͊ ̵̡͎̙̻̰̎́͠T̴̞͖͔̮̿̀͒̆̀̒̊̄̋͠h̷̢̨̨̡͉̹̖̖͚̋̆́ͅe̴̢͚̤̫͍̝̤̠͑̓͒̋͒̕͜͜͠ ̵̬̦̍͂̅͐͝L̵̻̫̯̱͕͗̓̇́͊̚͝ợ̴͙̫̩̽̌̐̊̍̆o̶̢̼̭͎͉͇̭̠̼͗̈́̊͋̒̓ͅp̸̪̖̻̼͕͔̭̮͎̱͐͐ ̶͇̫̣̹̥̖̽͒̉̔̅ͅ#̷̢͆̇̋͊͒̊̕̚~̷̤̗̱̯̘̿͐̃̀͊͝#̵͚̘̼̝̱̼͙̻̘̗͛̑͗̓̾͘͠͝~̵̯̱̖͙̣͌̅̿̓̐̿͝#̶̡̼̬̰͇̙͐̾̈́̅͜~̷̭̼͛̍̇̋̎̌̿͂͊͝#̵̲̙͚̠͍̈́̂͛͜")
    print("   ")
    print("   ")
    print("   ")
    print("   ")
    while(True):
        #<-input block->
        #check for audio
        next(creng)
        current_audio_output = next(ear)
        audcortex.passIn(current_audio_output[1], current_audio_output[0])
        #print(current_audio_output[0])
        current_voice_val = creng.send(current_audio_output[0])
