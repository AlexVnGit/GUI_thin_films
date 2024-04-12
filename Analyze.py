from FitData import*
import numpy as np

def Analyze(y, ROId, ROIu):

    centroids = []
    sigmas = []
    error = []

    for r in range(len(ROId)):

        x1 = float(ROId[r])
        x2 = float(ROIu[r])

        Cent = float(peakCentroid(x1,x2,y))
        Sigma = float(peakSigma(x1,x2,y))
        Net = float(peakNet(x1,x2,y))

        centroids.append(Cent)
        sigmas.append(Sigma)
        error.append(Sigma/np.sqrt(float(Net)))


    return centroids, error
#################################################################