import json

def createBlankCred():
    data = {
    'email' :
                {
                    'emailU' : '',
                    'emailP' : ''
                }
              ,
    'twitter' :
                {
                    'key0' : '',
                    'key1' : ''
                }
              ,
    'phone' :
                {
                    'phoneU' : '',
                    'phoneP' : ''
                }
              ,
    'shodan' :
                {
                    'shodanK' : ''
                },
    'spotify' :
        {
            "SPOTIPY_CLIENT_ID" : "",
            "SPOTIPY_CLIENT_SECRET" : "",
            "SPOTIPY_REDIRECT_URI" :  ""
        }
    }
    with open('credFile.json', 'w') as outfile:
        json.dump(data, outfile)

def load_file():
    with open('credFile.json') as json_file:
        data = json.load(json_file)
    return(data)

def fillbykey(key0, key1, param):
    data = load_file()

    data[key0][key1] = param
    with open('credFile.json', 'w') as outfile:
        json.dump(data, outfile)

def returnbykey(key0,key1):
    data = load_file()
    return(data[key0][key1])
