#configlib.py
import json

def createBlankCred():
    data = {
    'spotify' :
                {
                    'device_id' : '',
                    'configured': ''
                }
              ,
    'oslo' :
                {
                    'initialized' : '',
                    'createdaudiolog' : '',
                    'serializedweb' : '',
                    'serializedperception' : '',
                    'directorycheck' : '',
                    'profilescreated': '',

                }
              ,
    'phone' :
                {
                    'configured' : ''
                }
              ,
    'gmail' :
                {
                    'configured' : ''
                },
    'wyze' :
        {
            "configured": "",
        },

    'customaudio' :
        {
            "name": "",
        }
    }
    with open('memory/runtime/config.json', 'w') as outfile:
        json.dump(data, outfile)

def load_file():
    with open('memory/runtime/config.json') as json_file:
        data = json.load(json_file)
    return(data)

def fillbykey(key0, key1, param):
    data = load_file()

    data[key0][key1] = param
    with open('memory/runtime/config.json', 'w') as outfile:
        json.dump(data, outfile)

def returnbykey(key0,key1):
    data = load_file()
    return(data[key0][key1])

def check_file_paths():
    if(os.path.exists('./gmailapi/credentials.json') and os.path.exists('./gmailapi/credentials.json')):
        fillbykey("gmail", 'configured', 'true')
