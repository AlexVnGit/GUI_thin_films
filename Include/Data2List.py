#RiP
import csv

def Data2List(File):

    """
    Converts raw .mca file into Yield list
    
    INPUTS:  "FileName.mca"
    OUTPUTS: yield list
    """

    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    y = []
    aux = []
    for i in range(14,len(data)-1):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        y.append(float(aux[i][0]))
    
    return y

def Data2Lists(File):

    """
    Converts raw .mca file into Yield and channel lists
    
    INPUTS:  "FileName.mca"
    OUTPUTS: yield and channel lists
    """
    
    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    ch = []
    y = []
    aux = []
    for i in range(14,len(data)-1):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        ch.append(float(i)) ## axes in channel
        y.append(float(aux[i][0]))
    
    return y, ch

def Results2List(File):

    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter="\n", skipinitialspace=True)
        data = list(reader)
    centroides = []
    sigmas = []
    nets = []
    aux = []
    for i in range(1,len(data)):
        aux.append(data[i][0].split())
    for i in range(len(aux)):
        centroides.append(float(aux[i][0]))
        sigmas.append(float(aux[i][1]))
        nets.append(float(aux[i][2]))

    return centroides, sigmas, nets

def Material2List(File):

    density = 7.31 ## g/cm^3 for Sn
    with open(File, 'r') as file:
        reader = csv.reader(file, delimiter='\n', skipinitialspace=True)
        data = list(reader)
    energies = []
    stopPower = []
    aux = []
    for i in range(1,len(data)):
        aux.append(data[i][0].split('|'))
    for i in range(len(aux)):
        energies.append(float(aux[i][0]))
        stopPower.append(float(aux[i][1])*density) ## MeV/cm
    
    return energies, stopPower