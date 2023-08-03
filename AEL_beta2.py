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

    if Notebook.notebook.select() == Notebook.notebook.tabs()[-1] and len(Notebook.notebook.tabs()) < 15:
            
        wng.popup('Tab Selector Menu')

        tk.Label(wng.warning, text = 'Please Select New Type of Tab to Open \n').pack()
        tk.Button(wng.warning, command = lambda: Tabs.tab_change(1), 
                        text = 'Calibration Trial').pack()
        tk.Button(wng.warning, command = lambda: Tabs.tab_change(2), 
                        text = 'Material Trial').pack()
        tk.Label(wng.warning, text ='\n').pack()
        tk.Button(wng.warning, text = 'Return',
                    command = lambda : Tabs.tab_change(3)).pack()

    elif len(Notebook.notebook.tabs()) >= 15:
        Notebook.notebook.forget(14)


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
        __file_menu = tk.Menu(menu, tearoff = False) 
        menu.add_cascade(label = 'File', menu = __file_menu)
        __file_menu.add_command(label = 'Upload Plotting Data')
        __file_menu.add_command(label = 'Remove Current Plotting Data')
        __file_menu.add_command(label = 'Remove Algorithm Results')
        __file_menu.add_separator()
        __file_menu.add_command(label = "Save Results")
        __file_menu.add_command(label = "Delete Trial")
        __file_menu.add_command(label = "Manage Alpha Particles Source Values")
        __file_menu.add_separator()
        __file_menu.add_command(label = 'Exit Program', command = self.main.quit)

            # Indica ao programa qual a fonte de particulas alfa
        __source_menu = tk.Menu(menu, tearoff = False)
        menu.add_cascade(label = 'Alpha Particles Source', menu = __source_menu)
        __source_menu.add_radiobutton(label = "Ra 226")
        __source_menu.add_radiobutton(label = "Ur 232")

            # Indica ao programa qual o algoritmo a correr
        __algorithm_menu = tk.Menu(menu, tearoff = False)
        menu.add_cascade(label = 'Algorithm', menu = __algorithm_menu)
        __algorithm_menu.add_radiobutton(label = "Manual Selection")
        __algorithm_menu.add_radiobutton(label = "Threshold Input")

            # Gere as tabs do programa
        __tabs_menu = tk.Menu(menu, tearoff = False)
        menu.add_cascade(label = 'Manage Tabs', menu = __tabs_menu)
        __tabs_menu.add_command(label = 'Add Calibration Tab')
        __tabs_menu.add_command(label = 'Add Material Tab')
        __tabs_menu.add_separator()
        __tabs_menu.add_command(label = 'Remove Current Tab')

            # Corre o algoritmo
        menu.add_command(label = 'Run')

            # Abre o ficheiro Help
        menu.add_command(label = "Help")

    def run(self):
        #### O metodo que permite o programa manter-se aberto
        self.main.mainloop()

class Warnings():
    def popup(self, name):

        self.warning = tk.Toplevel(window.main)
        self.warning.title(name)
        self.warning.geometry('700x300')
        self.warning.grab_set()

class Tabs():

    def First_Tabs(self):

        ####### A variavel do Notebook ##########
        self.notebook = ttk.Notebook(window.main)   
        self.notebook.pack(expand = True, fill = 'both') # Expande a frame da tab ate ao final
                                                         # da janela
        self.notebook.enable_traversal() # Permite o uso de Ctrl+Tab para circular entre tabs
        
        ########### As frames principais - Os resultados e a frame de adicionar
        self.CRFrame = tk.Frame(self.notebook, bg = 'dark grey')
        self.PlusFrame = tk.Frame(self.notebook)
        
        ############# Aqui adicionam-se as frames iniciadas acima
        self.notebook.add(self.CRFrame, text = 'Final Results')
        self.notebook.add(self.PlusFrame, text = '+')

        ########### Variavel para contar o numero de separadores 
        self.value = 0

        ############ Este comando adiciona o evento a funcao, para adicionar frames
        self.notebook.bind("<<NotebookTabChanged>>", handleTabChange)      


    @staticmethod
    def tab_change(num):

        index = len(Notebook.notebook.tabs()) - 1
        Tab[Notebook.value] = tk.Frame(Notebook.notebook)

        if num == 3:

            Notebook.notebook.select(index - 1)
            wng.warning.destroy()
            

        elif num == 1:

            Notebook.notebook.insert(index, Tab[Notebook.value], text = "Calibration Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()

            
        elif num == 2:

            Notebook.notebook.insert(index, Tab[Notebook.value], text = "Material Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()


window = Skeleton()
Notebook = Tabs()
Notebook.First_Tabs()
wng = Warnings()

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

Tab = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, 
       tab9, tab10, tab11, tab12, tab13]

##############################################################

""" GraphicFrame_Calib = tk.Frame(Notebook.CTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Calib.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Calib, text = 'Calibration').grid(row = 0)

GraphicFrame_Material = tk.Frame(Notebook.MTFrame, borderwidth = 5, relief = 'ridge')
GraphicFrame_Material.grid(column = 0, row = 0, sticky = "nw", pady = 5)
tk.Label(GraphicFrame_Material, text = 'Material').grid(row = 0) """

window.run()
