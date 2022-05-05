#knowledge_graph.py
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
import numpy as np
from sklearn.decomposition import NMF
import spacy
import dill
import sys
sys.path.insert(0, './Language')
import spacyGenerator

def freeze_graph(web_cl):
    fh = open("memory/serialized-instances/knowledge.obj", 'wb')
    if(len(dill.detect.baditems(web_cl))==0):
        pickle.dump(web_cl, fh)
    else:
        return(False)

def torch_graph():
    web_cl = kg()
    fh = open("memory/serialized-instances/knowledge.obj", 'wb')
    pickle.dump(web_cl, fh)

def thaw_graph():
    fh = open("memory/serialized-instances/knowledge.obj", 'rb')
    wewb = pickle.load(fh)
    return(wewb)

class kg:
    def __init__(self):
        self.matrix = []
        self.clustRaw = None
        self.clustered = False
        self.clustNounChunk = None
        self.time_since_clustered = 0
    def process_catalyzed(self, frame, poin):
        q = statement(frame, poin)
        q.process()
        self.matrix.append(q)
        self.time_since_clustered+=1
        if(len(self.matrix)>25 and self.time_since_clustered>20):
            self.text_cluster()
            self.time_since_clustered = 0

    #fix to np array dtype object
    def precluster(self):
        print("<-- Preclustering knowledge_graph: general -->")
        listheld = []
        for x in range(0, len(self.matrix)):
            heldtxt = self.matrix[x].plaintext
            listheld.append(heldtxt)
        return(listheld)

    def precluster2(self):
        print("<-- Preclustering knowledge_graph: topics -->")
        listheld = []
        for x in range(0, len(self.matrix)):
            heldtxt = self.matrix[x].chunks
            listheld.append(heldtxt)
        return(listheld)

    def postcluster2(self, question):
        print("<-- Knowledge graph post-clustering resolution begun -->")
        context_arr = []
        print("prespacyGenerator.onlynouns")
        #takes in string
        question = spacyGenerator.only_nouns(question)
        #returns string

        print("<-- Vectorizing Question -->")
        #question = " ".join(question)
        X2 = self.vectorizer2.fit_transform(np.array([question]))
        print("<-- Question Vectorized -->")
        print("<-- Normalizing Question -->")
        svd = NMF(50)
        normalizer = Normalizer(copy=False)
        lsaq = make_pipeline(svd, normalizer)
        X2 = lsaq.fit_transform(X2)
        print("<-- Question Normalized -->")
        print("<-- Making Cluster Prediction -->")
        q = self.lkm.predict(X2)
        q2 = self.lkm2.predict(X2)
        ql = [q, q2]
        print("<-- Question Cl -->")
        print()
        for x in range(0, len(self.matrix)):
            if(self.matrix[x].clusteringId is not None):
                if(self.matrix[x].clusteringId[1] == ql[1]):
                    #print(self.matrix[x].plaintext)
                    context_arr.append(self.matrix[x].plaintext)
        return(context_arr)

    def text_cluster(self):
        X = self.precluster()
        X2 = self.precluster2()
        vectorizer = TfidfVectorizer(analyzer='word',max_df=0.9,max_features=5000,min_df=1,use_idf=False)
        self.vectorizer2 = TfidfVectorizer(analyzer='word',max_df=1.0,max_features=5000,min_df=1,use_idf=False)
        print("<-- Fitting TF-IDF Vectorizer to knowledge_graph -->")
        X = vectorizer.fit_transform(X)
        X2 = self.vectorizer2.fit_transform(X2)
        print("<-- Performing LSA value decomposition on knowledge_graph -->")
        svd = NMF(50)
        svd2 = NMF(50)
        normalizer = Normalizer(copy=False)
        normalizer2 = Normalizer(copy=False)
        lsa = make_pipeline(svd, normalizer)
        lsa2 = make_pipeline(svd2, normalizer2)
        X = lsa.fit_transform(X)
        X2 = lsa2.fit_transform(X2)
        km = KMeans(n_clusters=15,init="k-means++",max_iter=100000)
        km2 = KMeans(n_clusters=15,init="k-means++",max_iter=100000)
        print("<-- Fitting kmeans++ -->")
        self.lkm = km.fit(X)
        self.lkm2 = km2.fit(X2)
        print("<--- kmeans++ fit --->")
        original_space_centroids = svd.inverse_transform(self.lkm.cluster_centers_)
        original_space_centroids2 = svd2.inverse_transform(self.lkm2.cluster_centers_)

        order_centroids = original_space_centroids.argsort()[:, ::-1]
        order_centroids2 = original_space_centroids2.argsort()[:, ::-1]

        terms = vectorizer.get_feature_names()
        terms2 = self.vectorizer2.get_feature_names()
        #print(self.lkm.cluster_centers_)
        for i in range(15):
            print("Cluster %d:" % i, end="")
            for ind in order_centroids[i, :10]:
                print(" %s" % terms[ind], end="")
            print()
            print("Cluster %d:" % i, end="")
            for ind in order_centroids2[i, :10]:
                print(" %s" % terms2[ind], end="")
            print()
        self.clustered = True
        for x in range(0, len(self.matrix)):
            self.matrix[x].clusteringId = [self.lkm.labels_[x], self.lkm2.labels_[x]]
            #print(str(self.matrix[x].plaintext) + " " + str([km.labels_[x], km2.labels_[x]]))
            #print(km.labels_[x])
class statement:
    def __init__(self, frame, poin):
        self.plaintext = frame['plaintext']
        self.plaintext = " ".join(frame['plaintext'])
        self.chunks = " ".join(frame['chunks'])
        self.speaker = frame['speaker']
        self.trustinstatement = 0
        self.statement_array = []
        self.semweb_pointer = poin
        self.clusteringId = None
    def process(self):
        #print(self.plaintext)
        for x in range(0, len(self.plaintext)):
            self.statement_array.append(self.plaintext[x])
            #print(self.statement_array)



#make sentence split in languageloop
#make main
#subj obj pattern matching
