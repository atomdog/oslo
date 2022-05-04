#clusterResolve.py
import audiocortex

import numpy as np
import random

from yellowbrick.cluster import KElbowVisualizer
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from kneed import KneeLocator


from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from sklearn import mixture
from sklearn.cluster import OPTICS

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_samples, silhouette_score
#--------NOTES--------
#In high-dimensional data, the curse of dimensionality says that all distances become similar.
#This also affects data with cosine dist.
#PCA variance should be between 0.95 between 0.99
#---------------------

class clusterRes:
        def __init__(self):
            self.X = np.array(audiocortex.dump_sfp())
            self.pcad = None
            self.m = True
            self.vknn = None
            self.optimalclusters = None
            self.varPCA = None
            self.persistentKmodel = None
            self.persistentPCAKmodel = None
            self.kv = None
            self.y_km = None
            self.y_kx = None
        def knn_pred(self, value):
            self.vknn = KNeighborsClassifier(n_neighbors=self.optimalclusters)
            self.vknn.fit(self.X, self.y_kx)
            return(self.vknn.predict(np.array([value])))

        def kmean_pred(self, value):
            return(self.persistentKmodel.predict(np.array([value])))
        def variancePCA(self):
            self.PC = PCA()
            self.pcad = self.PC.fit_transform(self.X)
            self.varPCA = np.cumsum(self.PC.explained_variance_ratio_)
            print(self.varPCA)
            plt.plot(np.cumsum(self.PC.explained_variance_ratio_))
            plt.xlabel('number of components')
            plt.ylabel('cumulative explained variance');
            plt.show()
        #quick opt k
        def optKQuick(self, krange0, krange1):
            try:
                if(self.pcad.shape[0]>5):
                    km = KMeans(n_clusters=1, init='k-means++', max_iter=14000, tol=1e-04)
                    visualizer = KElbowVisualizer(km, k=(krange0,krange1), show=False)
                    if(visualizer==None):
                        print("<-- Optimal k failed-->")
                        return(1)
                    visualizer.fit(self.pcad)
                    print(visualizer.elbow_value_)
                    self.optimalclusters = visualizer.elbow_value_
                    if(self.optimalclusters==None):
                        self.optimalclusters = 1
                else:
                    print("<-- Optimal k failed-->")
            except:
                print("<-- Voice Upgrade Failed -->")
                self.optimalclusters = 1

        #sleeping necessary
        #take nap to re- up models
        def optKLong(self):
            if(len(self.X)>0):
                self.variancePCA()
            else:
                return(False)
            km = KMeans(n_clusters=1, init='k-means++', max_iter=14000, tol=1e-04)
            visualizer = KElbowVisualizer(km, k=(1,len(self.X)), show=False)
            if(visualizer==None):
                return(1)
            visualizer.fit(self.X)
            plt.clf()
            if(self.optimalclusters==None):
                self.optimalclusters = 1
            if(self.optimalclusters < len(self.pcad)):
                self.optimalclusters = visualizer.elbow_value_
            else:
                return(False)
        #abbreviated optimal cluster + clustering
        def upgradeQuick(self):
            print("<-- Performing Quick Voice Upgrade -->")
            if(len(self.X)>0):
                self.variancePCA()
                self.optKQuick(1,self.pcad.shape[0])
                print("<- Updated Optimal Known Voices:" + str(self.optimalclusters) + " ->")
                return(True)
            else:
                print("<-- Voice Upgrade Failed -->")
                return(False)
        #extensive+accurate optimal cluster + clustering
        def upgradeLong(self):
            print("<-- Performing Long Voice Upgrade -->")
            if(len(self.X)>0):
                self.variancePCA()
                self.optKLong()
                print("<-- Voice Upgrade Successful -->")
                print("<- Updated Optimal Known Voices:" + str(self.optimalclusters) + " ->")
                return(True)
            else:
                print("<-- Clustering failed -->")
                return(False)

        def cosine_dist(self, x, y):
            nx = np.array(x)
            ny = np.array(y)
            return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

        def kmean(self):
            km = KMeans(n_clusters=self.optimalclusters, init='k-means++', max_iter=14000, tol=1e-04)
            self.persistentPCAKmodel = km.fit(self.pcad)
            self.y_km = self.persistentPCAKmodel.predict(self.pcad)
            self.persistentKmodel = km.fit(self.X)
            self.y_kx = self.persistentKmodel.predict(self.X)

        def graphkmean(self):
            better_colors = []
            plt.clf()
            for coloriterator in range(0, self.optimalclusters):
                f = random.random()
                f2 = random.random()
                f3 = random.random()
                cv = coloriterator+random.randint(0, 20)
                red = (cv+f) % 1.0
                blue = (cv+f2) % 1.0
                green = (cv+f3) % 1.0
                color_insert=(red, blue, green)
                better_colors.append(color_insert)
            for i in range(len(self.pcad)):
                plt.scatter(self.pcad[i][0], self.pcad[i][1], c=[better_colors[self.y_km[i]]], alpha=0.8)
                plt.annotate(str(self.y_km[i]),(self.pcad[i][0],self.pcad[i][1]))
            #print(self.pcad)
            plt.show()
        def graph_plain(self):
            plt.clf()
            for i in range(len(self.pcad)):
                plt.scatter(self.pcad[i][0], self.pcad[i][1])
                #plt.annotate(str(self.y_km[i]),(self.pcad[i][0],self.pcad[i][1]))
            #print(self.pcad)
            plt.show()
        def graph_gm(self):
            better_colors = []
            plt.clf()
            for coloriterator in range(0, len(self.gm_labels)):
                f = random.random()
                f2 = random.random()
                f3 = random.random()
                cv = self.gm_labels[coloriterator]
                red = (cv+f) % 1.0
                blue = (cv) % 1.0
                green = (cv) % 1.0
                color_insert=(red, blue, green)
                better_colors.append(color_insert)
            for i in range(len(self.X)):
                plt.scatter(self.X[i][0], self.X[i][1], c=[better_colors[self.gm_labels[i]]], alpha=0.8)
                plt.annotate(str(self.gm_labels[i]),(self.X[i][0],self.X[i][1]))
            #print(self.pcad)
            plt.show()

        def optK_comprehensive(self):
            #silhouette score tracking
            max_sil_score_found = -100000
            k_number = -1

            #bayesian information criterion tracking
            min_bic_found = 10000000000
            b_number = -1

            #akaike information criterion tracking
            min_aic_found = 10000000000
            a_number = -1

            for itera in range(2, len(self.X)):
                km = KMeans(n_clusters=itera, init='k-means++', max_iter=14000, tol=1e-04)
                gm = GaussianMixture(n_components=itera, random_state=0).fit(self.X)
                km.fit_predict(self.X)
                score = silhouette_score(self.X, km.labels_, metric='cosine')
                bicscore = gm.bic(self.X)
                aicscore = gm.aic(self.X)
                if(aicscore<min_aic_found):
                    a_number = itera
                    min_aic_found = aicscore
                if(bicscore<min_bic_found):
                    b_number = itera
                    min_bic_found = bicscore
                if(score>max_sil_score_found):
                    k_number = itera
                    max_sil_score_found = score
            print("//silhouette optimal clusters...")
            print(k_number)
            print(max_sil_score_found)
            print("//bayesian information criterion optimal clusters...")
            print(b_number)
            print(min_bic_found)
            print("//akaike information criterion optimal clusters...")
            print(a_number)
            print(min_aic_found)
        
        def gauss_mm(self):
            self.X = np.array(audiocortex.dump_sfp())
            self.gm = GaussianMixture(n_components=2, random_state=0).fit(self.X)
            self.gm_labels = self.gm.predict(self.X)

            pass

def voice_engine():
    cR = clusterRes()
    if(cR.upgradeQuick()==True):
        cR.kmean()
        cR.graphkmean()
    yield(True)
    while(True):
        inframe = yield
        if(inframe is not None):
            if(inframe is not 0 and inframe[1] is not None and inframe[0] is not None):
                pred = cR.knn_pred(inframe)
                pred2 = cR.kmean_pred(inframe)
                print(pred)
                print(pred2)
                yield(pred2)
            elif(inframe == 0):
                cr.upgradeQuick()
        else:
            pass


cR = clusterRes()
cR.variancePCA()
print(cR.varPCA)
cR.optK_comprehensive()
cR.graph_plain()
cR.gauss_mm()
cR.graph_gm()






#aggregate all algorithms
#aggregate clustert0->clustert1->clustertn?
#points of clustert0 = points of cluster1 - 1, clustering could be totally different
