########### 
# Por enquanto não se utilizam todas estas bibliotecas
#Mas irão ser necessárias (provavelmente)
#########

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
from matplotlib.pylab import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#import ctypes
 
#ctypes.windll.shcore.SetProcessDpiAwareness(1)

#############################################
# Esta funcao recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI. WIP
#############################################
def Plot(File, Name):
    Channel = []
    Counts = []

    if Name[-4:] == ".mca":

        for i in range(12, len(File) - 1):
            Counts.append(float(File[i]))
            Channel.append(i-11)

    fig = Figure()
    ax = fig.add_subplot(111)
    ax.plot(Channel, Counts, 'D', label = "Calibration Run")
    legend = ax.legend(loc = "upper right", ncol = 2, shadow = False,fancybox = False, framealpha = 0.0, fontsize = 15)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis = 'both', which = 'major', labelsize = 15)
    xlabel('Channel', fontsize = 15)
    ylabel('Counts', fontsize = 15)
    canvas = FigureCanvasTkAgg(fig, GraphicFrame)
    canvas.draw()
    canvas.get_tk_widget().grid(sticky = 'nw')



            



##############################################################################
#Esta função irá ler o ficheiro input. Em principio, apos receber o ficheiro
#ira automaticamente exibir o grafico
##############################################################################
def FileReader(): 

    domain = (('text files', '*.mca *.txt *.dat'), ('all files', '*.*'))
    filename = fd.askopenfilename(title = 'Open a file', initialdir = '.', filetypes = domain)    
    #showinfo(title = 'Selected File', message = filename)
    print(filename)
    OpenFile = open(filename, 'r')
    file = OpenFile.read()
    OpenFile.close()
    file = file.splitlines()
    Plot(file, filename)



###########################################################################
#Funcao em desenvolvimento... Ira ser a funçao que decide qual o algoritmo
#a ser utilizado na analise dos dados WIP
###########################################################################
def Analysis():

    Type = Menu.get()

    Window = tk.Tk()
    if Type == 'Select Analysis Method':
       myLabel = tk.Label(Window, text = "No Analysis Method Selected")
       myLabel.pack()
       ReturnButton = tk.Button(Window, text = 'Return', command = Window.destroy)
       ReturnButton.pack()  
    else:
       myLabel = tk.Label(Window, text = "Analysis Method Selected: \n" + Type)
       myLabel.pack()
       ReturnButton = tk.Button(Window, text = 'Return', command = Window.destroy)
       ReturnButton.pack()


###############################################################
# Funcao para abrir novas Tabs, WIP
################################################################
def Tabs():

    test2 = tk.Frame(TabFrame, borderwidth = 5, relief = 'sunken', bg = 'red', height = 1)
    test2.grid()
    Tab.add(test2, text = 'Trial 1')
    


########
#Toda esta secçao define as estruturas presentes na janela
#A maior parte dos widgets têm comentarios para explicar o contexto
#####
main = tk.Tk() #Janela Principal
main.state('zoomed')
main.title("AEL Thin Film Characterization")

######################## FRAMES #################################

    #Frame dos ícones ferramentas
ToolbarFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge') 
ToolbarFrame.grid(column = 0, row = 0, sticky = "nw")
#ToolbarFrame.grid_propagate(False)

    #Frame das Tabs
TabFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
TabFrame.grid(column = 1, row = 0, sticky = tk.E)
#TabFrame.grid_propagate(False)

    #Frame para o Gráfico
GraphicFrame = tk.Frame(main, borderwidth = 5, relief = 'ridge')
GraphicFrame.grid(column = 0, row = 1, sticky = "sw")
#GraphicFrame.grid_propagate(False)

    #Frame para os Dados
DataFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
DataFrame.grid(column = 1, row = 1, sticky = "se")
#DataFrame.grid_propagate(False)

#################### Tabs ########################

Tab = ttk.Notebook(TabFrame)
Tab.grid(sticky = "w")
CalibFrame = tk.Frame(TabFrame, borderwidth = 5, relief ='sunken', bg = 'blue', height = 1 )
CalibFrame.grid()
Tab.add(CalibFrame, text = 'Calib Trial')

##################### BUTOES #######################
    
    #Botao para chamar o menu de Upload do ficheiros
    
tk.Button(ToolbarFrame, text = "Insert Files" , command = FileReader, height = 1).grid(column = 0, row = 0)

    #Menu Dropwdown das Ferramentas de análise
Menu = tk.StringVar()
Menu.set("Select Analysis Method")
Options = ["Peak-Input", "Noise Remover", "Manual Selection"]
Tools = tk.OptionMenu(ToolbarFrame, Menu, *Options)
Tools.grid(column = 1, row = 0)
    
    #Botão de Começo da Análise
tk.Button(ToolbarFrame, text = 'Run', command = Analysis, height = 1).grid(column = 2, row = 0)

    #Botão de Download dos Dados
Download = tk.Button(ToolbarFrame, text = 'Download', height = 1)
Download.grid(column = 3, row = 0)

    #Botão de Separador Novo de Análise (Para os Filmes)
ThinFilm = tk.Button(ToolbarFrame, text = 'New Trial', height = 1, command = Tabs)
ThinFilm.grid(column = 4, row = 0)

    #Botão de Voltar ao Menu Principal
Escape = tk.Button(ToolbarFrame, text = 'Return to Main Menu', height = 1)
Escape.grid(column = 5, row = 0)

##################### MAINLOOP ####################

    #Mainloop mantém a janela do GUI aberta.
main.mainloop() 
