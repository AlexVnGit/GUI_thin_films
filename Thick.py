from Data2List import*
from matplotlib.pylab import *

def Thickness(Energies, Emin, Emax):
    ### Calculo da espessura
    energies, stopPow = Material2List('Sn.txt')

    Thick_max = []
    Thick_min = []

    for p in range(len(Emax)): ## percorrer cada um dos picos

        thick_max = 0
        thick_min = 0

        for i in range(len(stopPow)):
            #print('energies[i] = ', energies[i])
            if energies[i] >= Emax[p] and energies[i] <= Energies[p]:
                #print('energies[i] = ', energies[i])
                thick_max += 0.001/stopPow[i]

            if energies[i] >= Emin[p] and energies[i] <= Energies[p]:
                thick_min += 0.001/stopPow[i]

        Thick_max.append(thick_max)
        Thick_min.append(thick_min)

    print(Thick_max)
    print(Thick_min)

    thick_min = mean(Thick_max)
    thick_max = mean(Thick_min)

    thick = (thick_max + thick_min)/2 *1e7 ## nm
    dthick = (thick_max*1e7 - thick) ## nm

    print('Thickness = ',thick,'+-',dthick,' nm','\n')
    print()

    return