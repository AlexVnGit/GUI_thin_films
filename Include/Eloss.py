import numpy as np

def Eloss(Energies, calibCent, filmCent, calibErr, filmErr, m, dm):
    ### Calculo da perda de energia, erro na perda de energia, energias máxima e minima perdida
    
    Eloss = []
    dEloss = []
    Emin = []
    Emax = []

    for p in range(len(calibCent)):

        eloss = (float(calibCent[p]) - float(filmCent[p])) * float(m)  ## keV
        deloss = np.sqrt(float(m)**2 * (float(calibErr[p])**2 + float(filmErr[p])**2) + (float(calibCent[p]) - float(filmCent[p]))**2 * float(dm)**2)  ## keV
        emin = Energies[p] - (eloss + deloss)/1000   ## MeV
        emax = Energies[p] - (eloss - deloss)/1000   ## MeV

        Eloss.append(eloss)
        dEloss.append(deloss)
        Emin.append(emin)
        Emax.append(emax)

    return Emin, Emax, Eloss