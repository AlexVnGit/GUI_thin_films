import numpy as np

def Eloss(Energies, calibCent, filmCent, calibErr, filmErr, m, dm):
    ### Calculo da perda de energia, erro na perda de energia, energias máxima e minima perdida
    #resultFile.write('Eloss (keV)'+'\t'+'dEloss (keV)'+'\t'+'Emin (MeV)'+'\t'+'Emax (MeV)'+'\n')
    Eloss = []
    dEloss = []
    Emin = []
    Emax = []

    for p in range(len(calibCent)):

        eloss = (calibCent[p] - filmCent[p]) * m * 1000  ## keV
        deloss = np.sqrt(m**2 * (calibErr[p]**2 + filmErr[p]**2) + (calibCent[p]-filmCent[p])**2 * dm**2) * 1000  ## keV
        emin = Energies[p] - (eloss + deloss)/1000   ## MeV
        emax = Energies[p] - (eloss - deloss)/1000   ## MeV

        Eloss.append(eloss)
        dEloss.append(deloss)
        Emin.append(emin)
        Emax.append(emax)

        #resultFile.write(str(eloss)+'\t'+str(deloss)+'\t'+str(emin)+'\t'+str(emax)+'\n')
        #Eloss.append(eloss)
    #resultFile.close()

    print('Eloss = ', Eloss)
    print('dEloss = ', dEloss)
    print()
    return Emin, Emax