####################################################################
# Por enquanto não se utilizam todas estas bibliotecas
#Mas irão ser necessárias (provavelmente)
####################################################################

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

########## Ajusta-se ao ecra e foca os widgets ######
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

#####################################################

class Essential():
    def __init__(self):

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


################################################################
#Toda esta secçao define as estruturas presentes na janela
#A maior parte dos widgets têm comentarios para explicar o contexto
###################################################################
main = tk.Tk() #Janela Principal
main.state('zoomed')
main.title("AEL Thin Film Characterization")
window = Essential()

##################### MAINLOOP ####################

    #Mainloop mantém a janela do GUI aberta.
main.mainloop() 