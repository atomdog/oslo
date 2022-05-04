from sklearn.cluster import KMeans
import numpy as np
import pprofile
import tables
import dateLib
import matplotlib.pyplot as plt
import hashlib

class audioLog(tables.IsDescription):
    ID      = tables.StringCol(16)   # 16-character String
    time  = tables.StringCol(128)      # Signed 64-bit integer
    text  = tables.StringCol(5000)
    speechFingerPrint = tables.StringCol(5000)
    clusterTag  = tables.StringCol(16)

#standard hash
def create_hash_id(text, now):
    q = str(hashlib.md5((text+now).encode()).hexdigest())
    return(q)

#preps data for log by string conversion, no clusterID
def log_prep(text, sfp):
    #get current time, add date list to string
    d = dateLib.getNow()
    dretstring = ""
    for x in range(0, len(d)):
        if(x==(len(d)-1)):
            dretstring += str(d[x])
        else:
            dretstring += str(d[x]) + ","

    #convert fingerprint array to string
    sfpretstring = ""
    for x in range(0, len(sfp)):
        if(x==(len(sfp)-1)):
            sfpretstring += str(sfp[x])
        else:
            sfpretstring+= str(sfp[x])+","

    #hash of current time and text
    id = create_hash_id(dretstring,text)
    return([id,dretstring,text,sfpretstring])

#cleans and reassigns to proper datatypes
def log_clean(id, time, text, sfp, ct):
    dt = time.split(",")
    sfpi = sfp.split(",")
    for x in range(0, len(sfpi)):
        sfpi[x] = sfpi[x].astype(np.float)
    cti = int(cti)
    return(id,dt,text,sfpi,cti)


#creates empty audio log / clears current one
#pass audiolog class
def create_log(aL):
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="w", title="audiolog")
    group = h5file.create_group("/", 'Null', 'Audio')
    table = h5file.create_table(group, 'Null', aL, "Audio log")
    table.flush()
    h5file.close()

#appends precleaned row to log file
def append_log(id, time, text, sfp, ct):
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="a", title="audiolog")
    table = h5file.root.Null.Null
    r = table.row

    r["ID"] = id #encrypt
    r["time"] = time #encrypt
    r["text"] = text #encrypt
    r["speechFingerPrint"] = sfp #encrypt
    r["clusterTag"] = ct #encrypt

    r.append()
    table.flush()
    h5file.close()

def get_table_length():
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="a", title="audiolog")
    table = h5file.root.Null.Null
    count = 0
    for row in table:
        count+=1
    table.flush()
    h5file.close()
    return(count)

#prints full table
def print_full_table():
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="a", title="audiolog")
    table = h5file.root.Null.Null
    for row in table:
        print(" ")
        print(row["ID"].decode() + "||" + row["time"].decode() + "||" + row["text"].decode()+ "||" + row["speechFingerPrint"].decode()  +"||" + row["clusterTag"].decode())
        #+ "||" + row["speechFingerPrint"].decode()
        print(" ")
    table.flush()
    h5file.close()

def dump_sfp():
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="a", title="audiolog")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        #print(row["speechFingerPrint"].decode())
        q = (row["speechFingerPrint"].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = float(q[x])
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)

def dump_text():
    h5file = tables.open_file("memory/logs/audiolog.h5", mode="a", title="audiolog")
    table = h5file.root.Null.Null
    arr = []
    for row in table:
        store = []
        #print(row["speechFingerPrint"].decode())
        q = (row["text"].decode()).split(",")
        q = list(filter(None, q))
        for x in range(0, len(q)):
            q[x] = q[x]
        arr.append(q)
    table.flush()
    h5file.close()
    return(arr)


class audio_cortex:
        def __init__(self):
            self.m = True
            self.size = get_table_length()

            self.size_bool = False
        def check_size(self):
            if(self.size_bool==False):
                if(self.size>1):
                    self.size_bool = True
                    return(True)
                else:
                    return(False)
            else:
                return(True)
        def resolve_clusters(self,text,sfp):
            return("None")
        def log_Audio(self, text, sfp, clust):
            prepped = log_prep(text,sfp)
            append_log(prepped[0], prepped[1], prepped[2], prepped[3], clust)
        def passIn(self,text,sfp):
            clustered = "None"
            if(self.check_size()):
                clustered = self.resolve_clusters(text,sfp)
            self.log_Audio(text,sfp,clustered)

def wipe_log():
    f = audioLog
    create_log(f)
