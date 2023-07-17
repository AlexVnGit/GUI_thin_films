import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import matplotlib as mp

########### 
# Por enquanto não se utilizam todas estas bibliotecas
#Mas irão ser necessárias (provavelmente)
#########

####### 
#Esta função irá ler o ficheiro input. Em principio, apos receber o ficheiro
#ira automaticamente exibir o grafico
######
def FileReader(): 

    domain = (('text files', '*.mca *.txt *.dat'), ('all files', '*.*'))
    filename = fd.askopenfile(title = 'Open a file', initialdir = '.', filetypes = domain)    
    showinfo(title = 'Selected File', message = filename)

######
#Funcao em desenvolvimento... Ira ser a funçao que decide qual o algoritmo
#a ser utilizado na analise dos dados
####
def Analysis():

    Test1 = Menu.get()

    Window = tk.Tk()
    if Test1 == 'Select Analysis Method':
       myLabel = tk.Label(Window, text = "No Analysis Method Selected")
       myLabel.pack()
       ReturnButton = tk.Button(Window, text = 'Return', command = Window.mainloop())
       ReturnButton.pack()  
    else:
       myLabel = tk.Label(Window, text = "Analysis Method Selected: \n" + Test1)
       myLabel.pack()
       ReturnButton = tk.Button(Window, text = 'Return', command = Window.mainloop())
       ReturnButton.pack()
       

########
#Toda esta secçao define as estruturas presentes na janela
#A maior parte dos widgets têm comentarios para explicar o contexto
#####
main = tk.Tk() #Janela Principal
main.state('zoomed')
main.title("AEL Thin Film Characterization")

    #Frame dos ícones ferramentas
ToolbarFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge', width = 500, height = 30) 
ToolbarFrame.grid(column = 0, row = 0, padx = 0, pady = 0)
    
    #Botao para chamar o menu de Upload do ficheiros
FileUpload = tk.Button(ToolbarFrame, text = "Insert Files" , command = FileReader)
FileUpload.grid(column = 0, row = 0)
FileUpload.focus()

    #Menu Dropwdown das Ferramentas de análise
Menu = tk.StringVar()
Menu.set("Select Analysis Method")
Options = ["Peak-Input", "Noise Remover", "Manual Selection"]
Tools = tk.OptionMenu(ToolbarFrame, Menu, *Options)
Tools.grid(column = 1, row = 0)
Tools.focus()
    
    #Botão de Começo da Análise
Run = tk.Button(ToolbarFrame, text = 'Run', command = Analysis)
Run.grid(column = 2, row = 0)
Run.focus()

    #Botão de Download dos Dados
Download = tk.Button(ToolbarFrame, text = 'Download')
Download.grid(column = 3, row = 0)
Download.focus()

    #Botão de Separador Novo de Análise (Para os Filmes)
ThinFilm = tk.Button(ToolbarFrame, text = 'New Trial')
ThinFilm.grid(column = 4, row = 0)
ThinFilm.focus()

    #Botão de Voltar ao Menu Principal
Escape = tk.Button(ToolbarFrame, text = 'Return to Main Menu')
Escape.grid(column = 5, row = 0)
Escape.focus()

    #Frame para o Gráfico
GraphicFrame = tk.Frame(main, borderwidth = 5, relief = 'ridge', width = 1000, height = 600)
GraphicFrame.grid(column = 0, row = 1)
GraphicFrame.focus()

    #Frame para os Dados
DataFrame = tk.LabelFrame(main, borderwidth = 5, relief = 'ridge', width = 280, height = 600)
DataFrame.grid(column = 1, row = 1)
DataFrame.focus()

    #Mainloop mantém a janela do GUI aberta.
main.mainloop() 
