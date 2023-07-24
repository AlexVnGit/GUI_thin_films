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

########## Ajusta-se ao ecrã e foca os widgets ######
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

#####################################################

##########################################################
# Funcao para os botoes do MATPLOTLIB funcionarem no widget
###########################################################
def on_key_event(event, canvas, toolbar):
    matplotlib.backend_bases.key_press_handler(event, canvas, toolbar)

###########################################################
# Funcao para eliminar entries e labels dentro da frame
###########################################################

def ClearData():
    for widget in ResultFrame.winfo_children():
        widget.destroy()
    ResultFrame.grid_remove()

#############################################
# Esta funcao recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI.
# Ao mesmo tempo cria um txt para outras funções
# acederem aos dados
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
#Esta função irá ler o ficheiro input.
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

def Regression(xvalues):

    avgx = average(xvalues)
    OpenFile = open("226_Ra.txt")
    yvalues = OpenFile.read()
    OpenFile.close()
    yvalues = yvalues.splitlines()
    
    for i in range(len(xvalues)):
        yvalues[i] = float(yvalues[i])

    avgy = average(yvalues)
    Placeholder1 = 0
    Placeholder2 = 0
    i = 0

    for i in range(len(xvalues)):
        Placeholder1 = Placeholder1 + ((xvalues[i] - avgx) * (yvalues[i] - avgy))
        Placeholder2 = Placeholder2 + (xvalues[i] - avgx)**2
    
    m = Placeholder1 / Placeholder2
    b = avgy - m * avgx

    tk.Label(LinearFrame, text = "Slope: " + str(m)).grid()
    tk.Label(LinearFrame, text = "Y-Axis Intersect: " + str(b)).grid()



##################################################################
#Primeiro Algoritmo! Estabelece o Threshold e seleciona os picos
##################################################################
def ThresholdM(Peaks):

    Text = open("Data.txt", "r")
    List1 = Text.read()
    Text.close()
    List1 = List1.splitlines()
    List1.reverse()
    List2 = []

    for i in range(len(List1)):
        List1[i] = float(List1[i])
        List2.append(i+1)

    List2.reverse()
    i = 0
    Threshold = 50
    j = 0

    ########## O ARRAY TEM QUE SER DEFINIDO ASSIM PARA 
    # CADA LISTA DENTRO DA LISTA SEJA INDEPENDENTE
    #EXPLICACAO:
    #https://www.geeksforgeeks.org/python-using-2d-arrays-lists-the-right-way/
    Yaxis = [[0 for i in range(1)] for j in range (Peaks)]   #[ [], [], ..., [] ]
    Xaxis = [[0 for i in range(1)] for j in range (Peaks)]

    Temp = []
    
    for i in range(len(List1)):
        if List1[i] > Threshold:
            Temp.append(List1[i])
        if List1[i] <= Threshold:
            Temp.append(0)

    List1.clear()
    j = 0
    i = 0

    for i in range(len(Temp)-1):
        
        if j == Peaks:
                break
        
        elif Temp[i] == 0 and Temp[i+1] != 0:
            
            Yaxis[j].append(Temp[i+1])
            Xaxis[j].append(List2[i+1])

        elif Temp[i] != 0 and Temp[i+1] != 0:

            Yaxis[j].append(Temp[i+1])
            Xaxis[j].append(List2[i+1])


        elif Temp[i] != 0 and Temp[i+1] == 0:

            j = j + 1
            
        elif Temp[i] == 0 and Temp[i+1] == 0:
            
            ()    
           
    j = 0
    i = 0

    Temp.clear()
    List2.clear()
    
    tk.Label(ResultFrame, text = "Peaks \t Counts \t Channel", 
                     font = 14).grid(row = 0, columnspan = 2)

    for j in range(Peaks):
        Temp.append(int(max(Yaxis[j]))) ###Guarda os Maximos

        i = Yaxis[j].index(max(Yaxis[j])) ###Guarda o indice dos Maximos
        List2.append(Xaxis[j][i])      ###Devolve o número do canal Correspondente
                                        # ao maximo

        tk.Label(ResultFrame, text = "Peak " + str(Peaks - j) + ":\t" + 
                            str(Temp[j]) + "\t" + str(List2[j])).grid(columnspan = 2)
    
    Linearize = tk.Button(ResultFrame, text = "Linearize", 
              command = Regression(List2))
    Linearize.grid(row = 2 + j, column = 0)
    
    tk.Button(ResultFrame, text = "Clear Data", 
              command = ClearData).grid(row = 2 + j, column = 1)


###########################################################
# Atualiza o algoritmo a ser utilizado, para informar
# o utilizador
############################################################

def Method(*args):
    Type = Menu.get()
    MethodLabel.config(text = Type)



###########################################################################
#Funcao em desenvolvimento... Ira ser a funçao que decide qual o algoritmo
#a ser utilizado na analise dos dados WIP
###########################################################################
def Analysis():       

    Method = Menu.get()
   
    Peaks = int(PeaksInput.get())
    ClearData()
    ResultFrame.grid()


    if Peaks != 0:

        if Method == 'Gaussian Fit':
            #GaussM(Peaks)
            ()

        elif Method == 'Threshold-Input':
            ThresholdM(Peaks)

        elif Method == 'Manual Selection':
            ()
            #ManualSM(Peaks)        
        

    elif Peaks == 0 or Peaks == None:
        Warning = tk.Tk()
        tk.Label(Warning, text = 'No Information of the Number of Peaks was Submited \n').grid()
        tk.Label(Warning, text = 'Please Insert the Number of Peaks\n').grid()
        tk.Button(Warning, text = 'Return', command = Warning.destroy).grid()

    #for i in range(int(PeaksInput.get())):
        #tk.Label(DataFrame, text = 'Peak ' + str(i + 1) + ':').grid(row = i + 3, column = 0)
        #tk.Label(DataFrame, relief = 'sunken', text = i + 4.5, borderwidth = 2, bg = 'white').grid(row = i + 3, column = 1)


###############################################################
# Funcao para abrir novas Tabs, MUITO WIP
################################################################
def Tabs():

    test2 = tk.Frame(TabFrame, borderwidth = 5, relief = 'sunken', bg = 'red', height = 1)
    test2.grid()
    Tab.add(test2, text = 'Trial 1')
    

################################################################
#Toda esta secçao define as estruturas presentes na janela
#A maior parte dos widgets têm comentarios para explicar o contexto
###################################################################
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

    #Frame para os Resultados do Algoritmo
    #Encontra-se dentro da DataFrame
ResultFrame = tk.LabelFrame(master = DataFrame)
ResultFrame.grid(row = 5, columnspan = 2, pady = 5)
ResultFrame.columnconfigure(0, weight = 1)
ResultFrame.columnconfigure(1, weight = 1)

    #Frame para os Dados Linearizados
LinearFrame = tk.LabelFrame(master = DataFrame)
LinearFrame.grid(row = 6, columnspan = 2, pady = 5)
LinearFrame.columnconfigure(0, weight = 1)
LinearFrame.columnconfigure(1, weight = 1)

#################### Tabs ########################

Tab = ttk.Notebook(TabFrame)
Tab.grid(sticky = "w")
CalibFrame = tk.Frame(TabFrame, borderwidth = 5, relief ='sunken', bg = 'blue', height = 1 )
CalibFrame.grid()
Tab.add(CalibFrame, text = 'Calib Trial')

#################### ENTRIES E LABELS ########################

tk.Label(DataFrame, text = 'Analysis Method Selected: ').grid(row = 0, columnspan = 2)

tk.Label(DataFrame, text = 'Please Input Number of Peaks: \n').grid(row = 2, columnspan = 2)
PeaksInput = tk.StringVar()
PeaksInput.set('0')
Entry = tk.Entry(DataFrame, textvariable = PeaksInput, relief = 'sunken',
                  borderwidth = 2).grid(row = 3, columnspan= 2)
MethodLabel = tk.Label(DataFrame, text = "\n")
MethodLabel.grid(row = 1, columnspan = 2)



##################### BUTOES #######################
    
    #Botao para chamar o menu de Upload do ficheiros
    
tk.Button(ToolbarFrame, text = "Insert Files" , command = FileReader, height = 1).grid(column = 0, row = 0)

    #Menu Dropwdown das Ferramentas de análise
Menu = tk.StringVar()
Menu.set("Select Analysis Method")
Options = ["Gaussian Fit", "Threshold-Input", "Manual Selection"]
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
