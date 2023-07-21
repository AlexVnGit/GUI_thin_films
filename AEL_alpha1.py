########### 
# Por enquanto não se utilizam todas estas bibliotecas
#Mas irão ser necessárias (provavelmente)
#########

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
#from PIL import ImageTk, Image
#from tkinter.messagebox import showinfo
from matplotlib.pylab import *
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import ctypes
 
ctypes.windll.shcore.SetProcessDpiAwareness(1)


def on_key_event(event, canvas, toolbar):
    matplotlib.backend_bases.key_press_handler(event, canvas, toolbar)

#############################################
# Esta funcao recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI. WIP
#############################################
def Plot(File, Name):
    Channel = []
    Counts = []

    Data = open("Data.txt", "w")

    if Name[-4:] == ".mca":

        for i in range(12, len(File) - 1):
            Counts.append(float(File[i]))
            Channel.append(i-11)
            Data.write(str(Counts[i-12])+"\n")

    Data.close()

    fig = Figure(figsize =(6, 5) )
    ax = fig.add_subplot(111)
    ax.plot(Channel, Counts, '.', label = "Calibration Run")
    legend = ax.legend(loc = "upper right", ncol = 2, shadow = False,fancybox = False, framealpha = 0.0, fontsize = 15)
    legend.get_frame().set_facecolor('#DAEBF2')
    tick_params(axis = 'both', which = 'major', labelsize = 15)
    xlabel('Channel', fontsize = 15)
    ylabel('Counts', fontsize = 15)
    canvas = FigureCanvasTkAgg(fig, GraphicFrame)
    canvas.draw()
    canvas.get_tk_widget().pack(expand= True)
    toolbar = NavigationToolbar2Tk(canvas, GraphicFrame)    
    canvas.mpl_connect('key_press_event', lambda event: on_key_event(event, canvas, toolbar))
    toolbar.update()
    main.bind('<Control-w>', lambda event: main.destroy())
  

##############################################################################
#Esta função irá ler o ficheiro input. Em principio, apos receber o ficheiro
#ira automaticamente exibir o grafico
##############################################################################
def FileReader(): 

    domain = (('text files', '*.mca'), ('all files', '*.*'))
    filename = fd.askopenfilename(title = 'Open a file', initialdir = '.', filetypes = domain)
    ###########INSERIR JANELA QUE NAO PERMITE FICHEIROS QUE NAO SEJAM MCA 
    OpenFile = open(filename, 'r')
    file = OpenFile.read()
    OpenFile.close()
    file = file.splitlines()
    Plot(file, filename)

##################################################################
#Primeiro Algoritmo!
# Muito WIP
##################################################################
def NRMethod(Peaks):

    Text = open("Data.txt", "r")
    Counts = Text.read()
    Text.close()
    Counts = Counts.splitlines()
    Counts.reverse()
    Channel = []

    for i in range(len(Counts)):
        Counts[i] = float(Counts[i])
        Channel.append(i+1)

    Channel.reverse()
    i = 0
    
    Threshold = 50

    Aux = [[0]]*Peaks   #[ [], [], ..., [] ]
    Temp = []
    
    for i in range(len(Counts)):
        if Counts[i] > Threshold:
            Temp.append(Counts[i])
        if Counts[i] <= Threshold:
            Temp.append(0)

    Counts.clear()
    j = 0
    i = 0

    for i in range(len(Temp)-1):
        
        if j == Peaks:
                break
        
        elif Temp[i] == 0 and Temp[i+1] != 0:
            print(Temp[i])
            Aux[j].append(Temp[i+1])
            #Counts.append(Channel[i])´

        elif Temp[i] != 0 and Temp[i+1] != 0:
            print(Temp[i])
            Aux[j].append(Temp[i+1])

        elif Temp[i] != 0 and Temp[i+1] == 0:
            print(Temp[i])
            j = j + 1
            
        elif Temp[i] == 0 and Temp[i+1] == 0:
            print(Temp[i])
            ()
           
    print(Aux)

    j = 0

    Channel.clear()

    for j in range(Peaks):
        Channel.append(max(Aux[j]))
        print(Channel[j])



def Method(self):
    Type = Menu.get()
    tk.Label(master = DataFrame, text = Type + "\n", bg = 'white').grid(row = 1, columnspan = 2)


###########################################################################
#Funcao em desenvolvimento... Ira ser a funçao que decide qual o algoritmo
#a ser utilizado na analise dos dados WIP
###########################################################################
def Analysis():       

    Method = Menu.get()
    Peaks = int(PeaksInput.get())


    if Peaks != 0:

        if Method == 'Noise Remover':
            NRMethod(Peaks)

    else:
        Warning = tk.Tk()
        tk.Label(Warning, text = 'No Information of the Number of Peaks was Submited \n').grid()
        tk.Label(Warning, text = 'Please Insert the Number of Peaks\n').grid()
        tk.Button(Warning, text = 'Return', command = Warning.destroy).grid()

    #for i in range(int(PeaksInput.get())):
        #tk.Label(DataFrame, text = 'Peak ' + str(i + 1) + ':').grid(row = i + 3, column = 0)
        #tk.Label(DataFrame, relief = 'sunken', text = i + 4.5, borderwidth = 2, bg = 'white').grid(row = i + 3, column = 1)


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
main.columnconfigure(0, weight = 3)
main.columnconfigure(1, weight = 0)
main.columnconfigure(2, weight = 2)

######################## FRAMES #################################


    #Frame dos ícones ferramentas
ToolbarFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge') 
ToolbarFrame.grid(column = 0, row = 0, sticky = "nw")

    #Frame das Tabs
TabFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
TabFrame.grid(column = 2, row = 0, sticky = 'ne')

    #Frame para o Gráfico
GraphicFrame = tk.Frame(main, borderwidth = 5, relief = 'ridge')
GraphicFrame.grid(column = 0, row = 1, sticky = "nw", pady = 5, columnspan = 2)


    #Frame para os Dados
DataFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
DataFrame.grid(column = 2, row = 1, sticky = "ne")
DataFrame.columnconfigure(0, weight = 1)
DataFrame.columnconfigure(1, weight = 1)
DataFrame.grid_propagate(True)


#################### Tabs ########################

Tab = ttk.Notebook(TabFrame)
Tab.grid(sticky = "w")
CalibFrame = tk.Frame(TabFrame, borderwidth = 5, relief ='sunken', bg = 'blue', height = 1 )
CalibFrame.grid()
Tab.add(CalibFrame, text = 'Calib Trial')

#################### ENTRIES ###########################

tk.Label(DataFrame, text = 'Analysis Method Selected: \n').grid(row = 0, columnspan = 2)

tk.Label(DataFrame, text = 'Please Input Number of Peaks: \n').grid(row = 2, columnspan = 2)
PeaksInput = tk.StringVar()
PeaksInput.set('0')
Entry = tk.Entry(DataFrame, textvariable = PeaksInput, relief = 'sunken',
                  borderwidth = 2, bg = 'white').grid(row = 3, columnspan= 2)


##################### BUTOES #######################
    
    #Botao para chamar o menu de Upload do ficheiros
    
tk.Button(ToolbarFrame, text = "Insert Files" , command = FileReader, height = 1).grid(column = 0, row = 0)

    #Menu Dropwdown das Ferramentas de análise
Menu = tk.StringVar()
Menu.set("Select Analysis Method")
Options = ["Peak-Input", "Noise Remover", "Manual Selection"]
tk.OptionMenu(ToolbarFrame, Menu, *Options, command = Method).grid(column = 1, row = 0)
    
    #Botão de Começo da Análise
tk.Button(ToolbarFrame, text = 'Run', height = 1, command = Analysis).grid(column = 2, row = 0)

    #Botão de Download dos Dados
tk.Button(ToolbarFrame, text = 'Download', height = 1).grid(column = 3, row = 0)

    #Botão de Separador Novo de Análise (Para os Filmes)
tk.Button(ToolbarFrame, text = 'New Trial', height = 1, command = Tabs).grid(column = 4, row = 0)

    #Botão de Voltar ao Menu Principal
tk.Button(ToolbarFrame, text = 'Return to Main Menu', height = 1).grid(column = 5, row = 0)


##################### MAINLOOP ####################

    #Mainloop mantém a janela do GUI aberta.
main.mainloop() 
