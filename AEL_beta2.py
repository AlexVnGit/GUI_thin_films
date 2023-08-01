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

class Skeleton:

    def __init__(self):

        ############# A Janela Mae ##############

        self.main = tk.Tk()
        self.main.title('ARC_TF')
        self.main.state('zoomed')
        self.main.configure(background = 'dark grey')

        ####### A variavel do Notebook ##########

        self.notebook = ttk.Notebook(self.main)   
        self.notebook.pack(expand = True, fill = 'both')    
        self.notebook.enable_traversal()

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


        """ Cada tab do Notebook vai ter uma frame que ocupa a janela na sua
            totalidade. Assim temos a CTFrame para os dados de calibracao;
            a MTFrame para os dados de ensaios das peliculas, e a
            CRFrame que aglomera todos os resulados finais obtidos. """
        
        self.CTFrame = tk.Frame(self.notebook, bg = 'blue')
        self.MTFrame = tk.Frame(self.notebook, bg = 'red')
        self.CRFrame = tk.Frame(self.notebook, bg = 'green')
        
        
        self.notebook.add(self.CTFrame, text = 'Calibration Trials')
        self.notebook.add(self.MTFrame, text = 'Material Trials')
        self.notebook.add(self.CRFrame, text = 'Calculated Results')


    def run(self):
        self.main.mainloop()


window = Skeleton()

GraphicFrame_Calib = tk.Frame(window.CTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Calib.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Calib, text = 'Calibration').grid(row = 0)

GraphicFrame_Material = tk.Frame(window.MTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Material.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Material, text = 'Material').grid(row = 0)

window.run()
