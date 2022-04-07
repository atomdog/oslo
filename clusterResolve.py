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

from scipy import sparse
from numba import njit
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
            self.y_labels = None
            self.labels = None
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
            #plt.plot(np.cumsum(pca.explained_variance_ratio_))

            #plt.xlabel('number of components')
            #plt.ylabel('cumulative explained variance');
            #plt.show()
        #@njit(fastmath=True, cache=True)
        def WCSS(X, m, labels, X2, m2):
            ret = 0
            m2 *= .5
            for i in range(len(X)):
                label = labels[i]
                ret += X2[i]+m2[label] - X[i]@m[:,label]
            return ret*2
        # X is a numpy array of data, m is the initial centers as column vectors, 
        # maxT helps with convergence, the function terminates based on maxT if something goes wrong
        # Xs is an optional argument to pass as the sparse version of X
        def kmeans(self, X,m, maxT, threshold, plots, Xs=None, X2Sum=None):
            (d,k),n,m2 = m.shape, len(X), np.einsum('ij,ij->j',m,m)
            E = sparse.csr_matrix((np.ones(n, bool), np.empty(n, np.int32), np.arange(n+1, dtype=np.int32)),(n,k))
            Xs, self.labels, prev_obj = X if Xs is None else Xs, E.indices, np.Inf
            if X2Sum is None: X2Sum = np.einsum('ij,ij->',X,X, dtype=np.float64)*.5
            # store the result of the matrix multiplication of 1D X and 2D m
            partL2 = np.dot(Xs,m) # this is a 1D array of length k
            np.subtract(np.multiply(.5, m2,m2), partL2, partL2)
            for t in range(maxT):
                # return the predicted labels for each value in 1D numpy array X, len(X) and len(labels) must be equal
                self.labels = np.argmin(partL2, axis=1) 
                E.data = partL2[np.arange(n), self.labels]
                E.eliminate_zeros() # this is necessary to make the sparse matrix work
                if E.nnz == 0: break # all points are identical
                np.einsum('ij,ij->j',X,X, dtype=np.float64, out=m2) # contains .5m^2 - Xm
                # call the objective WCSS helper function
                m2[np.arange(k), self.labels] += E.data # update centers
                np.add(Xs[E.indices,:], Xs[E.indptr[:-1],:], partL2) # update partL2
                np.subtract(X2Sum, partL2, partL2) # update partL2
                obj = self.WCSS(X, m, self.labels, X2Sum, m2)
                if prev_obj - obj <= threshold: break # threshold can be set to 0.0 for exact convergence
                prev_obj = obj
            if plots:
                plt.scatter(X[:,0], X[:,1], c=self.labels)
                plt.show()
            return self.labels, obj, t+1
            '''
            # assignment step
            partL2.argmin(1,labels)
            # mean updating step
            counts = np.bincount(labels, minlength=k)
            if np.all(counts): np.divide(X.T@E, counts, m)
            else:
                filter = counts !=0
                m[:,filter] = (X.T@E)[:,filter]/counts[filter]
            # check for convergence
            np.einsum('ij,ij->j',X,X, out=m2)
            obj, partL2 = self.WCSS(Xs, m, labels, X2Sum, m2)
            if prev_obj-obj <= threshold: break # threshold can be 0.0
            prev_obj = obj
            '''

        #quick opt k
        def optKQuick(self, krange0, krange1):
            try:
                if(len(self.pcad>5)):
                    km = KMeans(n_clusters=1, init='k-means++', max_iter=14000, tol=1e-04)
                    visualizer = KElbowVisualizer(km, k=(krange0,krange1), show=False)
                    if(visualizer==None):
                        return(1)
                        visualizer.fit(self.pcad)

                    self.optimalclusters = visualizer.elbow_value_
                    if(self.optimalclusters==None):
                        self.optimalclusters = 1
                else:
                    print("<-- Optimal k failed-->")
            except:
                self.optimalclusters = 1


        #sleeping necessary
        #take nap to re- up models
        def optKLong(self):
            try:
                if(len(self.pcad)>5):
                    km = KMeans(n_clusters=1, init='k-means++', max_iter=14000, tol=1e-04)
                    visualizer = KElbowVisualizer(km, k=(1,len(self.X)), show=False)
                if(visualizer==None):
                    return(1)
                visualizer.fit(self.X)
                plt.clf()
                if(self.optimalclusters < len(self.pcad)):
                    self.optimalclusters = visualizer.elbow_value_
                    km = KMeans(n_clusters=self.optimalclusters, init='k-means++', max_iter=14000, tol=1e-04)
                    km.fit(self.pcad)
                    self.y_labels = km.predict(self.pcad)
                else:
                    return(False)
            except:
                self.optimalclusters = 1

        def upgradeQuick(self):
            if(len(self.X)>0):
                self.variancePCA()
                self.optKQuick(1,len(self.pcad))
                print("<-- Voice Upgrade Successful -->")
                print("<- Updated Optimal Known Voices:" + str(self.optimalclusters) + " ->")
                return(True)
            else:
                print("<-- Voice Upgrade Failed -->")
                return(False)

        def upgradeLong(self):
            if(len(self.X)>0):
                self.variancePCA()
                self.optKLong()
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
                plt.scatter(self.pcad[i][0], self.pcad[i][1], c=[better_colors[self.y_labels[i]]], alpha=0.8)
                plt.annotate(str(self.y_labels[i]),(self.pcad[i][0],self.pcad[i][1]))
            #print(self.pcad)
            plt.show()

def voice_engine():
    cR = clusterRes()
    if(cR.upgradeQuick()==True):
        cR.kmean()
        cR.upgradeLong()
    yield(True)
    while(True):
        inframe = yield
        if(inframe is not None):
            if(inframe is not 0 and inframe[1] is not None and inframe[0] is not None):
                pred = cR.knn_pred(inframe)
                pred2 = cR.kmean_pred(inframe)
                cR.graphkmean()
                print(pred)
                print(pred2)
                yield(pred2)
            elif(inframe == 0):
                cR.upgradeQuick()
        else:
            pass










#aggregate all algorithms
#aggregate clustert0->clustert1->clustertn?
#points of clustert0 = points of cluster1 - 1, clustering could be totally different
