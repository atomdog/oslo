from sklearn.decomposition import FastICA
import numpy as np
#independent component analysis
#reference: https://towardsdatascience.com/separating-mixed-signals-with-independent-component-analysis-38205188f2f4

#sources in this context can be voices, noises, music
#sources must be a linear mixture
#sources must be independent of each other
#sources must be non-gaussian signals

#function to center data
#subtraction of mean from X to gain zero mean, mean can later be added back

#https://reader.elsevier.com/reader/sd/pii/S0893608000000265?token=1B57416CFE91DD96CC0238CFCD2E541348F94E24E0F4DF183B6D278201171C52A98002509C196DA1D15733C7C9A8760F&originRegion=us-east-1&originCreation=20211130193518
def center_data(x):
    return(x - np.mean(x, axis=0, keepdims=True))
def get_mean(x):
    return(np.mean(x, axis=0, keepdims=True))
#function to 'whiten' data
#linear transformation of X in order to remove correlations between sources and variances equal identity
def blanch_data(x):
    #calculate covariance
    covaried = np.cov(x)
    #perform singular value decomposition on covariance
    U, S, V = np.linalg.svd(covaried)
    #calculate diagonal eigenvalue matrix
    d = np.diag(1.0 / np.sqrt(S))
    #calculate whitening matrix
    whiteM = np.dot(U, np.dot(d, U.T))
    #dot prod whitening matrix with x
    Xw = np.dot(whiteM, x)
    return(Xw, whiteM)
#kurtosis function
#kurtosis measures 'tailedness' of the probability distribution
#scaled version of the fourth moment of the distribution
#a moment is a quantitative measure of the shape of a functions graph
#if the 'tailedness' is high, kurtosis will be high
def kurtosis(x):
    n = np.shape(x)[0]
    mean = np.sum((x**1)/n) # Calculate the mean
    var = np.sum((x-mean)**2)/n # Calculate the variance
    skew = np.sum((x-mean)**3)/n # Calculate the skewness
    kurt = np.sum((x-mean)**4)/n # Calculate the kurtosis
    kurt = kurt/(var**2)-3
    return kurt, skew, var, mean


def fast_ica(signals,  alpha = 1, thresh=1e-8, iterations=5000):
    m, n = signals.shape
     # Initialize random weights
    W = np.random.rand(m, m)
    for c in range(m):
        w = W[c, :].copy().reshape(m, 1)
        w = w/ np.sqrt((w ** 2).sum())
        i = 0
        lim = 100
        while ((lim > thresh) & (i < iterations)):
                 # Dot product of weight and signal
            ws = np.dot(w.T, signals)
                 # Pass w*s into contrast function g
            wg = np.tanh(ws * alpha).T
                 # Pass w*s into g'
            wg_ = (1 - np.square(np.tanh(ws))) * alpha
                 # Update weights
            wNew = (signals * wg.T).mean(axis=0) - wg_.mean() * w.squeeze()
                 # Decorrelate weights
            wNew = wNew - np.dot(np.dot(wNew, W[:c].T), W[:c])
            wNew = wNew / np.sqrt((wNew ** 2).sum())
                 # Calculate limit condition
            lim = np.abs(np.abs((wNew * w).sum()) - 1)
                 # Update weights
            w = wNew
                 # Update counter
            i += 1
            W[c, :] = w.T
    return W

def source_segment(data):
    print(data)
    meanX = get_mean(data)
    Xc = center_data(data)
    print("centered")
    Xc = Xc.reshape(4000, 2)
    print(Xc.shape)
    Xw, whiteM = blanch_data(Xc)
    print("whitened")
    W = fast_ica(Xw,  alpha=1)
    print("ICA")
    unMixed = Xw.T.dot(W.T)
    unMixed = (unMixed.T - meanX).T
    print(unMixed)
    return(unMixed)
