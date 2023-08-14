####################################################################
# Por enquanto não se utilizam todas estas bibliotecas
#Mas irão ser necessárias (provavelmente)
####################################################################

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
#from PIL import ImageTk, Image
#from tkinter.messagebox import showinfo
#from matplotlib.pylab import *
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import os as os
import math

########## Ajusta-se ao ecra e foca os widgets ######
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
######################################################

#########################################################################################
# Apaga as widgets dentro de frames e tira a geometria de frames, para fazer renovacao
# de dados. Podera conter, eventualmente, mais frames do que contem agora
#########################################################################################
def ClearWidget(Frame):
    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

    if Frame == 'Graphic':
        for widgets in TabList[num][1].GraphicFrame.winfo_children():
            widgets.destroy()         # Este 'for' destroi grafcos antigos e constoi novos
        TabList[num][1].GraphicFrame.grid_remove()

    elif Frame == 'Algorithm':
        for widget in TabList[num][1].AlgFrame.winfo_children(): 
            widget.destroy() #Destroi a opcao de widgets anteriores dos algoritmos
    
    elif Frame == 'Results':
        for widget in TabList[num][1].ResultFrame.winfo_children():
            widget.destroy() #Destroi os resultados anteriores dos algoritmos
        TabList[num][1].ResultFrame.grid_remove()
        

    elif Frame == 'Everything':
        for widgets in TabList[num][1].GraphicFrame.winfo_children():
            widgets.destroy()         # Este 'for' destroi grafcos antigos e constoi novos
        widget = 0
        TabList[num][1].GraphicFrame.grid_remove()

        
        for widget in TabList[num][1].AlgFrame.winfo_children(): 
            widget.destroy() #Destroi a opcao de widgets anteriores dos algoritmos
        widget = 0
        TabList[num][1].AlgFrame.grid_remove()


        for widgets in TabList[num][1].ResultFrame.winfo_children():
            widgets.destroy()         # Este 'for' destroi grafcos antigos e constoi novos
        widget = 0
        TabList[num][1].ResultFrame.grid_remove()

#########################################################################################
# Recebe os resultados dos algoritmos e mostra no GUI
########################################################################################
def ResultManager(Counts, Channel):

    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

    ClearWidget('Results')
    TabList[num][1].ResultFrame.grid(row = 3, columnspan = 2, pady = 5)

    i = 0
    for i in range(len(Channel)):

        Channel[i] = int(Channel[i])

        tk.Checkbutton(TabList[num][1].ResultFrame, onvalue = Channel[i], 
                       text = 'Channel: ' + str(Channel[i])).grid(row = i , column = 0)
        tk.Label(TabList[num][1].ResultFrame, 
                 text = '\t Counts: ' + str(Counts[i])).grid(row = i , column = 1)

###############################################################################
# Este e o algoritmo que determina a distancia quadrada minima entre pontos
# input, e pontos de dados
###############################################################################
def ManSelec_Alg():

    Valuey = Mnl_selectiony.get() #Input dos counts
    Valuex = Mnl_selectionx.get() #Input do Channel

    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

    with open(TabList[num][2], "r") as file:   #Leitura do ficheiro
        Counts = [int(line) for line in file]   #Extracao dos counts

    AuxList = []   #Lista para guardar minimos quadrados

    for i in range(0, len(Counts)):
        AuxList.append(math.sqrt(((Valuey - Counts[i])**2)+((Valuex - i + 1)**2)))

    # O ciclo for guarda toda a distancia quadrado dos valores input e dos valores dos dados

    Valuex = AuxList.index(min(AuxList)) + 1 #Corresponde ao channel com distancia minima
    Valuey = Counts[Valuex - 1] #Corresponde ao count do indice do xvalue
    
    TabList[num][1].Results_List_x.append(Valuex)
    TabList[num][1].Results_List_y.append(Valuey)

    ResultManager(TabList[num][1].Results_List_y, TabList[num][1].Results_List_x)
    
###############################################################################
# Este e o algoritmo que regista os picos acima de um determinado threshold
###############################################################################
def Threshold_Alg():

    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

#Use "with open" it will close the file after reading, no need to close it manually
    with open(TabList[num][2], "r") as file:
        Counts = [int(line) for line in file]

    Threshold = Algorithm.get()
    yaxis = []
    current_peak_counts = 0
    current_peak = []
    counter = 0
    xaxis = []

#Just iterate of the values of the list itself. Each "count" is an element of Counts
    for count in (Counts):
       #Remember, if you hit a peak the condition 
       # will enter this part always. So the "current_peak_counts" will just 
       #add the total sum of the area under the peak 
       # (this may even be useful for FWHM calculations).
       
        if count > Threshold:
            current_peak_counts += count
            current_peak.append(count)

        else:

            counter += 1

            #Just checking that our current_peak list is not empty, 
            #if it is then we're out of a peak and this will just skip this if statment
            #but if it is not, then we're at the end of a peak 
            #(count is now <= Threshold) and we should save the max value of
            #current_peak and put everything to zero (aka move to the next peak)

            if current_peak:
                
                if len(current_peak) > 7: #Nota Importante abaixo
                    yaxis.append(max(current_peak))
                    xaxis.append(counter + current_peak.index(max(current_peak)))
                    counter = counter + len(current_peak)
                    current_peak_counts = 0
                    current_peak = []
                
# O parametro len(current_peak) > 7, serve para evitar um
# a falha do algoritmo. Por vezes,
# no algoritmo, ele considera picos com poucos pontos, o que traz como consequencia a consideracao
# de picos que sao apenas oscilacoes da estatistica.


    #If the last peak is not added because the data ends with a peak (could be a problem, you should check it)
    """ if current_peak:
        yaxis.append(max(current_peak))
        xaxis.append(counter + current_peak.index(max(current_peak)))
        counter = counter + len(current_peak)
        current_peak_counts = 0
        current_peak = [] """
    

    ResultManager(yaxis, xaxis)

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

    ClearWidget('Graphic')
    TabList[num][1].GraphicFrame.grid(column = 0, row = 0, sticky = "nw", pady = 5, columnspan = 2)

    Data = open(TabList[num][2], "w")

    if Name[-4:] == ".mca":         #Por enquanto esta configurado para os ficheiros 
                                    # da maquina para AEL. Se for configurado RBS
                                    #ha-de-se incluir outro if.
        for i in range(12, len(File) - 1):  
            Counts.append(int(File[i]))
            Channel.append(i-11)
            Data.write(str(Counts[i-12])+"\n")

        # Ciclo for para adquirir os valores dos dados

    Data.close()

    figure = Figure(figsize = (6,4), dpi = 100) #A figura contem o grafico
    figure_canvas = FigureCanvasTkAgg(figure, TabList[num][1].GraphicFrame) #A class FigureCanvasTkAgg
    #liga o matplotlib ao tkinter

    NavigationToolbar2Tk(figure_canvas, TabList[num][1].GraphicFrame) # Esta linha permite que as ferramentas
    #do matplotlip aparecam na interface do tkinter

    #Aqui inicia-se o grafico com os dados e os eixos
    axes = figure.add_subplot() 
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

##############################################################################
# Esta funcao gere o evento especifico de adicionar tabs, futuramente
# ira ter uma seccao especifica para esconder tabs e recuperar a tab
# de adicionar tabs, caso haja menos que 15 tabs
#############################################################################
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

##############################################################################
# Esta funcao altera a interface dos dados inputs para cada algoritmo
##############################################################################
def Method(*args):

    num = Notebook.notebook.select()  # Devolve o id da tab onde o utilizador se encontra
    num = num[-1]                     # Vai buscar o numero na string do id
    num = int(num) - 3                # Altera-se o valor para corresponder aos indices da lista

    ClearWidget('Algorithm')
    TabList[num][1].AlgFrame.grid(row = 2, columnspan = 2)

    decider = Algorithm_Method.get() #Devolve a StringVar que decide qual o algoritmo em uso

    if decider == 'Manual Selection':   #Definicao dos controlos para o algoritmo ManSelec_Alg
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Please input: ').grid(row = 2, columnspan = 2)
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Channel: ').grid(row = 3, column = 0)
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Counts: ').grid(row = 3, column = 1)
        tk.Entry(TabList[num][1].AlgFrame, textvariable = Mnl_selectionx, relief = 'sunken',
                  borderwidth = 2).grid(row = 4, column = 0)
        tk.Entry(TabList[num][1].AlgFrame, textvariable = Mnl_selectiony, relief = 'sunken',
                  borderwidth = 2).grid(row = 4, column = 1)
        tk.Button(TabList[num][1].AlgFrame, text = 'Search', 
                  command = ManSelec_Alg).grid(row = 5, column = 0)
        tk.Button(TabList[num][1].AlgFrame, text = 'Remove Data',
                  command = lambda: ClearWidget('Results')).grid(row = 5, column = 1)

    elif decider == 'Threshold Input':  #Definicao dos controlos para o algoritmo Threshold_Alg
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Please input Threshold: ').grid(row = 2, columnspan = 2)
        tk.Label(TabList[num][1].AlgFrame, 
                 text = '').grid(row = 3, columnspan = 2)
        tk.Entry(TabList[num][1].AlgFrame, textvariable = Algorithm, relief = 'sunken',
                  borderwidth = 2).grid(row = 4, columnspan= 2)
        tk.Button(TabList[num][1].AlgFrame,text = 'Search', 
                  command =  Threshold_Alg).grid(row = 5, column = 0)
        tk.Button(TabList[num][1].AlgFrame,text = 'Remove Data',
                  command = lambda: ClearWidget('Results')).grid(row = 5, column = 1)
        
    else: #Devolve um aviso para se selecionar um algoritmo
        wng.popup('Algorithm Selection')

        tk.Label(wng.warning, text = '\nPlease Select an Algorithm \n').pack()
        tk.Button(wng.warning, text = 'Return', command = lambda: wng.warning.destroy()).pack()

#############################################################################
# A classe do esqueleto, onde esta a barra de ferramentas e a janela principal
# do programa
#############################################################################
class Skeleton:

    def __init__(self):

        ############# A Janela Mae ##############

        self.main = tk.Tk()
        self.main.title('ARC_TF')
        self.main.state('zoomed')
        self.main.configure(background = 'dark grey')

        ############## A barra de Ferramentas e opcoes #################
    
        self.menu = tk.Menu(self.main)
        self.main.config(menu = self.menu)

            # O tipico File Menu. Hao de haver mais opcoes no futuro
        __file_menu = tk.Menu(self.menu, tearoff = False) 
        self.menu.add_cascade(label = 'File', menu = __file_menu)
        __file_menu.add_command(label = 'Upload Plotting Data', command = FileReader)
        __file_menu.add_command(label = 'Remove Current Plotting Data',
                                command = lambda: ClearWidget('Graphic'))
        __file_menu.add_command(label = 'Remove Algorithm Results', 
                                command = lambda: ClearWidget('Results'))
        __file_menu.add_separator()
        __file_menu.add_command(label = "Save Results")
        __file_menu.add_command(label = "Reset All Data from Current Tab",
                                command = lambda: ClearWidget('Everything') )
        __file_menu.add_command(label = "Manage Alpha Particles Source Values")
        __file_menu.add_separator()
        __file_menu.add_command(label = 'Exit Program', command = self.main.quit)

            # Indica ao programa qual a fonte de particulas alfa
        """ __source_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Alpha Particles Source', menu = __source_menu)
        __source_menu.add_radiobutton(label = "Ra 226", 
                                      command = lambda: Method(2))
        __source_menu.add_radiobutton(label = "Ur 232", 
                                      command = lambda: Method(2)) """

            # Indica ao programa qual o algoritmo a correr
        """ __algorithm_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Algorithm', menu = __algorithm_menu)
        __algorithm_menu.add_command(label = "Manual Selection", 
                                        command = lambda: Method(1))
        __algorithm_menu.add_command(label = "Threshold Input", 
                                        command = lambda: Method(2)) """

            # Gere as tabs do programa
        __tabs_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Manage Tabs', menu = __tabs_menu)
        __tabs_menu.add_command(label = 'Add Calibration Tab', command = lambda: Tabs.tab_change(1))
        __tabs_menu.add_command(label = 'Add Material Tab', command = lambda: Tabs.tab_change(2))
        __tabs_menu.add_separator()
        __tabs_menu.add_command(label = 'Remove Current Tab')

            # Corre o algoritmo
        #self.menu.add_command(label = 'Run', command = Method)

            # Abre o ficheiro Help
        self.menu.add_command(label = "Help")

    def run(self):
        #### O metodo que permite o programa manter-se aberto
        self.main.mainloop()

#############################################################################
# A class dos avisos e popups. E facilmente reciclavel e versatil
#############################################################################
class Warnings:
    def popup(self, name):

        self.warning = tk.Toplevel(window.main)
        self.warning.title(name)
        self.warning.geometry('700x300')
        self.warning.grab_set()

############################################################################
# A class das Tabs. Inclui a estrutura propria do Notebook - widget de 
# separadores; as tabs dos resultados e de adicionar tabs; e a estrutura que
# muda a forma de tabs de calibracao e materiais
############################################################################
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

    def AnalysisTab(self, choice):

        ### Configuracao de geometria e Frames comuns a Calib e Material Tabs  ####
        
        TabList[Notebook.value][0].columnconfigure(0, weight= 4)
        TabList[Notebook.value][0].columnconfigure(1, weight = 1)
        TabList[Notebook.value][0].rowconfigure(0, weight = 4)
        TabList[Notebook.value][0].rowconfigure(1, weight = 1)

        self.GraphicFrame = tk.Frame(TabList[Notebook.value][0], borderwidth = 5, relief = 'ridge')
        self.GraphicFrame.grid(column = 0, row = 0, sticky = "nw", pady = 5, columnspan = 2)

        self.DataFrame = tk.Frame(TabList[Notebook.value][0], borderwidth = 5, relief = 'ridge')
        self.DataFrame.grid(column = 2, row = 0, sticky = "ne", pady = 5)

        self.SourceFrame = tk.Frame(TabList[Notebook.value][0], borderwidth = 5, relief = 'ridge')
        self.SourceFrame.grid(column = 1, row = 0, sticky = "ne", pady = 5)

        self.AlgFrame = tk.Frame(self.DataFrame, borderwidth = 0)
        self.AlgFrame.grid(row = 2, columnspan = 2)
       
        self.ResultFrame = tk.Frame(self.DataFrame)
        self.ResultFrame.grid(row = 3, columnspan = 2, pady = 5)

        tk.Label(self.DataFrame, text = 'Analysis Method Selected: ').grid(row = 0, columnspan = 2)
        Algs = ["Manual Selection", "Threshold Input"]
        tk.OptionMenu(self.DataFrame, Algorithm_Method, *Algs, command = Method).grid(row = 1, columnspan = 2)
        
        ##################################### Variaveis para cada instance ##########################

        self.Results_List_y = []
        self.Results_List_x = []

        self.variable1 = tk.DoubleVar()
        self.variable2 = tk.DoubleVar()
        self.variable3 = tk.DoubleVar()
        self.variable4 = tk.DoubleVar()
        self.variable5 = tk.DoubleVar()
        self.variable6 = tk.DoubleVar()
        self.variable7 = tk.DoubleVar()
        self.variable8 = tk.DoubleVar()
        self.variable9 = tk.DoubleVar()
        self.variable10 = tk.DoubleVar()
        self.variable11 = tk.DoubleVar()
        self.variable12 = tk.DoubleVar()
        self.variable13 = tk.DoubleVar()
        self.variable14 = tk.DoubleVar()
        self.variable15 = tk.DoubleVar()

        self.Var_Data = [
            self.variable1, self.variable2, self.variable3, self.variable4, self.variable5,
            self.variable6, self.variable7, self.variable8, self.variable9, self.variable10,
            self.variable11, self.variable12, self.variable13, self.variable14, self.variable15
        ]

        
        def MatTab(self):

            tk.Label(self.SourceFrame, text = 'Material of Film Used: ').grid(row = 0, columnspan = 2)
            Materials = ["Al", "Au", "Pb", "PMMA", "Sn"]
            tk.OptionMenu(self.SourceFrame, Mat, *Materials ).grid(row = 1, columnspan = 2)

        def CalibTab(self):

            tk.Label(self.SourceFrame, text = 'Radiation Source Selected: ').grid(row = 0, columnspan = 2)
            options = ["226 Ra", "232 Ur"]
            tk.OptionMenu(self.SourceFrame, Source, *options ).grid(row = 1, columnspan = 2)
        
        if choice == 1:
            CalibTab(self)
            
        elif choice == 2:
            MatTab(self)

    @staticmethod
    def tab_change(num):

        index = len(Notebook.notebook.tabs()) - 1

        if num == 3:

            Notebook.notebook.select(index - 1)
            wng.warning.destroy()
            

        elif num == 1:
            
            TabList[Notebook.value][1].AnalysisTab(1)
            Notebook.notebook.insert(index, TabList[Notebook.value][0], text = "Calibration Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()

            
        elif num == 2:

            TabList[Notebook.value][1].AnalysisTab(2)
            Notebook.notebook.insert(index, TabList[Notebook.value][0], text = "Material Trial")
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            wng.warning.destroy()

############ Variaveis Estruturais #############################

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

TabList = [
    [tab1, tabtype1, "Data1.txt"], [tab2, tabtype2, "Data2.txt"], [tab3, tabtype3, "Data3.txt"],
    [tab4, tabtype4, "Data4.txt"], [tab5, tabtype5, "Data5.txt"], [tab6, tabtype6, "Data6.txt"],
    [tab7, tabtype7, "Data7.txt"], [tab8, tabtype8, "Data8.txt"], [tab9, tabtype9, "Data9.txt"],
    [tab10, tabtype10, "Data10.txt"], [tab11, tabtype11, "Data11.txt"],
    [tab12, tabtype12, "Data12.txt"], [tab13, tabtype13, "Data13.txt"]
]

######### Variaveis globais cujo input e/pode ser utilizado por varias funcoes ############

Algorithm = tk.IntVar()
Algorithm.set(0)

Algorithm_Method = tk.StringVar()
Algorithm_Method.set('Select Algorithm to Run')

Source = tk.StringVar()
Source.set('Radiation Sources')

Mat = tk.StringVar()
Mat.set('Select Material')

Mnl_selectiony = tk.DoubleVar()
Mnl_selectiony.set(0)
Mnl_selectionx = tk.DoubleVar()
Mnl_selectionx.set(0)

##############################################################################################

window.run()


