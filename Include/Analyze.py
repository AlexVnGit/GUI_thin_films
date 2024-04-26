from Include.FitData import*
import numpy as np

def Analyze(y, ROId, ROIu):

    centroids = []
    sigmas = []
    error = []

    for r in range(len(ROId)):

        if ROId[r] == 0 or ROId[r] == '' or ROIu[r] == 0 or ROIu[r] == '':
            pass
        else:
            x1 = float(ROId[r])
            x2 = float(ROIu[r])

            Cent = peakCentroid(x1,x2,y)
            Sigma = peakSigma(x1,x2,y)
            Net = peakNet(x1,x2,y)

            centroids.append(Cent)
            sigmas.append(Sigma)
            error.append(Sigma/np.sqrt(Net))
            
    return centroids, error, sigmas
#################################################################