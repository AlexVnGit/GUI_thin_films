from matplotlib.pylab import *

##########################
## Calculo da espessura ##
##########################
def Thickness(Energies, Emin, Emax, material):
    
    density = material[0][1] #g/cm3
    energies = [float(material[i][0]) for i in range(1,len(material))] # MeV
    stopPow = [float(material[i][1])*density for i in range(1,len(material))]  # MeV/cm

    Thick_max = []
    Thick_min = []
    Thick_peak = []

    ## Loop over peaks
    for p in range(len(Emax)):

        thick_max = 0
        thick_min = 0
        thick_mean = 0
        for i in range(len(stopPow)):
            if energies[i] >= Emax[p] and energies[i] <= Energies[p]:
                thick_max += 0.001/stopPow[i]

            if energies[i] >= Emin[p] and energies[i] <= Energies[p]:
                thick_min += 0.001/stopPow[i]
            
            if energies[i] >= (Emax[p]+Emin[p])/2 and energies[i] <= Energies[p]:
                thick_mean += 0.001/stopPow[i]

        Thick_max.append(thick_max)
        Thick_min.append(thick_min)
        Thick_peak.append(thick_mean)

    thick_min = mean(Thick_max)
    thick_max = mean(Thick_min)

    thick = (thick_max + thick_min)/2 *1e7 ## nm
    dthick = (thick_max*1e7 - thick) ## nm

    print('Thickness = ',thick,'+-',dthick,' nm','\n')
    print()

    return Thick_peak