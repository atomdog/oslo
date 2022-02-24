#profLib.py
import json
import pprofile
def create_next_id():
    with open('profFile.json') as json_file:
        data = json.load(json_file)
    final_key = -1
    for key in data:
        final_key = key
    next_key = str(int(final_key)+1)
    data[next_key] = {}
    with open('profFile.json', 'w') as outfile:
        json.dump(data, outfile)
def createBlank():
    data = {}
    with open('profFile.json', 'w') as outfile:
        json.dump(data, outfile)
def load_file():
    with open('profFile.json') as json_file:
        data = json.load(json_file)
    return(data)
def fillbykey(key0, key1, param):
    data = load_file()
    data[key0][key1] = param
    with open('profFile.json', 'w') as outfile:
        json.dump(data, outfile)
def returnbykey(key0,key1):
    data = load_file()
    return(data[key0][key1])
def updateprofilefile(updated_list):
    data = {}
    for x in range(0, len(updated_list)):
        ckey = str(updated_list[x].ID)
        data[ckey] = {}
        data[ckey]['name'] = updated_list[x].namefirst
        data[ckey]['last_name'] = updated_list[x].namelast
        data[ckey]['pronouns'] = updated_list[x].pronouns
        data[ckey]['face'] = updated_list[x].face
        data[ckey]['trust'] = updated_list[x].trust
        data[ckey]['phone_number'] = updated_list[x].phonenumber
        data[ckey]['email'] = updated_list[x].email
        data[ckey]['date_met'] = updated_list[x].dateMet
        data[ckey]['clusterID'] = updated_list[x].clusterID
        data[ckey]['pes'] = updated_list[x].pes
        data[ckey]['previous_conv_pointer'] = updated_list[x].prevConv
    with open('profFile.json', 'w') as outfile:
        json.dump(data, outfile)

def load_profiles_from_file():
    with open('profFile.json') as json_file:
        data = json.load(json_file)
    profile_list = []
    for key in data:
        cdata = data[key]
        currently_loaded = pprofile.profile(int(key))
        if('name' in cdata):
            currently_loaded.namefirst = cdata['name']
        if('pronouns' in cdata and cdata['pronouns']!=None):
            currently_loaded.pronouns = int(cdata['pronouns'])
        if('last_name' in cdata):
            currently_loaded.namelast = cdata['last_name']
        if('trust' in cdata and cdata['trust']!=None):
            currently_loaded.trust = int(cdata['trust'])
        if('phone_number' in cdata):
            currently_loaded.phonenumber = cdata['phone_number']
        if('email' in cdata):
            currently_loaded.email = cdata['email']
        if('face' in cdata):
            currently_loaded.face = cdata['face']
        if('date_met' in cdata):
            currently_loaded.dateMet = cdata['date_met']
        profile_list.append(currently_loaded)
    return(profile_list)
    #return(data)
