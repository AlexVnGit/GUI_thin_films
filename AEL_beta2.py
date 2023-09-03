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
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
#from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import os
import math
from shutil import copy2

########## Ajusta-se ao ecra e foca os widgets ######
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)
###########################################################
# Returns the index of the Tab the user is on
###########################################################
def Current_Tab():

    final_num = Notebook.notebook.index(Notebook.notebook.select()) - 1  # Devolve o id da tab onde o utilizador se encontra                # Vai buscar o numero na string do id
              # Altera-se o valor para corresponder aos indices da lista

    if final_num >= 0:
        return final_num
    
    elif final_num < 0: # Para o caso do utilizador se encontrar na tab dos resultados finais
        wng.popup('Final Results Tab Warning')
        tk.Label(wng.warning, text = 'Most actions aren\'t available for this Tab.\n').pack()
        tk.Label(wng.warning, text = 'Please open a new Tab\n\n').pack()
        tk.Button(wng.warning, text = 'Return', command = lambda: wng.warning.destroy()).pack()

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

        if parameter == 1:
            TabList[num][1].Algorithm_Method.set('Select Algorithm to Run')
            TabList[num][1].Algorithm.set(0)
    
    elif Frame == 'Results':
        for widget in TabList[num][1].ResultFrame.winfo_children():
            widget.destroy() #Destroi os resultados anteriores dos algoritmos
        TabList[num][1].ResultFrame.grid_remove()
        
        if parameter == 1: #Porque o search do algoritmo de selecao manual reconstroi os widgets
                           # da frame sempre que se encontra um novo ponto, e necessario
                           # configurar o caso onde ha reset dos dados e o caso onde nao ha reset
            if os.path.isfile(TabList[num][3]) == True:
                os.remove(TabList[num][3])

    elif Frame == 'Source': # Este for remove as opcoes de energia de decaimento das fontes de alphas
        for widget in TabList[num][1].SourceOptionsFrame.winfo_children():
            widget.destroy() 
        TabList[num][1].SourceOptionsFrame.grid_remove()
        if parameter == 1:
            TabList[num][1].Source.set('Radiation Sources')
        

    elif Frame == 'Popup': # Remove os popups que existem no programa
        for widget in wng.warning.winfo_children():
            widget.destroy()
        wng.warning.destroy()

    elif Frame == 'Linear': # Remove os resultados da regressao linear
        for widget in TabList[num][1].LinearRegressionFrame.winfo_children():
            widget.destroy()
        TabList[num][1].LinearRegressionFrame.grid_remove()
        widget = 0
        for widget in Notebook.Calib_Result2.winfo_children():
            widget.destroy()

        if parameter == 1: # Nem todas as opcoes necessitam de destruir os resultados, 
                            # portanto existe o parametro, para fazer a escolha de apagar o documento
            os.remove(TabList[num][4])

    elif Frame == 'Thickness': # Remove os resultados do calculo da espessura
        for widget in TabList[num][1].ThicknessFrame.winfo_children():
            widget.destroy()
        TabList[num][1].ThicknessFrame.grid_remove()
        widget = 0
        for widget in Notebook.Mat_Result2.winfo_children():
            widget.destroy()
        

        if parameter == 1: # Apaga os resultados escritos calculados da espessura
            TabList[num][1].Mat.set('Select Material')
            os.remove(TabList[num][4])

    elif Frame == 'Everything': # Esta e a opcao que da reset a tudo numa tab
        for widgets in TabList[num][1].GraphicFrame.winfo_children():
            widgets.destroy()        
        widget = 0
        TabList[num][1].GraphicFrame.grid_remove()
        
        for widget in TabList[num][1].AlgFrame.winfo_children(): 
            widget.destroy() 
        widget = 0
        TabList[num][1].AlgFrame.grid_remove()
        TabList[num][1].Algorithm_Method.set('Select Algorithm to Run')
        TabList[num][1].Algorithm.set(0)

        for widget in TabList[num][1].ResultFrame.winfo_children():
            widget.destroy()       
        widget = 0
        TabList[num][1].ResultFrame.grid_remove()

        if TabTracker[num] < 0:

            for widget in TabList[num][1].SourceOptionsFrame.winfo_children():
                widget.destroy()
            widget = 0
            TabList[num][1].SourceOptionsFrame.grid_remove()
            TabList[num][1].Source.set('Radiation Sources')

            for widget in TabList[num][1].LinearRegressionFrame.winfo_children():
                widget.destroy()
            widget = 0
            TabList[num][1].LinearRegressionFrame.grid_remove()

        elif TabTracker[num] > 0:

            for widget in TabList[num][1].ThicknessFrame.winfo_children():
                widget.destroy()
            TabList[num][1].ThicknessFrame.grid_remove()
            TabList[num][1].Mat.set('Select Material')

        if parameter == 1:
            if os.path.isfile(TabList[num][3]) == True:
                os.remove(TabList[num][3])
            if os.path.isfile(TabList[num][4]) == True:
                os.remove(TabList[num][4])

############################################################################################
# Funcao que le os ficheiros e devolve listas. Estas podem ser 2d ou 1d, podem ter separadores
# diferentes (entre as colunas) e pode devolver as listas como strings, floats ou ints
############################################################################################
def File_Reader(Document, Separator, Decimal):

    OpenFile = open(Document, 'r') #Abre o documento
    lines = OpenFile.read() # Le o ficheiro como string
    OpenFile.close() # Fecha o documento
    lines = lines.splitlines() #Separa o array em linhas

    if Separator != '0': # O separator verifica se temos uma matriz ou um vetor
                        # caso seja '0', o documento a ser lido e um vetor, e nao e necessario separar por
                        # colunas.

        Results = [[0 for i in range(1)]for j in range(len(lines))] # Inicio de uma matriz com entradas 
                                                                    # independentes
        i = 0

        for line in lines:
            Results[i] = (line.split(Separator)) # Aqui separam se as colunas
            i += 1

        i = 0
        j = 0

        for j in range(0, len(lines)): # Neste ciclo, sao transformados os resultados em int ou float,
                                        # conforme o input
            for i in range(0, 2):

                if Decimal == 'Yes':
                    Results[j][i] = float(Results[j][i])

                elif Decimal == 'No':
                    Results[j][i] = int(Results[j][i])

        return Results
    
    else:

        i = 0

        if Decimal == 'String': # Caso queiramos apenas uma string, a funcao devolve logo o vetor lines

            return lines
        
        else:

            for i in range(0, len(lines)): # Aqui transforma se o vetor string em int ou float e devolve

                if Decimal == 'Yes':
                        lines[i] = float(lines[i])

                elif Decimal == 'No':
                    lines[i] = int(lines[i])

            return lines

############################################################################################
# Le os resultados finais e exibe os na primeira tab
############################################################################################
def Final_Results():

    num = Current_Tab()
    tracker = TabTracker[num]

    if tracker < 0:
        Linearize()

    else:
        Final_Calculation()

    for i in range(0, len(TabTracker)):
        if tracker < 0 and TabTracker[i] < 0:
            if os.path.isfile(TabList[i][4]) == True:

                Results = File_Reader(TabList[i][4], '0', 'Yes')
                tk.Label(Notebook.Calib_Result2, text = 'Calibration Trial ' + 
                        str(-TabTracker[i]) + ' - ' +
                        TabList[i][1].Source.get()).grid(row = 4 * i + i, columnspan = 3)
                tk.Label(Notebook.Calib_Result2, 
                        text = '(MeV)').grid(row = 4 * i + i + 1, column = 0)
                tk.Label(Notebook.Calib_Result2, 
                        text = 'Values').grid(row = 4 * i + i + 1, column = 1)
                tk.Label(Notebook.Calib_Result2, 
                        text = 'Uncertainty').grid(row = 4 * i + i + 1, column = 2)
                tk.Label(Notebook.Calib_Result2, 
                        text = 'Slope').grid(row = 4 * i + i + 2, column = 0)
                tk.Label(Notebook.Calib_Result2, 
                        text = 'Intersect').grid(row = 4 * i + i + 3, column = 0)
                tk.Label(Notebook.Calib_Result2, 
                        text = '').grid(row = 4 * i + i + 4, column = 0)

                tk.Label(Notebook.Calib_Result2, 
                        text = '%.7f' %(Results[0])).grid(row = 4 * i + i + 2, column = 1)
                tk.Label(Notebook.Calib_Result2, 
                        text = '%.7f' %(Results[1])).grid(row = 4 * i + i + 2, column = 2)
                tk.Label(Notebook.Calib_Result2, 
                        text = '%.4f' %(Results[2])).grid(row = 4 * i + i + 3, column = 1)
                tk.Label(Notebook.Calib_Result2, 
                        text = '%.4f' %(Results[3])).grid(row = 4 * i + i + 3, column = 2)
                
                Notebook.calib_canvas.update_idletasks()    
                Notebook.calib_canvas.config(scrollregion = Notebook.Calib_Result2.bbox())
                Notebook.Calib_Result2.bind('<Configure>', 
                              lambda e: Notebook.calib_canvas.configure(
                                  scrollregion = Notebook.calib_canvas.bbox('all'), width = e.width)) 

        if tracker > 0 and TabTracker[i] > 0:
            if os.path.isfile(TabList[i][4]) == True and os.path.isfile(TabList[i][3]) == True:

                Results = File_Reader(TabList[i][4], '0', 'Yes')
                Peaks = File_Reader(TabList[i][3], ',', 'No')
                Peaks.sort()

                size = len(Peaks)

                for j in range(0, size):
                    if j == 0:

                        tk.Label(Notebook.Mat_Result2, text = 'Material Trial ' + 
                            str(TabTracker[i]) + ' - ' +
                            TabList[i][1].Mat.get()).grid(row = (4 + size) * i + i + j , columnspan = 2)
                        tk.Label(Notebook.Mat_Result2, 
                                 text = 'Channel').grid(row = (4 + size) * i + i + j + 1, column = 0)
                        tk.Label(Notebook.Mat_Result2, 
                                 text = 'Thickness').grid(row = (4 + size) * i + i + j + 1, column = 1)
                    
                    tk.Label(Notebook.Mat_Result2, 
                             text= str(Peaks[j][0])).grid(row = (4 + size) * i + i + j + 2, 
                                                          column = 0)
                    tk.Label(Notebook.Mat_Result2, 
                             text= str(Results[j]) + ' nm').grid(row = (4 + size) * i + i + j + 2, 
                                                          column = 1)
                    
                tk.Label(Notebook.Mat_Result2, 
                                 text = '\nAverage').grid(row = (4 + size) * i + i + j + 3, column = 0)
                tk.Label(Notebook.Mat_Result2, 
                                 text = 'Uncertainty').grid(row = (4 + size) * i + i + j + 4, column = 0)
                tk.Label(Notebook.Mat_Result2, 
                                 text = '\n' + str(Results[j + 1]) 
                                 + ' nm').grid(row = (4 + size) * i + i + j + 3, column = 1)
                tk.Label(Notebook.Mat_Result2, 
                                 text = str(Results[j + 2]) 
                                 + ' nm').grid(row = (4 + size) * i + i + j + 4, column = 1)
                tk.Label(Notebook.Mat_Result2, 
                                 text = '').grid(row = (4 + size) * i + i + j + 5, 
                                                                  columnspan = 2)
                
                Notebook.mat_canvas.update_idletasks()
                Notebook.mat_canvas.config(scrollregion = Notebook.Mat_Result2.bbox())
                Notebook.Mat_Result2.bind('<Configure>', 
                              lambda e: Notebook.mat_canvas.configure(
                                  scrollregion = Notebook.mat_canvas.bbox('all'), width = e.width)) 
                
###########################################################################################
# Permite a escolha de regressoes lineares por parte do utilizador
###########################################################################################
def Calib_Choice():

    num = Current_Tab()
    Measure = []

    for i in range(0, len(TabList[num][1].Regression_List)):
            TabList[num][1].Regression_List[i].set(-1)
    # Este for previne as escolhas antigas de interferir com a nova selecao de regressoes
    
    for i in range(0, len(TabTracker)):

        if TabTracker[i] < 0: # Certifica que so le ficheiros com regressoes lineares

            if os.path.isfile(TabList[i][4]) == True:
                Measure.append(TabTracker[i])

    # Neste ciclo, o measure regista quantas tabs de calibracao tem uma regressao linear,
    # ja que o tabtracker identifica as tabs de calibracao como sendo negativas,
    # o measure tera sempre valores entre -1 e -10

    if not Measure:

        wng.popup('No Linear Regressions detected')
        tk.Label(wng.warning, text = 'No linear Regressions were detected.\n\n' + 
                 'Please Perform a Calibration Trial before calculating the Film\'s Thickness.\n\n').pack()
        tk.Button(wng.warning, text = 'Return', command = lambda: wng.warning.destroy()).pack()

    # No caso do Measure estar vario, aparece um aviso que nenhuma regressao linear foi efetuada

    
    else: # Caso contrario, entra o popup para selecionar quais as regressoes a utilizar

        wng.popup('Linear Regression Selection Menu')
        tk.Label(wng.warning, text = 'Please Select a Calibration Trial \n' +
                 'Choosing more than one calibration will average the slopes and intersects.\n\n').pack()

        for i in range(0, len(Measure)):
            button_Choice = tk.Checkbutton(wng.warning, 
                                           text = 'Linear Regression of Calibration Trial ' +
                                             str(-Measure[i]),
                                            variable = TabList[num][1].Regression_List[i], 
                                            onvalue = -Measure[i], offvalue = -1)
            button_Choice.pack()

        # Neste ciclo, por cada regressao linear efetuada, o utilizador pode esolher utilizar uma ou
        # mais, para a calibracao. A Regression_List guarda valores 1 ou -1 sendo que o indice desta
        # lista, e utilizado depois nos calculos finais

        tk.Button(wng.warning, text = 'Return', command = lambda: ClearWidget('Popup', 0)).pack()

################################################################################################
# Calcula a espessura por cada pico
################################################################################################
def Final_Calculation():

    num = Current_Tab()
    ClearWidget('Thickness', 0)
    TabList[num][1].ThicknessFrame.grid(row = 5, columnspan = 3, pady = 5)

    Material_choice = TabList[num][1].Mat.get() # Determina qual o ficheiro do material a ler
    Material_choice = 'Files\Materials\\' +  Material_choice + '.txt'

    slope = 0
    intersect = 0
    points = []
    regressions_index = []
    material_data = File_Reader(Material_choice, '|', 'Yes') #Daqui obtemos a lista que ira guardar
    # as energias e o stopping power do material em uso

# Este ciclo determina a tab de calibracao cuja regressao foi selecionada para uso
# o regressions_index guarda o indice do Tab Tracker
# Com este valor, podemos aceder ao indice do TabList para obter todos os dados que queiramos
    for i in range(0, len(TabList[num][1].Regression_List)):
        if TabList[num][1].Regression_List[i].get() != -1:
            regressions_index.append(TabTracker.index(-TabList[num][1].Regression_List[i].get()))

    i = 0
    j = 0
    Aux_Channel = []
    Temp = []

    for j in range(0, len(TabList[regressions_index[i]][1].DecayList)):

        if TabList[regressions_index[0]][1].DecayList[j].get() != -1: # Aqui, vamos buscar os valores de
                                                                        # decaimento que a utilizar para o intervalo
            Aux_Channel.append(TabList[regressions_index[0]][1].DecayList[j].get()) # de stopping powers
    # Como a fonte e a mesma para todas as calibracoes, nao importa qual delas e selecionada

    Aux_Channel.sort()
    peaks = len(Aux_Channel) # Para referencia do tamanho

    for i in range(0, len(regressions_index)):
        
        Aux_Regression = File_Reader(TabList[regressions_index[i]][4], '0', 'Yes') # Aqui vamos buscar as
        # regressoes lineares para fazer uma media

        slope = Aux_Regression[0] + slope # Acumular o declive
        intersect = Aux_Regression[2] + intersect # Acumular a ordenada na origem

    points = File_Reader(TabList[num][3], ',', 'No') # Analise dos picos de materiais em estudo
    points.sort() # Ordenar os picos por ordem crescente
    slope = slope / len(regressions_index)  # Buscar a media do declive
    intersect = intersect / len(regressions_index) # Buscar a ordenada na origem

    i = 0
    j = 0
    Aux_Regression.clear()     
    thickness = 0

    tk.Label(TabList[num][1].ThicknessFrame, text = 'Thickness [nm]').grid(row = 0, column = 0)
    tk.Label(TabList[num][1].ThicknessFrame, text = 'Channel').grid(row = 0, column = 1)

    for j in range(0, peaks):

        Temp.append((slope * points[j][0]) + intersect )  # Calibracao dos picos do material
        uncertain = 0 # Ira devolver a incerteza da media da espessura
        summed_values = 0 # Faz o somatorio dos valores do stopping power
        i = 1

        for i in range(1, len(material_data)): # O ciclo comeca em 1 porque a linha 0 tem a densidade e 
                                                # o numero atomico
            if material_data[i][0] >= Temp[j] and material_data[i][0] <= Aux_Channel[j]:

                stopping_power = material_data[i][1] * material_data[0][1]
                stopping_power = (10000 / stopping_power) # Stopping power a dividir pelo step
                                                          # e a multiplicar para obter as unidades em nm
                summed_values = summed_values + stopping_power # O somatorio que resulta na aproximacao da espessura

        Aux_Regression.append(summed_values) # Lista que guarda a espessura por perda de energia
        thickness = thickness + (Aux_Regression[j]) # Espessua media

        tk.Label(TabList[num][1].ThicknessFrame, text = '%.3f' %(Aux_Regression[j])).grid(row = j + 1, column = 0)
        tk.Label(TabList[num][1].ThicknessFrame, text = str(points[j][0])).grid(row = j + 1, column = 1)

        if j == peaks - 1: # No ultimo run do ciclo for
            
            i = 0
            thickness = thickness / len(Aux_Regression) # A fazer a media da espessura
 
            my_file = open(TabList[num][4], 'w')
            for i in range(0, len(Aux_Regression)): # Por fim faz se a incerteza da espessura media
                uncertain = (Aux_Regression[i] - thickness)**2 + uncertain
                my_file.write('%.3f' %(Aux_Regression[i]))
                my_file.write('\n')

            uncertain = uncertain / (peaks - 1)
            uncertain = math.sqrt(uncertain) # Ultimo passo que resulta na espessura certa

            my_file.write('%.3f' %(thickness))
            my_file.write('\n')
            my_file.write('%.3f' %(uncertain))
            my_file.close()

    tk.Label(TabList[num][1].ThicknessFrame, 
             text = 'Average Thickness [nm]').grid(row = j + 2, column = 0)
    tk.Label(TabList[num][1].ThicknessFrame, 
             text = 'Uncertainty [nm]').grid(row = j + 2, column = 1)
    tk.Label(TabList[num][1].ThicknessFrame, 
             text = '%.3f' %(thickness)).grid(row = j + 3, column = 0)
    tk.Label(TabList[num][1].ThicknessFrame, 
             text = '%.3f' %(uncertain)).grid(row = j + 3, column = 1)
    tk.Button(TabList[num][1].ThicknessFrame, 
              command = lambda: ClearWidget('Thickness', 1),
              text = 'Reset Results').grid(row = j + 4, columnspan = 2)

#########################################################################################
# Recebe os resultados dos algoritmos e mostra no GUI
########################################################################################
def ResultManager():

    num = Current_Tab()

    ClearWidget('Results', 0) # A funcao e evocada para dar reset aos valores anteriores
    TabList[num][1].ResultFrame.grid(row = 3, columnspan = 2, pady = 5)

    values = File_Reader(TabList[num][3], ',', 'No') #Esta leitura devolve os valores de channel e counts

    for j in range(0, len(values)): # O ciclo for apenas cria os checkbuttons e as labels para depois guardar
                                    # os valores a serem apagados/usados nas funcoes seguintes

        Result_Button = tk.Checkbutton(TabList[num][1].ResultFrame, variable = TabList[num][1].Var_Data[j],
                onvalue = 1, offvalue = -1,
                text = 'Channel: ' + str(values[j][0]))
        Result_Button.grid(row = j , column = 0)
        Result_Button.select()
        tk.Label(TabList[num][1].ResultFrame, 
                text = '\t Counts: ' + str(values[j][1])).grid(row = j , column = 1)
        
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

        Eraser.append(widget) # Aqui guardamos todos os widgets que exibem os resultados.
                                # E necessario guardar num vetor, para que depois sejam apagados os corretos

    values = File_Reader(TabList[num][3], '0', 'String') # Aqui vao se buscar os valores de channel e counts
                                                        # Como nao se fazem contas, apenas utilizamos a linha de
                                                        # string que contem ambos valores
    
    for i in range(len(TabList[num][1].Var_Data)):

        if TabList[num][1].Var_Data[i].get() == 1:
            Aux.append(values[k])   # Caso seja selecionada a opcao, guardamos a linha para depois reescrever
                                    # o documento que contem os resultados, de forma a guardar os pretendidos
    
        elif TabList[num][1].Var_Data[i].get() == -1: 

            # No caso do Var_data devolver um -1, significa que se removeu a selecao do valor
            # Nesse caso, tornamos esse valor num 0, destruimos o checkbutton no Eraser[j]
            # e destruimos a label dos counts no Eraser[j + 1]
            TabList[num][1].Var_Data[i].set(0)

            Eraser[j].destroy()
            Eraser[j + 1].destroy()

        elif TabList[num][1].Var_Data[i].get() == 0:

            # Caso haja um 0 no meio, na mudanca de dados, tiramos valores de iteracao do vetor Aux
            # e do vetor Eraser, para manter todas as contas certas
            k -= 1
            j -= 2

        j += 2
        k += 1

    i = 0

    for i in range(len(TabList[num][1].Var_Data)):
        # Este for esta separado para nao haver confusoes de indices no primeiro ciclo
        # Aqui, se for detetado um 0, pomos o IntVar no final do vetor Var_Data e
        # eliminamos os Var_Data[i] = 0 do meio dos valores selecionados/nao selecionados
        if TabList[num][1].Var_Data[i].get() == 0:
            TabList[num][1].Var_Data.append(TabList[num][1].Var_Data[i])
            TabList[num][1].Var_Data.pop(i)

    i = 0

    with open(TabList[num][3], "w") as file: # Por fim, reescrevemos o documento dos resultados
                                            # com os resultados unchecked removidos
        for i in range(len(Aux)):
            file.write(Aux[i] + '\n')

#########################################################################################
# Faz a regressao linear dos resultados
#########################################################################################
def Linearize():

    num = Current_Tab()
    
    i = 0
    xaxis = []
    yaxis = []
    values = File_Reader(TabList[num][3], ',', 'No') # Le os dados dos picos

    for i in range(0, len(values)):
        xaxis.append(values[i][0])  # Junto os canais apenas ao valor xaxis

    i = 0

    for i in range(0, len(TabList[num][1].DecayList)):

        if TabList[num][1].DecayList[i].get() != -1: 
# Na lista que guarda os valores dos alfas, juntam se aqueles que foram selecionados pelo utilizador
            yaxis.append(TabList[num][1].DecayList[i].get()) 
            
    
    xvalues = sorted(xaxis) #Organizam se ambos dados por ordem
    yvalues = sorted(yaxis)
    
    if len(xvalues) != len(yvalues): # Esta condicao verifica se para a regressao linear
        # existe uma relacao sobrejetiva
    
        wng.popup('Invalid Linear Regression Configuration')
        tk.Label(wng.warning, 
                 text = "Number of Radiation Decay does not " + 
                 "match the number of Peaks detected.\n").pack()
        tk.Label(wng.warning, text ="Please adjust the Searching Algorithms or the " +
                 "number of Decay Energy.\n\n").pack()
        tk.Button(wng.warning, text = 'Return',
                    command = lambda: wng.warning.destroy()).pack()
      
    else:

        ClearWidget('Linear', 0)
        TabList[num][1].LinearRegressionFrame.grid(row = 3, columnspan = 2, pady = 5)

        avgx = sum(xvalues) #Guardam se os valores das medias dos canais e da radiacao alfa
        avgy = sum(yvalues)
        avgx = avgx / len(xvalues)
        avgy = avgy / len(yvalues)

        Placeholder1 = 0
        Placeholder2 = 0
        i = 0

        for i in range(len(xvalues)):
            Placeholder1 = Placeholder1 + ((xvalues[i] - avgx) * (yvalues[i] - avgy))
            Placeholder2 = Placeholder2 + (xvalues[i] - avgx)**2

        m = Placeholder1 / Placeholder2 # Valor do declive
        b = avgy - m * avgx  # Valor da ordenada na origem

        sigma = 0
        i = 0
        Placeholder1 = 0
        Placeholder2 = 0

        # Estes proximos somatorios e contas servem para obter as incertezas dos valores do
        # declive e da ordenada de origem

        for i in range(0, len(xvalues)):
            sigma = (yvalues[i] - m * xvalues[i] - b)**2 + sigma
            Placeholder1 = xvalues[i]**2 + Placeholder1

        Placeholder2 = (sum(xvalues))**2
        sigma = sigma / (len(xvalues) - 2) 

        sigma_m = math.sqrt(sigma / ( Placeholder1 - (Placeholder2/len(xvalues))))
        sigma_b = math.sqrt((sigma * Placeholder1)/((len(xvalues) * Placeholder1) - Placeholder2))

        with open(TabList[num][4], 'w') as my_file:
            # Aqui, escrevem se os resultados num documento txt para outras funcoes
            # poderem aceder
            my_file.write('%.7f' %(m) + '\n')
            my_file.write('%.7f' %(sigma_m) + '\n')
            my_file.write('%.7f' %(b) + '\n')
            my_file.write('%.7f' %(sigma_b))

        # Por fim, escreve se no GUI os resultados obtidos
        tk.Label(TabList[num][1].LinearRegressionFrame, text = '(MeV)').grid(row = 0, column = 0)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Values').grid(row = 0, column = 1)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Uncertainty').grid(row = 0, column = 2)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Slope').grid(row = 1, column = 0)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = 'Intersect').grid(row = 2, column = 0)

        tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.7f' %(m)).grid(row = 1, column = 1)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.7f' %(sigma_m)).grid(row = 1, column = 2)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.4f' %(b)).grid(row = 2, column = 1)
        tk.Label(TabList[num][1].LinearRegressionFrame, text = '%.4f' %(sigma_b)).grid(row = 2, column = 2)

        tk.Button(TabList[num][1].LinearRegressionFrame, text = 'Clear Regression', 
                  command = lambda: ClearWidget('Linear', 1 )).grid(row = 3, column = 0, columnspan = 3)

###############################################################################
# Este e o algoritmo que determina a distancia quadrada minima entre pontos
# input, e pontos de dados
###############################################################################
def ManSelec_Alg(Valuex, Valuey):

    num = Current_Tab()
    Counts = File_Reader(TabList[num][2], '0', 'No')

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

    Counts = File_Reader(TabList[num][2], '0', 'No')

    Threshold = TabList[num][1].Algorithm.get()
    yaxis = []
    current_peak_counts = 0
    current_peak = []
    counter = 0
    xaxis = []
    i = 0
    j = 0

#Just iterate of the values of the list itself. Each "count" is an element of Counts
    for count in (Counts):
       #Remember, if you hit a peak the condition 
       # will enter this part always. So the "current_peak_counts" will just 
       #add the total sum of the area under the peak 
       # (this may even be useful for FWHM calculations).
       
        if count > Threshold and i > 60:

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

                    yaxis.append(max(current_peak))
                    xaxis.append(counter + current_peak.index(max(current_peak)))

                    if len(xaxis) > 1:
                        if xaxis[j] - xaxis[j-1] < 20:
                            
                            decider = max(yaxis[j-1], yaxis[j])

                            if decider == yaxis[j]:
                                yaxis.pop(j-1)
                                xaxis.pop(j-1)
                            elif decider == yaxis[j-1]:
                                yaxis.pop(j)
                                xaxis.pop(j)

                            j -= 1

                    counter = counter + len(current_peak)
                    current_peak_counts = 0
                    current_peak = []
                    j += 1
                
        i += 1




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
def showimage():
    num = Current_Tab()
    wng.popup('Decay Chain')
    


def onclick(event):

    num = Current_Tab()

    decider = TabList[num][1].Algorithm_Method.get()

    if decider == 'Manual Selection' and event.button == 3:
    # Estas duas opcoes verificam que so no modo Manual selection e so com o botado direito do rato
    # e que aparecem os dados
        xpoint = event.xdata
        ypoint = event.ydata
        ManSelec_Alg(xpoint, ypoint)

##############################################################################
#Esta funcao ira ler o ficheiro input.
##############################################################################
def DataUploader(): 

    num = Current_Tab()

    domain = (('text files', '*.mca'), ('all files', '*.*')) # Aqui limitamos os ficheiros que podem ser abertos
    filename = fd.askopenfilename(title = 'Open a file', initialdir = '.', filetypes = domain) 
    # Faz a ligacao tkinter - janela do SO para abrir o ficheiro de dados

    if not filename:
        pass # Certifica que o programa nao queixa caso nao seja efetuado um upload

    else:
        file = File_Reader(filename, '0', 'string') # Aqui le se o ficheiro que foi feito o upload
        TabList[num][5].Structure(file, filename)    # Logo de seguida faz se o grafico
        TabList[num][5].subplots()
        value = TabList[num][1].Algorithm.get()
        if value != 0:
            TabList[num][5].threshold(value)

##############################################################################
# Esta funcao gere o evento especifico de adicionar tabs, futuramente
# ira ter uma seccao especifica para esconder tabs e recuperar a tab
# de adicionar tabs, caso haja menos que 15 tabs
#############################################################################
def handleTabChange(event):

    if Notebook.notebook.select() == Notebook.notebook.tabs()[-1] and len(Notebook.notebook.tabs()) < 15:
        # Se a tab 'atual' for igual a ultima, que sera sempre a tab '+', e se o numero de tabs for menor que 15
        # Adiciona se outra tab
            
        wng.popup('Tab Selector Menu')

        tk.Label(wng.warning, text = 'Please Select New Type of Tab to Open \n').pack()
        tk.Button(wng.warning, command = lambda: Tabs.tab_change(1),
                        text = 'Calibration Trial').pack()
        tk.Button(wng.warning, command = lambda: Tabs.tab_change(2), 
                        text = 'Material Trial').pack()
        tk.Label(wng.warning, text ='\n').pack()
        tk.Button(wng.warning, text = 'Return',
                    command = lambda : Tabs.tab_change(3)).pack()
        # os numeros do tab_change indicam quais os tipos de tabs a adicionar


    elif len(Notebook.notebook.tabs()) >= 15:
        Notebook.notebook.hide(14)
        # Caso se chege ao numero 15 de tabs, o botao '+' e escondido

############################################################################
# Esta funcao gere as fontes de radiacao
#############################################################################
def SourceReader(*args):

    num = Current_Tab()
    
    ClearWidget('Source', 0) # Reset dos widgets e da geometria
    TabList[num][1].SourceOptionsFrame.grid(row = 2, columnspan = 2)

    for i in range(len(TabList[num][1].DecayList)):
        TabList[num][1].DecayList[i].set(-1) # Aqui garantimos que a mudanca de fontes de radiacao
        # alpha, nao interfere com a regressao linear a ser efetuada
    
    Alpha = TabList[num][1].Source.get()
    Alpha = 'Files\Sources\Values\\' +  Alpha + '.txt' # Esta adicao garante que o programa 
                                                    #encontra o ficheiro pretendido

    Decay = File_Reader 
    with open(Alpha, 'r') as file: # Aqui vai-se buscar todas as opcoes possiveis contidas no ficheiro
                                    # das fontes de radiacao
        Decay = [float(line) for line in file]

    i = 0
    for i in range(len(Decay)): # Aqui esta a criacao dos checkbuttons para selecionar os valores que o 
                                # utilizador pretende empregrar nos calculos
        checkbutton = tk.Checkbutton(TabList[num][1].SourceOptionsFrame, text = str(Decay[i]) + ' MeV',
                       variable = TabList[num][1].DecayList[i], onvalue = Decay[i], offvalue = -1)
        checkbutton.grid(row = i, columnspan = 2)
        checkbutton.select()

    tk.Button(TabList[num][1].SourceOptionsFrame, # Mostra uma imagem da cadeia 
              text = 'Show Decay Chain').grid(row = i + 1, column = 0)
    tk.Button(TabList[num][1].SourceOptionsFrame, text = 'Linear Regression',  # Efetua a regressao
                                                    # linear e poe os resultados na primeira tab
              command = Final_Results).grid(row = i + 1, column = 1)
    
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

        TabList[num][1].Algorithm.set(0)
        TabList[num][5].destroyer()
     

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
# Esta funcao muda uma linha de threshold, caso o utilizador escreva um numero
#############################################################################
def on_entry_change(*args):

    num = Current_Tab()

    try:
        value = TabList[num][1].Algorithm.get()
        TabList[num][5].threshold(value)
    except:
        pass

#############################################################################
# Esta funcao deixa dar upload ou apagar ficheiros para a pasta de dados
# permanentes que utiliza
############################################################################# 
def File_Manager(Choice, Nature, Action):

    if Choice == 'Source':
        if Nature == 1:
            if Action == 1:
                filename = fd.askopenfilename(filetypes = (('text files', '*.txt'), ('all files', '*.*')), 
                                              title = 'Add Alpha Source Energy File')
                dir = os.getcwd()
                dir = dir + '\Files\Sources\Values\\'
                if not filename:
                    pass
                else:
                    copy2(filename, dir, follow_symlinks=True)
            
            else:
                dir = os.getcwd()
                dir = dir + '\Files\Sources\Values\\'

                filename = fd.askopenfilename(filetypes = (('text files', '*.txt'), ('all files', '*.*')),
                                              initialdir = dir, title = 'Delete Alpha Source File')
                if not filename:
                    pass
                else:
                    os.remove(filename)
                
            Dir = os.scandir('Files\Sources\Values')
            source_list.clear()
            for entry in Dir:
                if entry.is_file():
                    temp = (os.path.splitext(entry.name))
                    source_list.append(temp[0])

        elif Nature == 0:
            if Action == 1:
                filename = fd.askopenfilename(filetypes = (('image files', '.jpg .jpeg .pgn'), 
                                                           ('all files', '*.*')), 
                                              title = 'Add Alpha Source Energy Decay Image')
                dir = os.getcwd()
                dir = dir + '\Files\Sources\Images\\'
                if not filename:
                    pass
                else:
                    copy2(filename, dir, follow_symlinks=True)
            
            else:
                dir = os.getcwd()
                dir = dir + '\Files\Sources\Images\\'

                filename = fd.askopenfilename(filetypes = (('image files', '.jpg .jpeg .pgn'), 
                                                            ('all files', '*.*')),
                                              initialdir = dir, title = 'Delete Alpha Source Decay Image')
                if not filename:
                    pass
                else:
                    os.remove(filename)


    elif Choice == 'Material':
        if Action == 1:
            filename = fd.askopenfilename(filetypes = (('text files', '*.txt'), ('all files', '*.*')), 
                                            title = 'Add Material File')
            dir = os.getcwd()
            dir = dir + '\Files\Materials\\'
            if not filename:
                pass
            else:
                copy2(filename, dir, follow_symlinks=True)
        
        else:
            dir = os.getcwd()
            dir = dir + '\Files\Materials\\'

            filename = fd.askopenfilename(filetypes = (('text files', '*.txt'), ('all files', '*.*')),
                                            initialdir = dir, title = 'Delete Material File')
            if not filename:
                pass
            else:
                os.remove(filename)
            
        Dir = os.scandir('Files\Materials')
        materials_list.clear()
        for entry in Dir:
            if entry.is_file():
                temp = (os.path.splitext(entry.name))
                materials_list.append(temp[0])

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
        __file_menu.add_command(label = 'Plot Data', command = DataUploader)
        __file_menu.add_command(label = "Save Results")
        __file_menu.add_separator()
        __file_menu.add_command(label = 'Remove Current Plot',
                                command = lambda: ClearWidget('Graphic', 0))
        __file_menu.add_command(label = 'Remove Algorithm Results', 
                                command = lambda: ClearWidget('Results', 0))
        __file_menu.add_command(label = "Reset All Data from Current Tab",
                                command = lambda: ClearWidget('Everything', 1) )
        __file_menu.add_separator()
        __file_menu.add_command(label = 'Exit', command = self.main.quit)

            # Gere as tabs do programa
        __tabs_menu = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Manage Tabs', menu = __tabs_menu)
        __tabs_menu.add_command(label = 'Add Calibration Tab', command = lambda: Tabs.tab_change(1))
        __tabs_menu.add_command(label = 'Add Material Tab', command = lambda: Tabs.tab_change(2))
        #__tabs_menu.add_separator()
        #__tabs_menu.add_command(label = 'Remove Current Tab', command = Tab_Remover)
        # Nao consigo arranjar maneira de implementar esta funcionalidade
        
        __files_data = tk.Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = 'Manage Data Files', menu = __files_data)
        __files_data.add_command(label = 'Add Alpha Source File', 
                                 command = lambda: File_Manager('Source', 1, 1))
        __files_data.add_command(label = 'Remove Alpha Source File',
                                 command = lambda: File_Manager('Source', 1, 0))
        __files_data.add_separator()
        __files_data.add_command(label = 'Add Alpha Source Image',
                                 command = lambda: File_Manager('Source', 0, 1))
        __files_data.add_command(label = 'Remove Alpha Source Image', 
                                 command = lambda: File_Manager('Source', 0, 0))
        __files_data.add_separator()
        __files_data.add_command(label = 'Add Material File',
                                 command = lambda: File_Manager('Material', 0, 1))
        __files_data.add_command(label = 'Remove Material File',
                                 command = lambda: File_Manager('Material', 0, 0))


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

        # A class cria poopups que tem que ser fechados antes de voltarem para o skeleton
        # funciona bem para avisos, mas tambem para menus com opcoes obrigatorias de submeter

        self.warning = tk.Toplevel(window.main)
        self.warning.title(name)
        self.warning.geometry('700x300')
        self.warning.grab_set()

    def Images(self): # Para as imagens dos decaimentos
        ()

############################################################################
# A class das Tabs. Inclui a estrutura propria do Notebook - widget de 
# separadores; as tabs dos resultados e de adicionar tabs; e a estrutura que
# muda a forma de tabs de calibracao e materiais
############################################################################
class Tabs:

    Counter_Mat = 0
    Counter_Calib = 0

    def First_Tabs(self):

        ####### A variavel do Notebook ##########
        self.notebook = ttk.Notebook(window.main)   
        self.notebook.pack(expand = True, fill = 'both') # Expande a frame da tab ate ao final
                                                         # da janela
        self.notebook.enable_traversal() # Permite o uso de Ctrl+Tab para circular entre tabs
        
        ########### As frames principais - Os resultados e a frame de adicionar
        self.CRFrame = tk.Frame(self.notebook, bg = 'dark grey')
        self.PlusFrame = tk.Frame(self.notebook, bg = 'dark grey')
        self.CRFrame.columnconfigure(0, weight = 3)
        self.CRFrame.columnconfigure(1, weight = 3)
        self.CRFrame.rowconfigure(0, weight = 3)
        self.CRFrame.rowconfigure(1, weight = 3)

        
        
        ############# Aqui adicionam-se as frames iniciadas acima
        self.notebook.add(self.CRFrame, text = 'Final Results')
        self.notebook.add(self.PlusFrame, text = '+')
        
        ############# Frames onde irao ser inseridos os resultados finais

        self.Calib_Result = tk.Frame(self.CRFrame, borderwidth = 5, relief = 'ridge')
        self.Calib_Result.grid(row = 0, column = 0, pady = 10, padx = 30, sticky = 'nw', rowspan = 2)
        self.Calib_Result.columnconfigure(0, weight = 3)
        self.Calib_Result.columnconfigure(1, weight = 1)

        self.Calib_Result_Title = tk.Label(self.Calib_Result, 
                 text = '                       Calibration Trials Results                       \n')
        self.Calib_Result_Title.grid(row = 0, column = 0, columnspan = 3)

        self.calib_canvas = tk.Canvas(self.Calib_Result)
        self.Calib_Result2 = tk.Frame(self.calib_canvas)
        self.calib_scrollbar = tk.Scrollbar(self.Calib_Result)

        self.calib_canvas.config(yscrollcommand = self.calib_scrollbar.set, highlightthickness = 0 )
        self.calib_scrollbar.config(orient = tk.VERTICAL, command = self.calib_canvas.yview)

        self.calib_canvas.grid(row = 1, column = 0)
        self.calib_scrollbar.grid(row = 1, column = 2, sticky = 'ns')
        self.calib_scrollbar.place
        self.calib_canvas.create_window(0, 0, window = self.Calib_Result2, anchor = tk.NW)
        self.Calib_Result2.bind('<Configure>', 
                              lambda e: self.calib_canvas.configure(
                                  scrollregion = self.calib_canvas.bbox('all'), width = e.width)) 


        self.Mat_Result = tk.Frame(self.CRFrame, borderwidth = 5, relief = 'ridge')
        self.Mat_Result.grid(row = 0, column = 1, pady = 10, padx = 30, sticky = 'ne', rowspan = 2)
        self.Mat_Result.columnconfigure(0, weight = 3)
        self.Mat_Result.columnconfigure(1, weight = 1)


        self.Mat_Result_Title = tk.Label(self.Mat_Result, 
                 text = '                       Material Trials Results                       \n')
        self.Mat_Result_Title.grid(row = 0, column = 0, columnspan = 3)

        self.mat_canvas = tk.Canvas(self.Mat_Result)
        self.Mat_Result2 = tk.Frame(self.mat_canvas)
        self.mat_scrollbar = tk.Scrollbar(self.Mat_Result)

        self.mat_canvas.config(yscrollcommand = self.mat_scrollbar.set, highlightthickness = 0 )
        self.mat_scrollbar.config(orient = tk.VERTICAL, command = self.mat_canvas.yview)

        self.mat_canvas.grid(row = 1, column = 0)
        self.mat_scrollbar.grid(row = 1, column = 2, sticky = 'ns')
        self.mat_canvas.create_window(0, 0, window = self.Mat_Result2, anchor = tk.NW )
        self.Mat_Result2.bind('<Configure>', 
                              lambda e: self.mat_canvas.configure(
                                  scrollregion = self.mat_canvas.bbox('all'), width = e.width)) 
        
        

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
        self.AlgFrame.grid(row = 2, columnspan = 2, pady = 5)
       
        self.ResultFrame = tk.Frame(self.DataFrame)
        
        
        ##################################### Variaveis para cada instance ##########################

        self.Algorithm_Method = tk.StringVar()
        self.Algorithm_Method.set('Select Algorithm to Run')

        self.Algorithm = tk.IntVar()
        self.Algorithm.trace('w', on_entry_change)
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

            self.Regression1 = tk.DoubleVar()
            self.Regression1.set(-1)
            self.Regression2 = tk.DoubleVar()
            self.Regression2.set(-1)
            self.Regression3 = tk.DoubleVar()
            self.Regression3.set(-1)
            self.Regression4 = tk.DoubleVar()
            self.Regression4.set(-1)
            self.Regression5 = tk.DoubleVar()
            self.Regression5.set(-1)
            self.Regression6 = tk.DoubleVar()
            self.Regression6.set(-1)
            self.Regression7 = tk.DoubleVar()
            self.Regression7.set(-1)
            self.Regression8 = tk.DoubleVar()
            self.Regression8.set(-1)
            self.Regression9 = tk.DoubleVar()
            self.Regression9.set(-1)
            self.Regression10 = tk.DoubleVar()
            self.Regression10.set(-1)

            self.Regression_List = [self.Regression1, self.Regression2, self.Regression3, self.Regression4, 
                                    self.Regression5, self.Regression6, self.Regression7, self.Regression8,
                                    self.Regression9, self.Regression10]
            
            self.Calib_Sel_Frame = tk.Frame(self.SourceFrame, borderwidth = 0)
            self.Calib_Sel_Frame.grid(row = 4, columnspan = 2)

            self.ThicknessFrame = tk.Frame(self.SourceFrame)

            tk.Label(self.SourceFrame, text = 'Material of Film Used: ').grid(row = 0, columnspan = 2)
            tk.OptionMenu(self.SourceFrame, self.Mat, *materials_list).grid(row = 1, columnspan = 2)

            
            tk.Label(self.SourceFrame, text = 'Choose the Calibration Regression \n'+ 
                     'Make sure the Peaks in the Calibration ' + 
                     'match the Peaks found for this trial').grid(row = 2, columnspan = 2, pady = 5)
            tk.Button(self.SourceFrame, text = 'Calibration Trial', 
                      command = Calib_Choice).grid(row = 3, column = 0)
            tk.Button(self.SourceFrame, text = 'Calculate Thickness', 
                      command = Final_Results).grid(row = 3, column = 1)

        def CalibTab(self):

            self.Source = tk.StringVar()
            self.Source.set('Radiation Sources')

            self.decay1 = tk.DoubleVar()
            self.decay1.set(-1)
            self.decay2 = tk.DoubleVar()
            self.decay2.set(-1)
            self.decay3 = tk.DoubleVar()
            self.decay3.set(-1)           
            self.decay4 = tk.DoubleVar()
            self.decay4.set(-1) 
            self.decay5 = tk.DoubleVar()
            self.decay5.set(-1) 
            self.decay6 = tk.DoubleVar()
            self.decay6.set(-1) 
            self.decay7 = tk.DoubleVar()
            self.decay7.set(-1) 

            self.DecayList = [self.decay1, self.decay2, self.decay3, self.decay4, self.decay5,
                              self.decay6, self.decay7]

            tk.Label(self.SourceFrame, 
                     text = 'Radiation Source Selected: ').grid(row = 0, columnspan = 2)
            tk.OptionMenu(self.SourceFrame, self.Source, 
                          *source_list, command = SourceReader).grid(row = 1, columnspan = 2)
            self.SourceOptionsFrame = tk.Frame(self.SourceFrame, borderwidth = 0)
            self.SourceOptionsFrame.grid(row = 2, columnspan = 2)
            self.LinearRegressionFrame = tk.Frame(self.SourceFrame, borderwidth = 1)
            
        
        if choice == 1:
            CalibTab(self)
            
        elif choice == 2:
            MatTab(self)

    @staticmethod
    def tab_change(num):

        index = len(Notebook.notebook.tabs()) - 1            

        if num == 1:

            Tabs.Counter_Calib -= 1
            TabTracker.append(Tabs.Counter_Calib)
            TabList[Notebook.value][1].AnalysisTab(1)
            Notebook.notebook.insert(index, TabList[Notebook.value][0], 
                                     text = "Calibration Trial " + str(-Tabs.Counter_Calib))
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            try:
                wng.warning.destroy()
            except:
                ()

            
        elif num == 2:

            Tabs.Counter_Mat += 1
            TabTracker.append(Tabs.Counter_Mat)
            TabList[Notebook.value][1].AnalysisTab(2)
            Notebook.notebook.insert(index, TabList[Notebook.value][0], 
                                     text = "Material Trial " + str(Tabs.Counter_Mat))
            Notebook.notebook.select(index)
            Notebook.value = Notebook.value + 1
            try:
                wng.warning.destroy()
            except:
                ()
        
        elif num == 3:

            Notebook.notebook.select(index - 1)
            wng.warning.destroy()

        elif num == 4:
            value = Current_Tab()
            Notebook.notebook.select(index - 1)

            if TabTracker[value] < 0:
                Tabs.Counter_Calib += 1

            else:
                Tabs.Counter_Mat -= 1


            TabTracker.pop(value)
                
###########################################################################
# Esta classe recebe os dados dos ficheiros externos
# e insere os graficos na frame grande do GUI.
# Ao mesmo tempo cria um txt para outras funções
# acederem aos dados
# Se estiver selecionado o threshold input, mostra uma linha do valor
############################################################################
class Plot:

    def Structure(self, File, Name):

        self.Channel = []    #Lista vazia para guardar o Channel
        self.Counts = []     #Lista vazia para guardar os Counts
        self.line = []

        num = Current_Tab()

        ClearWidget('Graphic', 0)
        TabList[num][1].GraphicFrame.grid(column = 0, row = 0, sticky = "nw", pady = 5, columnspan = 2)

        Data = open(TabList[num][2], "w")

        if Name[-4:] == ".mca":         #Por enquanto esta configurado para os ficheiros 
                                        # da maquina para AEL. Se for configurado RBS
                                        #ha-de-se incluir outro if.
            for i in range(12, len(File) - 1):  
                self.Counts.append(int(File[i]))
                self.Channel.append(i-11)
                Data.write(str(self.Counts[i-12])+"\n")

            # Ciclo for para adquirir os valores dos dados

        Data.close()

        if TabTracker[num] < 0:
            self.Title = 'Calibration Trial ' + str(-TabTracker[num])

        elif TabTracker[num] > 0: 
            self.Title = 'Material Trial ' + str(TabTracker[num])


        self.figure = Figure(figsize = (6,4), dpi = 100) #A figura contem o grafico
        self.figure_canvas = FigureCanvasTkAgg(self.figure, TabList[num][1].GraphicFrame) #A class FigureCanvasTkAgg
        #liga o matplotlib ao tkinter

        NavigationToolbar2Tk(self.figure_canvas, TabList[num][1].GraphicFrame) # Esta linha permite que as ferramentas
        #do matplotlip aparecam na interface do tkinter

    def subplots(self):
        #Aqui inicia-se o grafico com os dados e os eixos

        self.axes = self.figure.add_subplot() 
        self.axes.plot(self.Channel, self.Counts, '.', markersize = 7, label = 'Run')
        self.axes.set_title(self.Title)
        self.axes.set_xlabel('Channel')
        self.axes.set_ylabel('Counts')

        self.figure.canvas.mpl_connect('button_press_event', onclick)

        #Por fim, acrescenta-se a geometria do tkinter
        self.figure_canvas.get_tk_widget().pack()

    def destroyer(self):

        if self.line:
            self.line.pop().remove()
            self.figure_canvas.draw()


    def threshold(self, height):

        if self.line:
            self.line.pop().remove()

        self.line.append(self.axes.axhline(y = height, color = 'r', linestyle = '-'))
        self.figure_canvas.draw()

############################################################################
Dir = os.scandir('Files\Sources\Values')
source_list = []
for entry in Dir:
    if entry.is_file():
        temp = (os.path.splitext(entry.name))
        source_list.append(temp[0])

Dir = os.scandir('Files\Materials')
materials_list = []
for entry in Dir:
    if entry.is_file():
        temp = (os.path.splitext(entry.name))
        materials_list.append(temp[0])
############ Variaveis Estruturais #############################

window = Skeleton()
Notebook = Tabs()
Notebook.First_Tabs()
wng = Warnings()

############## Tabs variaveis para serem criadas ###############

""" "Beta Function"
window.menu.add_command(label = 'Tab', command = lambda: print(Notebook.notebook.tabs()))
# Hei de utilizar quando completar a remocao de tabs
# Nao vai estar na versao final """

tab1 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab2 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab3 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab4 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab5 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab6 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab7 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab8 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab9 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab10 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab11 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab12 = tk.Frame(Notebook.notebook, bg = 'dark grey')
tab13 = tk.Frame(Notebook.notebook, bg = 'dark grey')

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

graph1 = Plot()
graph2 = Plot()
graph3 = Plot()
graph4 = Plot()
graph5 = Plot()
graph6 = Plot()
graph7 = Plot()
graph8 = Plot()
graph9 = Plot()
graph10 = Plot()
graph11 = Plot()
graph12 = Plot()
graph13 = Plot()


TabList = [
    [tab1, tabtype1, "Temp\Data1.txt", "Temp\Analysis1.txt", "Temp\Result1.txt", graph1], 
    [tab2, tabtype2, "Temp\Data2.txt", "Temp\Analysis2.txt", "Temp\Result2.txt", graph2], 
    [tab3, tabtype3, "Temp\Data3.txt", "Temp\Analysis3.txt", "Temp\Result3.txt", graph3], 
    [tab4, tabtype4, "Temp\Data4.txt", "Temp\Analysis4.txt", "Temp\Result4.txt", graph4], 
    [tab5, tabtype5, "Temp\Data5.txt", "Temp\Analysis5.txt", "Temp\Result5.txt", graph5], 
    [tab6, tabtype6, "Temp\Data6.txt", "Temp\Analysis6.txt", "Temp\Result6.txt", graph6],
    [tab7, tabtype7, "Temp\Data7.txt", "Temp\Analysis7.txt", "Temp\Result7.txt", graph7], 
    [tab8, tabtype8, "Temp\Data8.txt", "Temp\Analysis8.txt", "Temp\Result8.txt", graph8], 
    [tab9, tabtype9, "Temp\Data9.txt", "Temp\Analysis9.txt", "Temp\Result9.txt", graph9], 
    [tab10, tabtype10, "Temp\Data10.txt", "Temp\Analysis10.txt", "Temp\Result10.txt", graph10], 
    [tab11, tabtype11, "Temp\Data11.txt", "Temp\Analysis11.txt", "Temp\Result11.txt", graph11], 
    [tab12, tabtype12, "Temp\Data12.txt", "Temp\Analysis12.txt", "Temp\Result12.txt", graph12], 
    [tab13, tabtype13, "Temp\Data13.txt", "Temp\Analysis13.txt", "Temp\Result13.txt", graph13]
]

TabTracker = []

#############################################################################################
Tabs.tab_change(1)
Notebook.notebook.select(1)

os.mkdir('Temp') # Pasta onde serao guardados os ficheiros temporarios
window.run()
##############################################################################################

for i in range(Notebook.value):
    if os.path.isfile(TabList[i][2]) == True:
        os.remove(TabList[i][2]) # Apaga os dados adquiridos quando se faz plot
    if os.path.isfile(TabList[i][3]) == True:
        os.remove(TabList[i][3]) # Apaga os dados dos resultados dos algoritmos
    if os.path.isfile(TabList[i][4]) == True:
        os.remove(TabList[i][4]) # Apaga os resultados das regressoes lineares

os.rmdir('Temp') # Apaga a pasta Temp