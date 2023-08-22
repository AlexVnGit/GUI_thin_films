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
import os
import math

########## Ajusta-se ao ecra e foca os widgets ######
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
###########################################################
# Returns the index of the Tab the user is on
###########################################################
def Current_Tab():

    final_num = int(Notebook.notebook.select()[-1]) - 3  # Devolve o id da tab onde o utilizador se encontra                # Vai buscar o numero na string do id
              # Altera-se o valor para corresponder aos indices da lista

    return final_num

#########################################################################################
# Apaga as widgets dentro de frames e tira a geometria de frames, para fazer renovacao
# de dados. Podera conter, eventualmente, mais frames do que contem agora
#########################################################################################
def ClearWidget(Frame, parameter):
    num = Current_Tab()

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
        
        if parameter == 1: #Porque o search do algoritmo de selecao manual reconstroi os widgets
                           # da frame sempre que se encontra um novo ponto, e necessario
                           # configurar o caso onde ha reset dos dados e o caso onde nao ha reset
            try:
                os.remove(TabList[num][3])
            except:
                ()        

    elif Frame == 'Source':
        for widget in TabList[num][1].SourceOptionsFrame.winfo_children():
            widget.destroy()
        TabList[num][1].SourceOptionsFrame.grid_remove()

    elif Frame == 'Everything':
        for widgets in TabList[num][1].GraphicFrame.winfo_children():
            widgets.destroy()         # Este 'for' destroi grafcos antigos e constoi novos
        widget = 0
        TabList[num][1].GraphicFrame.grid_remove()

        
        for widget in TabList[num][1].AlgFrame.winfo_children(): 
            widget.destroy() #Destroi a opcao de widgets anteriores dos algoritmos
        widget = 0
        TabList[num][1].AlgFrame.grid_remove()


        for widget in TabList[num][1].ResultFrame.winfo_children():
            widget.destroy()         # Este 'for' destroi grafcos antigos e constoi novos
        widget = 0
        TabList[num][1].ResultFrame.grid_remove()

        for widget in TabList[num][1].SourceOptionsFrame.winfo_children():
            widget.destroy()
            TabList[num][1].SourceOptionsFrame.grid_remove()

        if parameter == 1:
            try:
                os.remove(TabList[num][3])
            except:
                ()     

#########################################################################################
# Recebe os resultados dos algoritmos e mostra no GUI
########################################################################################
def ResultManager():

    num = Current_Tab()

    ClearWidget('Results', 0)
    TabList[num][1].ResultFrame.grid(row = 3, columnspan = 2, pady = 5)

    OpenFile = open(TabList[num][3], 'r')
    lines = OpenFile.read()
    OpenFile.close()
    lines = lines.splitlines()  
    Results = [[0 for i in range(1)]for j in range(len(lines))]
    i = 0

    for line in lines:
        Results[i] = (line.split(','))
        i += 1
    
    for j in range(0, len(lines)):

        for i in range(0, 2):
            Results[j][i] = int(Results[j][i])

        Result_Button = tk.Checkbutton(TabList[num][1].ResultFrame, variable = TabList[num][1].Var_Data[j],
                onvalue = 1, offvalue = -1,
                text = 'Channel: ' + str(Results[j][0]))
        Result_Button.grid(row = j , column = 0)
        Result_Button.select()
        tk.Label(TabList[num][1].ResultFrame, 
                text = '\t Counts: ' + str(Results[j][1])).grid(row = j , column = 1)
        
##########################################################################################
# Retira os resultados que nao estao checked e atualiza o txt dos resultados
##########################################################################################        
def Unchecked_Results():
    num = Current_Tab()
    i = 0
    j = 0
    k = 0


    Eraser = []
    Aux = []

    for widget in TabList[num][1].ResultFrame.winfo_children():

        Eraser.append(widget)

    OpenFile = open(TabList[num][3], 'r')
    lines = OpenFile.read()
    OpenFile.close()
    lines = lines.splitlines()
    
    for i in range(len(TabList[num][1].Var_Data)):

        if TabList[num][1].Var_Data[i].get() == 1:
            Aux.append(lines[k])
    
        elif TabList[num][1].Var_Data[i].get() == -1:
            Eraser[j].destroy()
            Eraser[j + 1].destroy()
            TabList[num][1].Var_Data[i].set(0)

        elif TabList[num][1].Var_Data[i].get() == 0:
            k = k - 1

        j += 2
        k += 1

    i = 0

    for i in range(len(TabList[num][1].Var_Data)):
        if TabList[num][1].Var_Data[i].get() == 0:
            TabList[num][1].Var_Data.append(TabList[num][1].Var_Data[i])
            TabList[num][1].Var_Data.pop(i)

    i = 0

    with open(TabList[num][3], "w") as file:
        for i in range(len(Aux)):
            file.write(Aux[i] + '\n')

#########################################################################################
# Linearizes the results with the radiation sources
#########################################################################################
def Linearize():

    num = Current_Tab()
    OpenFile = open(TabList[num][3], 'r')
    lines = OpenFile.read()
    OpenFile.close()
    lines = lines.splitlines()  
    Results = [[0 for i in range(1)]for j in range(len(lines))]
    i = 0

    xaxis = []
    yaxis = []

    avgx = 0
    avgy = 0

    for line in lines:
        Results[i] = (line.split(','))
        xaxis.append(int(Results[i][0])) 

        if TabList[num][1].DecayList[i] != 0:
            yaxis.append(TabList[num][1].DecayList[i].get())

        avgx = xaxis[i] + avgx
        avgy = yaxis[i] + avgy

        i += 1
    
    xvalues = sorted(xaxis)
    yvalues = sorted(yaxis)
    print(xvalues)
    print(yvalues)

    avgx = avgx / len(xvalues)
    avgy = avgy / len(yvalues)

    Placeholder1 = 0
    Placeholder2 = 0
    i = 0

    for i in range(len(xvalues)):
        Placeholder1 = Placeholder1 + ((xvalues[i] - avgx) * (yvalues[i] - avgy))
        Placeholder2 = Placeholder2 + (xvalues[i] - avgx)**2

    m = Placeholder1 / Placeholder2
    b = avgy - m * avgx

    sigma = 0
    i = 0
    Placeholder1 = 0
    Placeholder2 = 0

    for i in range(0, len(xvalues)):
        sigma = (yvalues[i] - m * xvalues[i] - b)**2 + sigma
        Placeholder1 = xvalues[i]**2 + Placeholder1

    Placeholder2 = (sum(xvalues))**2
    sigma = sigma / (len(xvalues) - 2) 

    sigma_m = math.sqrt(sigma / ( Placeholder1 - (Placeholder2/len(xvalues))))
    sigma_b = math.sqrt((sigma * Placeholder1)/((len(xvalues) * Placeholder1) - Placeholder2))

    tk.Label(TabList[num][1].LinearRegressionFrame, text = '(MeV)').grid(row = 0, column = 0)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Values').grid(row = 0, column = 1)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Uncertainty').grid(row = 0, column = 2)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Slope').grid(row = 1, column = 0)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Intercept').grid(row = 2, column = 0)

    tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.7f' %(m)).grid(row = 1, column = 1)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.7f' %(sigma_m)).grid(row = 1, column = 2)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.4f' %(b)).grid(row = 2, column = 1)
    tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.4f' %(sigma_b)).grid(row = 2, column = 2)

    tk.Button(TabList[num][1].LinearRegressionFrame, text = 'Commit Regression').grid(row = 3, column = 0)
    tk.Button(TabList[num][1].LinearRegressionFrame, text = 'Clear Linear Regression').grid(row = 3, column = 1)

###############################################################################
# Este e o algoritmo que determina a distancia quadrada minima entre pontos
# input, e pontos de dados
###############################################################################
def ManSelec_Alg(Valuex, Valuey):

    num = Current_Tab()

    with open(TabList[num][2], "r") as file:   #Leitura do ficheiro
        Counts = [int(line) for line in file]   #Extracao dos counts

    AuxList = []   #Lista para guardar minimos quadrados

    for i in range(0, len(Counts)):
        AuxList.append(math.sqrt(((Valuey - Counts[i])**2)+((Valuex - i + 1)**2)))

    # O ciclo for guarda toda a distancia quadrado dos valores input e dos valores dos dados

    Valuex = AuxList.index(min(AuxList)) + 1 #Corresponde ao channel com distancia minima
    Valuey = Counts[Valuex - 1] #Corresponde ao count do indice do xvalue

    if os.path.isfile(TabList[num][3]) == True:
        with open(TabList[num][3], 'a') as results:
            results.write(str(Valuex) + ',' + str(Valuey) + '\n')

    elif os.path.isfile(TabList[num][3]) == False:

        with open(TabList[num][3], 'w') as results:
            results.write(str(Valuex) + ',' + str(Valuey) + '\n')

    ResultManager()
    
###############################################################################
# Este e o algoritmo que regista os picos acima de um determinado threshold
###############################################################################
def Threshold_Alg():

    num = Current_Tab()

#Use "with open" it will close the file after reading, no need to close it manually
    with open(TabList[num][2], "r") as file:
        Counts = [int(line) for line in file]

    Threshold = TabList[num][1].Algorithm.get()
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

                if len(current_peak) > 5: #Nota Importante abaixo
                    yaxis.append(max(current_peak))
                    xaxis.append(counter + current_peak.index(max(current_peak)))
                    counter = counter + len(current_peak)
                    current_peak_counts = 0
                    current_peak = []
                
# O parametro len(current_peak) > 7, serve para evitar um
# a falha do algoritmo. Por vezes,
# no algoritmo, ele considera picos com poucos pontos, o que traz como consequencia a consideracao
# de picos que sao apenas oscilacoes da estatistica.

    if os.path.isfile(TabList[num][3]) == True:
        with open(TabList[num][3], 'a') as results:
            for i in range(len(xaxis)):
                results.write(str(xaxis[i]) + ',' + str(yaxis[i]) + '\n')

    elif os.path.isfile(TabList[num][3]) == False:
        with open(TabList[num][3], 'w') as results:
            for i in range(len(xaxis)):
                results.write(str(xaxis[i]) + ',' + str(yaxis[i]) + '\n')

    #If the last peak is not added because the data ends with a peak (could be a problem, you should check it)
    ResultManager()

################################################################################
# Gere o evento de obtencao de pontos diretamente do grafico
################################################################################
def onclick(event):

    num = Current_Tab()

    decider = TabList[num][1].Algorithm_Method.get()

    if decider == 'Manual Selection' and event.button == 3:
        xpoint = event.xdata
        ypoint = event.ydata
        ManSelec_Alg(xpoint, ypoint)

#############################################
# Esta funcao recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI.
# Ao mesmo tempo cria um txt para outras funções
# acederem aos dados
#############################################
def Plot(File, Name):

    Channel = []    #Lista vazia para guardar o Channel
    Counts = []     #Lista vazia para guardar os Counts

    num = Current_Tab()

    ClearWidget('Graphic', 0)
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

    figure.canvas.mpl_connect('button_press_event', onclick)

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

############################################################################
# Esta funcao gere 
#############################################################################
def SourceReader(*args):

    num = Current_Tab()
    
    ClearWidget('Source', 0)
    TabList[num][1].SourceOptionsFrame.grid(row = 2, columnspan = 2)
    
    Alpha = TabList[num][1].Source.get()
    Alpha = Alpha + '.txt'

    if Alpha == '226Ra.txt':
        TabList[num][1].DecayList[6].set(-1)

    with open(Alpha, 'r') as file:
        Decay = [float(line) for line in file]

    i = 0
    for i in range(len(Decay)):
        checkbutton = tk.Checkbutton(TabList[num][1].SourceOptionsFrame, text = str(Decay[i]) + ' MeV',
                       variable = TabList[num][1].DecayList[i], onvalue = Decay[i], offvalue = -1)
        checkbutton.grid(row = i, columnspan = 2)
        checkbutton.select()

    tk.Button(TabList[num][1].SourceOptionsFrame, 
              text = 'Show Decay Chain').grid(row = i + 1, column = 0)
    tk.Button(TabList[num][1].SourceOptionsFrame, text = 'Linear Regression', 
              command = Linearize).grid(row = i + 1, column = 1)
    
##############################################################################
# Esta funcao altera a interface dos dados inputs para cada algoritmo
##############################################################################
def Method(*args):

    num = Current_Tab()

    ClearWidget('Algorithm', 0)
    TabList[num][1].AlgFrame.grid(row = 2, columnspan = 2)

    decider = TabList[num][1].Algorithm_Method.get() #Devolve a StringVar que decide qual o algoritmo em uso

    if decider == 'Manual Selection':   #Definicao dos controlos para o algoritmo ManSelec_Alg
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Right-Click on/near the Peaks in the Graphic ').grid(row = 2, columnspan = 2)
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'For an automatic point detection: ').grid(row = 3, columnspan = 2)
        tk.Button(TabList[num][1].AlgFrame, text = 'Remove Unchecked', 
                  command = Unchecked_Results).grid(row = 4, column = 0)
        tk.Button(TabList[num][1].AlgFrame, text = 'Remove All',
                  command = lambda: ClearWidget('Results', 1)).grid(row = 4, column = 1)
        tk.Label(TabList[num][1].AlgFrame,
                 text = 'Channel: ').grid(row = 5, column = 0)
        tk.Label(TabList[num][1].AlgFrame,
                 text = 'Counts: ').grid(row = 5, column = 1)

    elif decider == 'Threshold Input':  #Definicao dos controlos para o algoritmo Threshold_Alg
        tk.Label(TabList[num][1].AlgFrame, 
                 text = 'Please input Threshold: ').grid(row = 2, columnspan = 3)
        tk.Entry(TabList[num][1].AlgFrame, textvariable = TabList[num][1].Algorithm, relief = 'sunken',
                  borderwidth = 2).grid(row = 3, columnspan= 3)
        tk.Button(TabList[num][1].AlgFrame,text = 'Search', 
                  command =  Threshold_Alg).grid(row = 4, column = 0)
        tk.Button(TabList[num][1].AlgFrame,text = 'Remove Unchecked',
                  command = Unchecked_Results).grid(row = 4, column = 1)
        tk.Button(TabList[num][1].AlgFrame,text = 'Remove All',
                  command = lambda: ClearWidget('Results', 1)).grid(row = 4, column = 2)
        
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
                                command = lambda: ClearWidget('Graphic', 0))
        __file_menu.add_command(label = 'Remove Algorithm Results', 
                                command = lambda: ClearWidget('Results', 0))
        __file_menu.add_separator()
        __file_menu.add_command(label = "Save Results")
        __file_menu.add_command(label = "Reset All Data from Current Tab",
                                command = lambda: ClearWidget('Everything', 1) )
        __file_menu.add_command(label = "Manage Alpha Particles Source Values")
        __file_menu.add_separator()
        __file_menu.add_command(label = 'Exit', command = self.main.quit)

            # Gere as tabs do programa
        __tabs_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Manage Tabs', menu = __tabs_menu)
        __tabs_menu.add_command(label = 'Add Calibration Tab', command = lambda: Tabs.tab_change(1))
        __tabs_menu.add_command(label = 'Add Material Tab', command = lambda: Tabs.tab_change(2))
        __tabs_menu.add_separator()
        __tabs_menu.add_command(label = 'Remove Current Tab')

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
        
        ##################################### Variaveis para cada instance ##########################

        self.Algorithm_Method = tk.StringVar()
        self.Algorithm_Method.set('Select Algorithm to Run')

        self.Algorithm = tk.IntVar()
        self.Algorithm.set(0)

        self.variable1 = tk.IntVar()
        self.variable1.set(0)
        self.variable2 = tk.IntVar()
        self.variable2.set(0)
        self.variable3 = tk.IntVar()
        self.variable3.set(0)
        self.variable4 = tk.IntVar()
        self.variable4.set(0)
        self.variable5 = tk.IntVar()
        self.variable5.set(0)
        self.variable6 = tk.IntVar()
        self.variable6.set(0)
        self.variable7 = tk.IntVar()
        self.variable7.set(0)
        self.variable8 = tk.IntVar()
        self.variable8.set(0)
        self.variable9 = tk.IntVar()
        self.variable9.set(0)
        self.variable10 = tk.IntVar()
        self.variable10.set(0)
        self.variable11 = tk.IntVar()
        self.variable11.set(0)
        self.variable12 = tk.IntVar()
        self.variable12.set(0)
        self.variable13 = tk.IntVar()
        self.variable13.set(0)
        self.variable14 = tk.IntVar()
        self.variable14.set(0)
        self.variable15 = tk.IntVar()
        self.variable15.set(0)

        self.Var_Data = [
            self.variable1, self.variable2, self.variable3, self.variable4, self.variable5,
            self.variable6, self.variable7, self.variable8, self.variable9, self.variable10,
            self.variable11, self.variable12, self.variable13, self.variable14, self.variable15
        ]
    
        tk.Label(self.DataFrame, text = 'Analysis Method Selected: ').grid(row = 0, columnspan = 2)
        Algs = ["Manual Selection", "Threshold Input"]
        tk.OptionMenu(self.DataFrame, self.Algorithm_Method, *Algs, command = Method).grid(row = 1, columnspan = 2)

        def MatTab(self):

            self.Mat = tk.StringVar()
            self.Mat.set('Select Material')

            tk.Label(self.SourceFrame, text = 'Material of Film Used: ').grid(row = 0, columnspan = 2)
            Materials = ["Al", "Au", "Pb", "PMMA", "Sn"]
            tk.OptionMenu(self.SourceFrame, self.Mat, *Materials ).grid(row = 1, columnspan = 2)

        def CalibTab(self):

            self.Source = tk.StringVar()
            self.Source.set('Radiation Sources')

            self.decay1 = tk.DoubleVar()
            self.decay1.set(0)
            self.decay2 = tk.DoubleVar()
            self.decay2.set(0)
            self.decay3 = tk.DoubleVar()
            self.decay3.set(0)           
            self.decay4 = tk.DoubleVar()
            self.decay4.set(0) 
            self.decay5 = tk.DoubleVar()
            self.decay5.set(0) 
            self.decay6 = tk.DoubleVar()
            self.decay6.set(0) 
            self.decay7 = tk.DoubleVar()
            self.decay7.set(0) 

            self.DecayList = [self.decay1, self.decay2, self.decay3, self.decay4, self.decay5,
                              self.decay6, self.decay7]

            tk.Label(self.SourceFrame, text = 'Radiation Source Selected: ').grid(row = 0, columnspan = 2)
            options = ["226Ra", "232Ur"]
            tk.OptionMenu(self.SourceFrame, self.Source, *options, command = SourceReader).grid(row = 1, columnspan = 2)
            self.SourceOptionsFrame = tk.Frame(self.SourceFrame, borderwidth = 0)
            self.SourceOptionsFrame.grid(row = 2, columnspan = 2)
            self.LinearRegressionFrame = tk.Frame(self.SourceFrame, borderwidth = 1)
            self.LinearRegressionFrame.grid(row = 3, columnspan = 2)
            
        
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
    [tab1, tabtype1, "Temp\Data1.txt", "Temp\Result1.txt"], [tab2, tabtype2, "Temp\Data2.txt", "Temp\Result2.txt"], 
    [tab3, tabtype3, "Temp\Data3.txt", "Temp\Result3.txt"], [tab4, tabtype4, "Temp\Data4.txt", "Temp\Result4.txt"], 
    [tab5, tabtype5, "Temp\Data5.txt", "Temp\Result5.txt"], [tab6, tabtype6, "Temp\Data6.txt", "Temp\Result6.txt"],
    [tab7, tabtype7, "Temp\Data7.txt", "Temp\Result7.txt"], [tab8, tabtype8, "Temp\Data8.txt", "Temp\Result8.txt"], 
    [tab9, tabtype9, "Temp\Data9.txt", "Temp\Result9.txt"], [tab10, tabtype10, "Temp\Data10.txt", "Temp\Result10.txt"], 
    [tab11, tabtype11, "Temp\Data11.txt", "Temp\Result11.txt"], [tab12, tabtype12, "Temp\Data12.txt", "Temp\Result12.txt"], 
    [tab13, tabtype13, "Temp\Data13.txt", "Temp\Result13.txt"]
]

##############################################################################################
try: 
    os.mkdir('Temp') # Pasta onde serao guardados os ficheiros temporarios
except:
    ()  # No caso de haver ja uma pasta Temp, o programa prossegue

window.run()

for i in range(Notebook.value):
    try:
        os.remove(TabList[i][2]) # Apaga os dados adquiridos quando se faz plot
    except:
        ()
    try:
        os.remove(TabList[i][3]) # Apaga os dados dos resultados dos algoritmos
    except:
        ()

os.rmdir('Temp') # Apaga a pasta Temp