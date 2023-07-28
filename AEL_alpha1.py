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

def ClearData(Value):

    if Value == 0:
        for widget in ResultFrame.winfo_children():
            widget.destroy()
        ResultFrame.grid_remove()
    elif Value == 1:
        for widget in LinearFrame.winfo_children():
            widget.destroy()
        LinearFrame.grid_remove()
    elif Value == 2:
        for widget in DecayFrame.winfo_children():
            widget.destroy()
        DecayFrame.grid_remove()

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

    fig = Figure()
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
#Esta funcao ira ler o ficheiro input.
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

#############################################################################
#Esta funcao ira fazer a regressao linear da fonte com os canais
#############################################################################
def Regression(xvalues):

    ClearData(1)
    LinearFrame.grid(row = 6, pady = 5, padx = 5, columnspan = 2, sticky = 's')
    LinearFrame.columnconfigure(0, weight = 1)
    LinearFrame.columnconfigure(1, weight = 1)

    avgx = average(xvalues)
    Placeholder = []

    for i in range(len(Decay)):
        Placeholder.append(float(Decay[i].get()))
  
    yvalues = []
    i = 0
    for i in range(len(Decay)):
        if Placeholder[i] != 0:
            yvalues.append(Placeholder[i])
    
    if len(yvalues) != len(xvalues):

        RegWarn = tk.Toplevel(main)
        RegWarn.title("Warning")
        RegWarn.geometry("700x300")
        RegWarn.grab_set()
        tk.Label(RegWarn, text = "Number of Radiation Decay does not " + 
                 "match the number of Peaks detected.\n").pack()
        tk.Label(RegWarn, text = "Please adjust the Peak Algorithm or the " +
                 "number of Decay Energy.\n\n").pack()
        tk.Button(RegWarn, text = "Return", command = lambda : RegWarn.destroy()).pack()
        ClearData(1)

    else:
        Placeholder.clear()

        avgy = average(yvalues)
        Placeholder1 = 0
        Placeholder2 = 0
        i = 0

        for i in range(len(xvalues)):
            Placeholder1 = Placeholder1 + ((xvalues[i] - avgx) * (yvalues[i] - avgy))
            Placeholder2 = Placeholder2 + (xvalues[i] - avgx)**2
    
        m = Placeholder1 / Placeholder2
        b = avgy - m * avgx

        tk.Label(LinearFrame, text = "Slope: " + str(m)).grid(row = 0, columnspan = 2)
        tk.Label(LinearFrame, text = "Y-Axis Intersect: " + str(b)).grid(row = 1, columnspan = 2)

        tk.Button(LinearFrame, text = "Save Data").grid(row = 2, column = 0)
        tk.Button(LinearFrame, text = "Clear Data", 
                command = lambda : ClearData(1)).grid(row = 2, column = 1)

##################################################################
#Primeiro Algoritmo! Estabelece o Threshold e seleciona os picos
#Ha de ser melhorado com o algoritmo do Tomas. Para avancar
#noutros componentes, deixei a funcao antiga
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
        
    
    tk.Button(ResultFrame, text = "Linearize", 
              command = lambda : Regression(List2)).grid(row = 2 + j, column = 0)
    
    tk.Button(ResultFrame, text = "Clear Data", 
              command = lambda : ClearData(0)).grid(row = 2 + j, column = 1)

def ManualSel():

    Alpha = Source.get()

    if Alpha == 'Radium 226':
        ()

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
    ClearData(0)
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
        tk.Button(Warning, text = 'Return', command = lambda : Warning.destroy).grid()

#########################################################################
#Funcao que define a fonte de alfas a ser utilizada
##########################################################################
def SourceReader(*args):
    
    Alpha = Source.get()
    SourceLabel.config(text = Alpha + "\n")
    ClearData(2)
    DecayFrame.grid(row = 0, column = 1, ipadx = 5, ipady = 5, padx = 5, pady = 5)

    if Alpha == 'Radium 226':
        Radium1 = tk.Checkbutton(DecayFrame, onvalue = 7.68682, offvalue = 0,
                        text = '214 Po -> 210 Pb: 7,68682 MeV', variable = Decay[0])
        Radium1.grid(column = 0)
        Radium1.select()

        Radium2 = tk.Checkbutton(DecayFrame, onvalue = 6.00255, offvalue = 0,
                        text = '218 Po -> 214 Pb: 6,00255 MeV', variable = Decay[1])
        Radium2.grid(column = 0)
        Radium2.select()

        Radium3 = tk.Checkbutton(DecayFrame, onvalue = 5.48950, offvalue = 0,
                        text = '222 Rn -> 218 Po: 5,48950 MeV', variable = Decay[2])
        Radium3.grid(column = 0)
        Radium3.select()

        Radium4 = tk.Checkbutton(DecayFrame, onvalue = 5.30433, offvalue = 0,
                        text = '210 Po -> 206 Pb: 5,30433 MeV', variable = Decay[3])
        Radium4.grid(column = 0)
        Radium4.select()

        Radium5 = tk.Checkbutton(DecayFrame, onvalue = 4.77301, offvalue = 0,
                        text = '226 Ra -> 222 Rn: 4,77301 MeV', variable = Decay[4])
        Radium5.grid(column = 0)
        Radium5.select()

        Decay6.set('0')
        Decay7.set('0')

    elif Alpha == 'Uranium 232':
        Uranium1 = tk.Checkbutton(DecayFrame, onvalue = 8.78437, offvalue = 0,
                        text = '212 Po -> 208 Pb: 8,78437 MeV', variable = Decay[0])
        Uranium1.grid(column = 0)
        Uranium1.select()

        Uranium2 = tk.Checkbutton(DecayFrame, onvalue = 6.77830, offvalue = 0,
                        text = '216 Po -> 212 Pb: 6,77830 MeV', variable = Decay[1])
        Uranium2.grid(column = 0)
        Uranium2.select()

        Uranium3 = tk.Checkbutton(DecayFrame, onvalue = 6.28808, offvalue = 0,
                        text = '220 Rn -> 216 Po: 6,28808 MeV', variable = Decay[2])
        Uranium3.grid(column = 0)
        Uranium3.select()

        Uranium4 = tk.Checkbutton(DecayFrame, onvalue = 6.05107, offvalue = 0,
                        text = '212 Bi -> 208 Tl: 6,05107 MeV', variable = Decay[3])
        Uranium4.grid(column = 0)
        Uranium4.select()
        
        Uranium5 = tk.Checkbutton(DecayFrame, onvalue = 5.67339, offvalue = 0,
                        text = '224 Ra -> 220 Rn: 5,67339 MeV', variable = Decay[4])
        Uranium5.grid(column = 0)
        Uranium5.select()
        
        Uranium6 = tk.Checkbutton(DecayFrame, onvalue = 5.40050, offvalue = 0,
                        text = '228 Th -> 224 Ra: 5,40050 MeV', variable = Decay[5])
        Uranium6.grid(column = 0)
        Uranium6.select()

        Uranium7 = tk.Checkbutton(DecayFrame, onvalue = 5.30216, offvalue = 0,
                        text = '232 U  -> 228 Th: 5,30216 MeV', variable = Decay[6])
        Uranium7.grid(column = 0)
        Uranium7.select()

###############################################################
# Funcao para abrir novas Tabs, MUITO WIP
################################################################
def Tabs():

    test2 = ttk.Frame(Tab, borderwidth = 5, relief = 'sunken', height = 1)
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
main.columnconfigure(1, weight = 1)


######################## FRAMES #################################

    #Frame dos ícones ferramentas
ToolbarFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge') 
ToolbarFrame.grid(column = 0, row = 0, sticky = "nw", columnspan = 1)

    #Frame das Tabs
TabFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
TabFrame.grid(column = 4, row = 0, sticky = 'e')

    #Frame para o Gráfico
GraphicFrame = tk.Frame(main, borderwidth = 5, relief = 'ridge')
GraphicFrame.grid(column = 0, row = 1, sticky = "nw", pady = 5, columnspan = 2)


    #Frame para os Dados
DataFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge')
DataFrame.grid(column = 4, row = 1, sticky = "ne")
DataFrame.columnconfigure(0, weight = 1)
DataFrame.columnconfigure(1, weight = 1)
#DataFrame.columnconfigure(2, weight = 1)
DataFrame.rowconfigure(0, weight = 1)
DataFrame.rowconfigure(1, weight = 1)
DataFrame.rowconfigure(2, weight = 1)
DataFrame.rowconfigure(3, weight = 1)
#DataFrame.grid_propagate(True)

GoldenFrame = tk.LabelFrame(master = DataFrame, borderwidth = 0)
GoldenFrame.grid(row = 1, column = 0, columnspan = 2)

    #Frame para os Resultados do Algoritmo
    #Encontra-se dentro da DataFrame
ResultFrame = tk.LabelFrame(master = GoldenFrame, borderwidth = 0)
ResultFrame.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = 'nw')

    #Frame para o Algoritmo a ser usado
InfoFrame = tk.LabelFrame(master = DataFrame)
InfoFrame.grid(column = 0, row = 0, padx = 5, pady = 5, sticky = 'n')

    #Frame para os Dados Linearizados
LinearFrame = tk.LabelFrame(master = DataFrame)

    #Frame Mae para o Decaimento da Particula
DecayFrameMaster = tk.LabelFrame(master = DataFrame)
DecayFrameMaster.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'n')

    #Frame com informacoes sobre o Decaimento da Particula
DecayFrame = tk.LabelFrame(master = GoldenFrame, borderwidth = 0)


#################### Tabs ########################

Tab = ttk.Notebook(TabFrame)
Tab.grid(sticky = "w")
CalibFrame = ttk.Frame(Tab, borderwidth = 5, relief ='sunken', height = 1 )
CalibFrame.grid()
Tab.add(CalibFrame, text = 'Calib Trial')

#################### ENTRIES, LABELS E STRINGVAR########################

tk.Label(InfoFrame, text = 'Analysis Method Selected: ').grid(row = 0, columnspan = 2)
tk.Label(InfoFrame, text = 'Please Input Number of Peaks: \n').grid(row = 2, columnspan = 2)

PeaksInput = tk.StringVar()
PeaksInput.set('0')
Entry = tk.Entry(InfoFrame, textvariable = PeaksInput, relief = 'sunken',
                  borderwidth = 2).grid(row = 3, columnspan= 2)
MethodLabel = tk.Label(InfoFrame, text = "")
MethodLabel.grid(row = 1, columnspan = 2)

tk.Label(DecayFrameMaster, 
         text = '\n Source of Alpha Particles').grid(row = 0, columnspan = 1)
SourceLabel = tk.Label(DecayFrameMaster, text = '\n')
SourceLabel.grid(row = 1, columnspan = 1)

Decay1 = tk.StringVar()
Decay1.set('0')
Decay2 = tk.StringVar()
Decay2.set('0')
Decay3 = tk.StringVar()
Decay3.set('0')
Decay4 = tk.StringVar()
Decay4.set('0')
Decay5 = tk.StringVar()
Decay5.set('0')
Decay6 = tk.StringVar()
Decay6.set('0')
Decay7 = tk.StringVar()
Decay7.set('0')

Decay = [Decay1, Decay2, Decay3, Decay4, Decay5, Decay6, Decay7]

##################### BUTOES #######################
    
    #Botao para chamar o menu de Upload do ficheiros
    
tk.Button(ToolbarFrame, text = "Insert Files" , 
          command = FileReader, height = 1).grid(column = 0, row = 0)

    #Menu Dropwdown das Ferramentas de análise
Menu = tk.StringVar()
Menu.set("Select Analysis Method")
Options = ["Gaussian Fit", "Threshold-Input", "Manual Selection"]
tk.OptionMenu(ToolbarFrame, Menu, *Options, command = Method).grid(column = 1, row = 0)

    #Botão de Fonte da Partícula Alpha dos Dados
Source = tk.StringVar()
Source.set("Select Source File")
SourceList = ["Uranium 232", "Radium 226"]
tk.OptionMenu(ToolbarFrame, Source, *SourceList, command = SourceReader).grid(column = 3, row = 0)
    
    #Botão de Começo da Análise
tk.Button(ToolbarFrame, text = 'Run', height = 1, command = Analysis).grid(column = 2, row = 0)

    #Botão de Separador Novo de Análise (Para os Filmes)
tk.Button(ToolbarFrame, text = 'New Trial', height = 1, command = Tabs).grid(column = 4, row = 0)

    #Botão de Voltar ao Menu Principal
tk.Button(ToolbarFrame, text = 'Return to Main Menu', 
          height = 1, command = lambda : main.destroy()).grid(column = 5, row = 0)


##################### MAINLOOP ####################

    #Mainloop mantém a janela do GUI aberta.
main.mainloop() 
