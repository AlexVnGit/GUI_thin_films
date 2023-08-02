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

######################################################

def handleTabChange(event):

    Tabs.tab_add(Notebook.value)

class Skeleton:

    def __init__(self):

        ############# A Janela Mae ##############

        self.main = tk.Tk()
        self.main.title('ARC_TF')
        self.main.state('zoomed')
        self.main.configure(background = 'dark grey')

        ############## A barra de Ferramentas e opcoes #################
    
        menu = tk.Menu(self.main)
        self.main.config(menu = menu)

            # O tipico File Menu. Hao de haver mais opcoes no futuro
        file_menu = tk.Menu(menu, tearoff = False) 
        menu.add_cascade(label = 'File', menu = file_menu)
        file_menu.add_command(label = 'Upload Data')
        file_menu.add_command(label = 'Run')
        file_menu.add_separator()
        file_menu.add_command(label = "Save Data")
        file_menu.add_command(label = "Delete Trial")
        file_menu.add_command(label = "Manage Alpha Particles Source Values")
        file_menu.add_separator()
        file_menu.add_command(label = "Help")

            # Indica ao programa qual a fonte de particulas alfa
        source_menu = tk.Menu(menu, tearoff = False)
        menu.add_cascade(label = 'Alpha Particles Source', menu = source_menu)
        source_menu.add_radiobutton(label = "Ra 226")
        source_menu.add_radiobutton(label = "Ur 232")

            # Indica ao programa qual o algoritmo a correr
        algorithm_menu = tk.Menu(menu, tearoff = False)
        menu.add_cascade(label = 'Algorithm', menu = algorithm_menu)
        algorithm_menu.add_radiobutton(label = "Manual Selection")
        algorithm_menu.add_radiobutton(label = "Threshold Input")

    def run(self):
        self.main.mainloop()

class Tabs():


    def First_Tabs(self):

        ####### A variavel do Notebook ##########

        self.value = 0

        self.notebook = ttk.Notebook(window.main)   
        self.notebook.pack(expand = True, fill = 'both')    
        self.notebook.enable_traversal()
        
        """ Cada tab do Notebook vai ter uma frame que ocupa a janela na sua
            totalidade. Assim temos a CTFrame para os dados de calibracao;
            a MTFrame para os dados de ensaios das peliculas, e a
            CRFrame que aglomera todos os resulados finais obtidos. """
        
        """ self.CTFrame = tk.Frame(self.notebook, bg = 'blue')
        self.MTFrame = tk.Frame(self.notebook, bg = 'red') """
        self.CRFrame = tk.Frame(self.notebook, bg = 'dark grey')
        self.PlusFrame = tk.Frame(self.notebook)
        
        
        """ self.notebook.add(self.CTFrame, text = 'Calibration Trials')
        self.notebook.add(self.MTFrame, text = 'Material Trials') """
        self.notebook.add(self.CRFrame, text = 'Final Results')
        self.notebook.add(self.PlusFrame, text = '+')

    @staticmethod
    def tab_add(num):
        if Notebook.notebook.select() == Notebook.notebook.tabs()[-1] and len(Notebook.notebook.tabs()) < 17:
            index = len(Notebook.notebook.tabs()) - 1
            Tab[num] = tk.Frame(Notebook.notebook)
            print(Tab[num])
            Notebook.notebook.insert(index, Tab[num], text = "teste")
            Notebook.notebook.select(index)    
            Notebook.value = Notebook.value + 1



window = Skeleton()
Notebook = Tabs()
Notebook.First_Tabs()

############## Tabs variaveis para serem criadas ###############

tab1 = Tabs()
tab2 = Tabs()
tab3 = Tabs()
tab4 = Tabs()
tab5 = Tabs()
tab6 = Tabs()
tab7 = Tabs()
tab8 = Tabs()
tab9 = Tabs()
tab10 = Tabs()
tab11 = Tabs()
tab12 = Tabs()
tab13 = Tabs()
tab14 = Tabs()
tab15 = Tabs()

Tab = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12,
       tab13, tab14, tab15]

Notebook.notebook.bind("<<NotebookTabChanged>>", handleTabChange)

##############################################################

""" GraphicFrame_Calib = tk.Frame(Notebook.CTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Calib.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Calib, text = 'Calibration').grid(row = 0)

GraphicFrame_Material = tk.Frame(Notebook.MTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Material.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Material, text = 'Material').grid(row = 0) """

window.run()
