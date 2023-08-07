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

#############################################
# Esta funcao recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI.
# Ao mesmo tempo cria um txt para outras funções
# acederem aos dados
#############################################
def Plot(File, Name):

    Channel = []    #Lista vazia para guardar o Channel
    Counts = []     #Lista vazia para guardar os Counts

    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

    for widgets in TabType[num].GraphicFrame.winfo_children():
        widgets.destroy()         # Este 'for' destroi grafcos antigos e constoi novos

    Data = open("Data.txt", "w")

    if Name[-4:] == ".mca":         #Por enquanto esta configurado para os ficheiros 
                                    # da maquina para AEL. Se for configurado RBS
                                    #ha-de-se incluir outro if.
        for i in range(12, len(File) - 1):  
            Counts.append(float(File[i]))
            Channel.append(i-11)
            Data.write(str(Counts[i-12])+"\n")

        # Ciclo for para adquirir os valores dos dados

    Data.close()

    figure = Figure(figsize = (6,4), dpi = 100) #A figura contem o grafico
    figure_canvas = FigureCanvasTkAgg(figure, TabType[num].GraphicFrame) #A class FigureCanvasTkAgg
    #liga o matplotlib ao tkinter

    NavigationToolbar2Tk(figure_canvas, TabType[num].GraphicFrame) # Esta linha permite que as ferramentas
    #do matplotlip aparecam na interface do tkinter

    #Aqui inicia-se o grafico com os dados e os eixos
    axes = figure.add_subplot() #
    axes.plot(Channel, Counts, 'D')
    axes.set_title("Calibration Run")
    axes.set_xlabel('Channel')
    axes.set_ylabel('Counts')

    #Por fim, acrescenta-se a geometria do tkinter
    figure_canvas.get_tk_widget().pack()


  
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
        Notebook.notebook.hide(14)

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
        __file_menu.add_command(label = 'Upload Plotting Data', command = FileReader)
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
        __tabs_menu.add_command(label = 'Add Calibration Tab', command = lambda: Tabs.tab_change(1))
        __tabs_menu.add_command(label = 'Add Material Tab', command = lambda: Tabs.tab_change(2))
        __tabs_menu.add_separator()
        __tabs_menu.add_command(label = 'Remove Current Tab')

            # Corre o algoritmo
        menu.add_command(label = 'Run')

            # Abre o ficheiro Help
        menu.add_command(label = "Help")

    def run(self):
        #### O metodo que permite o programa manter-se aberto
        self.main.mainloop()

class Warnings:
    def popup(self, name):

        self.warning = tk.Toplevel(window.main)
        self.warning.title(name)
        self.warning.geometry('700x300')
        self.warning.grab_set()

class Tabs:

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

    def CalibTab(self):
        TabFrame[Notebook.value].columnconfigure(0, weight= 3)
        TabFrame[Notebook.value].columnconfigure(1, weight = 1)
        TabFrame[Notebook.value].columnconfigure(2, weight = 2)
        TabFrame[Notebook.value].rowconfigure(0, weight = 4)
        TabFrame[Notebook.value].rowconfigure(1, weight = 1)
        self.GraphicFrame = tk.Frame(TabFrame[Notebook.value], borderwidth = 5, relief = 'ridge')
        self.GraphicFrame.grid(column = 0, row = 0, sticky = "nw", pady = 5, columnspan = 2)

        self.DataFrame = tk.Frame(TabFrame[Notebook.value], borderwidth = 5, relief = 'ridge')
        self.DataFrame.grid(column = 2, row = 0, sticky = "ne", pady = 5)
        tk.Label(self.DataFrame, text = 'Hallo').grid()
        
        
    def MatTab(self):
        TabFrame[Notebook.value].columnconfigure(0, weight= 3)
        TabFrame[Notebook.value].columnconfigure(1, weight = 1)
        TabFrame[Notebook.value].columnconfigure(2, weight = 2)
        TabFrame[Notebook.value].rowconfigure(0, weight = 4)
        TabFrame[Notebook.value].rowconfigure(1, weight = 1)
        self.GraphicFrame = tk.Frame(TabFrame[Notebook.value], borderwidth = 5, relief = 'ridge')
        self.GraphicFrame.grid(column = 0, row = 0, sticky = "nw", pady = 5, columnspan = 2)
        

    @staticmethod
    def tab_change(num):

        index = len(Notebook.notebook.tabs()) - 1

        if num == 3:

            Notebook.notebook.select(index - 1)
            wng.warning.destroy()
            

        elif num == 1:
            
            TabType[Notebook.value].CalibTab()
            Notebook.notebook.insert(index, TabFrame[Notebook.value], text = "Calibration Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()

            
        elif num == 2:

            TabType[Notebook.value].MatTab()
            Notebook.notebook.insert(index, TabFrame[Notebook.value], text = "Material Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()


window = Skeleton()
Notebook = Tabs()
Notebook.First_Tabs()
wng = Warnings()

############## Tabs variaveis para serem criadas ###############

tab1 = tk.Frame(Notebook.notebook)
tab2 = tk.Frame(Notebook.notebook)
tab3 = tk.Frame(Notebook.notebook)
tab4 = tk.Frame(Notebook.notebook)
tab5 = tk.Frame(Notebook.notebook)
tab6 = tk.Frame(Notebook.notebook)
tab7 = tk.Frame(Notebook.notebook)
tab8 = tk.Frame(Notebook.notebook)
tab9 = tk.Frame(Notebook.notebook)
tab10 = tk.Frame(Notebook.notebook)
tab11 = tk.Frame(Notebook.notebook)
tab12 = tk.Frame(Notebook.notebook)
tab13 = tk.Frame(Notebook.notebook)

TabFrame = [tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, 
       tab9, tab10, tab11, tab12, tab13]

tabtype1 = Tabs()
tabtype2 = Tabs()
tabtype3 = Tabs()
tabtype4 = Tabs()
tabtype5 = Tabs()
tabtype6 = Tabs()
tabtype7 = Tabs()
tabtype8 = Tabs()
tabtype9 = Tabs()
tabtype10 = Tabs()
tabtype11 = Tabs()
tabtype12 = Tabs()
tabtype13 = Tabs()

TabType = [tabtype1, tabtype2, tabtype3, tabtype4, tabtype5, tabtype6, 
           tabtype7, tabtype8, tabtype9, tabtype10, tabtype11, tabtype12, tabtype13]

##############################################################

window.run()
