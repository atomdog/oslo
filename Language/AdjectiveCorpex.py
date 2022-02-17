#AdjCorp Constructor
import numpy as np
import tables
import hashlib


class adjCorp(tables.IsDescription):
    text  = tables.StringCol(5000)
    marker = tables.StringCol(1)

def create_corpus(aC):
    h5file = tables.open_file("Language/corpora/singlewordsentiment.h5", mode="w", title="SingleWordSentiment")
    group = h5file.create_group("/", 'Null', 'SingleWord')
    table = h5file.create_table(group, 'Null', aC, "SingleWordSentiment")
    table.flush()
    h5file.close()

def append_corpus(text, marker):
    h5file = tables.open_file("Language/corpora/singlewordsentiment.h5", mode="a", title="SingleWordSentiment")
    table = h5file.root.Null.Null
    r = table.row
    r["text"] = text
    r["marker"] = marker
    r.append()
    table.flush()
    h5file.close()

def print_full_table():
    h5file = tables.open_file("Language/corpora/singlewordsentiment.h5", mode="r", title="SingleWordSentiment")
    table = h5file.root.Null.Null
    for row in table:
        print(row["text"].decode() + " || " + row["marker"].decode())
    table.flush()
    h5file.close()

def textToH5(paths, corpclass):
    summedtext = []
    for x in range(0, len(paths)):
        file1 = open(paths[x], 'r')
        Lines = file1.readlines()
        for line in Lines:
            if(paths[x][9]=="p"):
                c = line.strip().encode('ascii', 'ignore')
                c = c.decode("utf-8")
                summedtext.append([c, 1])
            else:
                c = line.strip().encode('ascii', 'ignore')
                c = c.decode("utf-8")
                summedtext.append([c, 0])
    summedtext = sorted(summedtext)
    for x in range(0, len(summedtext)):
        append_corpus(summedtext[x][0], summedtext[x][1])


#get row of text without opening/closing file
def getIndex(tab, ind):
    row = tab.read(ind,ind+1)
    #flush I/O
    tab.flush()
    return([row["text"][0].decode(),row["marker"][0].decode()])

#binary search to return sentiment
def binarySearch(text):
    h5file = tables.open_file("Language/corpora/singlewordsentiment.h5", mode="r", title="SingleWordSentiment")
    table = h5file.root.Null.Null
    bottom = 0
    middle = 0
    top = len(table)-1
    while(bottom<=top):
        middle = (bottom+top) // 2
        if(getIndex(table, middle)[0] < text):
            bottom = middle + 1
        elif(getIndex(table, middle)[0] > text):
            top = middle -1
        else:
            final = getIndex(table, middle)[1]
            h5file.close()
            if(final == "0"):
                final = "-1"
            return(final)
    table.flush()
    h5file.close()
    return("0")
