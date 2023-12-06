from tkinter import*
from tkinter import messagebox
from tkinter.ttk import Notebook
from tkinter.ttk import Combobox
from PIL import ImageTk,Image
import control as ctl
import control.matlab
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy import signal
import serial
import matplotlib.animation as animation
from datetime import datetime





class Interface:
    def __init__(self,master):
        global z
        z = 0
        
        # Define os valores globais das variáveis utilizadas na interface
        global v_0, v_1, v_2, v_3, ek_1, uk_1, it, ref, referencia, V,V1,T,U,R, tempoList,ref_1, ref1_1, now


        #Inicializa as condições iniciais da ESP-32
        self.ser = serial.Serial("COM3", 9600)  #Inicia a comunicação serial com a ESP-32
        self.ser.write(b'1023w')  # Inicia a ESP32, com a velocidade nula
        self.ser.write(b'x') # Reinicia o estado da ESP-32

       
        # Define as condicões iniciais das variáveis utilizadas no programa
        it = 0
        ref = 0
        self.ler = 'r'
        v_0, v_1, v_2, v_3, ek_1, uk_1,now = 0,0,0,0,0,0,0
        ref_1,ref1_1 = 0,0  # Condições iniciais das referências, cado não utilizar retirar essa parte
        
        # Parâmetros sugeridos e projetados
        self.kp31 = 600
        self.ki31 = 281.7



        #Define o título e os símbolos gerais da interface

        self.fontePadrao = ("Arial", "10")

        self.titulo = Label(master, text="INTERFACE DIDÁTICA PARA SINTONIA DE CONTROLADOR P.I.D EM UMA PLANTA INDUSTRIAL")
        self.titulo["font"] = ("Arial", "15", "bold")
        self.titulo["background"]= "light blue"
        self.titulo.place(x=175, y=40)

        img1 = Image.open("UFC.png")
        img1_resize =  img1.resize((49,80))
        self.imagem1 = ImageTk.PhotoImage(img1_resize)
        self.label1 = Label(master, image= self.imagem1,compound=BOTTOM)
        self.label1.image= self.imagem1
        self.label1["background"]= "light blue"
        self.label1.place( x=20, y=5)


        img2 = Image.open("Naicon.jpeg")
        img2_resize = img2.resize((68,80))
        self.imagem2 = ImageTk.PhotoImage(img2_resize)
        self.label2 = Label(master, image= self.imagem2,compound=BOTTOM)
        self.label2.image= self.imagem2
        self.label2["background"]= "light blue"
        self.label2.place( x=1175, y=10)
        

        # Cria as abas da interface de simulação do sistema
        self.abas = Notebook(master, height= 825 ,width = 1250)
        self.frame_aba1 = Frame(self.abas, background = 'light gray')
        self.frame_aba2 = Frame(self.abas, background= 'light gray')
        self.frame_aba3 = Frame(self.abas, background = 'light gray')

        # Conjunto de Elmentos presentes na primeira aba do sistema
    

        # Diagrama da Bancada didática, contendo uma explicação sobre os elementos que compõem a mesma.
        self.label15 = Label(self.frame_aba1, text = " DIAGRAMA DA BANCADA DIDÁTICA:", background = "light gray")
        self.label15['font'] = ("Arial","12","bold")
        self.label15.place(x = 50 , y = 50)


        img13  =  Image.open("Bancada.png")
        img13_resize = img13.resize((776, 687))
        self.imagem13 = ImageTk.PhotoImage(img13_resize)
        self.label16 =  Label(self.frame_aba1, image = self.imagem13)
        self.label16.image = self.imagem13
        self.label16["background"] = "light blue"
        self.label16.place(x= 250 ,y =100)

        # Conjunto de botões que vão abrir pop-ups com informações a respeito da bancada
        #INVERSOR
        self.botao11 = Button(self.frame_aba1, relief = "ridge", borderwidth=3 ,foreground= "red", background = "blue")
        self.botao11["text"] = "?"
        self.botao11["font"] = ("Arial","6","bold")
        self.botao11["command"] = self.popup01
        self.botao11.place(x= 310 , y = 425)

        
        #ESTEIRA
        self.botao12 = Button(self.frame_aba1, relief = "ridge", borderwidth = 3, foreground= "red", background = "blue")
        self.botao12["text"] = "?"
        self.botao12["font"] = ("Arial","6","bold")
        self.botao12["command"] = self.popup02
        self.botao12.place(x = 810, y = 135)

        
        #SENSOR        
        self.botao13 = Button(self.frame_aba1, relief= "ridge", borderwidth= 3, foreground= "red", background = "blue")
        self.botao13["text"] = "?"
        self.botao13["font"] = ("Arial","6","bold")
        self.botao13["command"] = self.popup03
        self.botao13.place(x = 1000 , y = 185 )


        #MOTOR
        self.botao14 = Button(self.frame_aba1, relief = "ridge", borderwidth = 3, foreground= "red", background = "blue")
        self.botao14["text"] = "?"
        self.botao14["font"] = ("Arial","6","bold")
        self.botao14["command"] = self.popup04
        self.botao14.place(x= 580 , y = 225)


        #ARTEFATO METÁLICO
        self.botao15 = Button(self.frame_aba1, relief ="ridge", borderwidth =3,  foreground= "red", background = "blue")
        self.botao15["text"] = "?"
        self.botao15["font"] = ("Arial","6","bold")
        self.botao15["command"] = self.popup05
        self.botao15.place(x= 810 , y =225)

        #CIRCUITO DE LEITURA
        self.botao16 = Button(self.frame_aba1, relief ="ridge", borderwidth=3,foreground= "red", background = "blue")
        self.botao16["text"] = "?"
        self.botao16["font"] = ("Arial","6","bold")
        self.botao16["command"] = self.popup06
        self.botao16.place(x= 910, y = 550 )


        #ESP-32
        self.botao17 = Button(self.frame_aba1, relief = "ridge", borderwidth = 3, foreground= "red", background = "blue")
        self.botao17["text"] = "?"
        self.botao17["font"] = ("Arial","6","bold")
        self.botao17["command"] = self.popup07
        self.botao17.place(x = 760 , y = 415)

        
        #CIRCUITO DE ACIONAMENTO
        self.botao18 = Button(self.frame_aba1, relief= "ridge", borderwidth= 3, foreground= "red", background = "blue")
        self.botao18["text"] = "?"
        self.botao18["font"] = ("Arial","6","bold")
        self.botao18["command"] = self.popup08
        self.botao18.place(x = 525 , y = 550)

        
        # COMPUTADOR 
        self.botao19 = Button(self.frame_aba1, relief ="ridge", borderwidth=3, foreground= "red", background = "blue")
        self.botao19["text"] = "?"
        self.botao19["font"] = ("Arial","6","bold")
        self.botao19["command"] = self.popup09
        self.botao19.place(x = 720  , y = 730)

        # Fim do conjunto de botões popup
        # Fim do conjunto dos elementos a aba01


        #Início da aba02 do sistema

        # Conjunto de Elementos presentes na segunda aba da interface
        self.label21 = Label(self.frame_aba2,text='MODELAGEM DA PLANTA G(s):', background = 'light gray')
        self.label21['font']=("Arial", "12", "bold")
        self.label21.place(x=50 ,y=50)

        img21 = Image.open("PLANTA.png")
        self.imagem21 = ImageTk.PhotoImage(img21)
        self.label22 = Label(self.frame_aba2, image= self.imagem21)
        self.label22.image = self.imagem21
        self.label22["background"]=  "blue"
        self.label22.place( x=50, y=100)

        
        self.n3label = Label(self.frame_aba2,text= "N3:", background = 'light gray')
        self.n3label["font"] = ("Arial",'10','bold')
        self.n3label.place(x=50, y=200)


        self.n3 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.n3["width"] = 5
        self.n3["font"] = ("Arial",'10','bold')
        self.n3.place(x=75, y=200)


        self.n2label = Label(self.frame_aba2,text="N2:", font=self.fontePadrao, background = 'light gray')
        self.n2label["font"] = ("Arial",'10','bold')
        self.n2label.place(x=130, y=200)

        self.n2 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.n2["width"] = 5
        self.n2["font"] = ("Arial",'10','bold')
        self.n2.place(x=155, y=200)

        
        self.n1label = Label(self.frame_aba2,text="N1:", background = 'light gray')
        self.n1label["font"] = ("Arial",'10','bold')
        self.n1label.place(x=210, y=200)

        self.n1 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.n1["width"] = 5
        self.n1["font"] = ("Arial",'10','bold')
        self.n1.place(x=235, y=200)

        
        self.n0label = Label(self.frame_aba2,text="N0:" , background = 'light gray')
        self.n0label["font"] = ("Arial",'10','bold')
        self.n0label.place(x=290, y=200)

        self.n0 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.n0["width"] = 5
        self.n0["font"] = ("Arial",'10','bold')
        self.n0.place(x=315, y=200)

        self.d3label = Label(self.frame_aba2,text= "D3:",background = 'light gray')
        self.d3label["font"] = ("Arial",'10','bold')
        self.d3label.place(x=50, y=250)


        self.d3 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.d3["width"] = 5
        self.d3["font"] = ("Arial",'10','bold')
        self.d3.place(x=75, y=250)


        self.d2label = Label(self.frame_aba2,text="D2:", font=self.fontePadrao, background = 'light gray')
        self.d2label["font"] = ("Arial",'10','bold')
        self.d2label.place(x=130, y=250)

        self.d2 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.d2["width"] = 5
        self.d2["font"] = ("Arial",'10','bold')
        self.d2.place(x=155, y=250)

        
        self.d1label = Label(self.frame_aba2,text="D1:", background = 'light gray')
        self.d1label["font"] = ("Arial",'10','bold')
        self.d1label.place(x=210, y=250)

        self.d1 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.d1["width"] = 5
        self.d1["font"] = ("Arial",'10','bold')
        self.d1.place(x=235, y=250)

        
        self.d0label = Label(self.frame_aba2,text="D0:", background = 'light gray')
        self.d0label["font"] = ("Arial",'10','bold')
        self.d0label.place(x=290, y=250)

        self.d0 = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.d0["width"] = 5
        self.d0["font"] = ("Arial",'10','bold')
        self.d0.place(x=315,y=250)

        self.tfplanta = Button(self.frame_aba2, borderwidth = 1, relief= "ridge", background ="blue",foreground = "white" )
        self.tfplanta["text"] = "Plotar G(s): "
        self.tfplanta["font"] = ("Arial", "8" , "bold")
        self.tfplanta["width"] = 24
        self.tfplanta["command"] = self.plotatfplanta
        self.tfplanta.place(x=450, y=100)

        self.mensagem = Label(self.frame_aba2, text="", borderwidth = 6, relief= "ridge")
        self.mensagem["font"]= ("Arial", "12", "bold")
        self.mensagem.place(x=450, y=130)

        
        self.label23 = Label(self.frame_aba2,text='MODELAGEM DO CONTROLADOR P.I.D C(s):', background = 'light gray')
        self.label23['font']=("Arial", "12", "bold")
        self.label23.place(x=50 ,y=320)

        img = Image.open("PID.png")
        self.imagem6 = ImageTk.PhotoImage(img)
        self.label24 = Label(self.frame_aba2, image= self.imagem6)
        self.label24.image= self.imagem6
        self.label24["background"]= "blue"
        self.label24.place( x=50, y=370)

        self.kplabel = Label(self.frame_aba2, text = 'Kp: ', font = self.fontePadrao, background = 'light gray')
        self.kplabel["font"]= ("Arial", "10", "bold")
        self.kplabel.place(x=50, y=470)

        self.kp = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.kp["width"]= 5
        self.kp["font"]= ("Arial",'10','bold')
        self.kp.place(x= 75, y= 470)

        self.kilabel = Label(self.frame_aba2, text = 'Ki: ', font = self.fontePadrao, background = 'light gray')
        self.kilabel["font"]= ("Arial", "10", "bold")
        self.kilabel.place(x = 130, y=470)

        self.ki = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.ki["width"]= 5
        self.ki["font"]= ("Arial",'10','bold')
        self.ki.place(x=155, y=470)

        self.kdlabel = Label(self.frame_aba2, text = 'Kd: ', background = 'light gray')
        self.kdlabel["font"]= ("Arial", "10", "bold")
        self.kdlabel.place(x=210, y=470)

        self.kd = Entry(self.frame_aba2, borderwidth = 2, relief = 'ridge')
        self.kd["width"]= 5
        self.kd["font"]= ("Arial",'10','bold')
        self.kd.place(x=235, y= 470)

        self.tfcontrolador = Button(self.frame_aba2, borderwidth =1 , relief ="ridge", background ="blue", foreground ="white")
        self.tfcontrolador["text"] = "Plotar C(s):"
        self.tfcontrolador["font"] = ("Arial", "8" , "bold")
        self.tfcontrolador["width"] = 24
        self.tfcontrolador["command"] = self.plotatfcontrolador
        self.tfcontrolador.place(x=450, y=320)

        self.mensagem2 = Label(self.frame_aba2, text="", font=self.fontePadrao, borderwidth = 6, relief = "ridge")
        self.mensagem2["font"]= ("Arial", "12", "bold")
        self.mensagem2.place(x= 450, y= 350)


        # Passa a figura e informações para a segunda aba
        # Diferenciar os dois tipos de 
        
        # Conjunto de Elmentos presentes na primeira aba do sistema
        self.label24 = Label(self.frame_aba2,text= 'Configuração dos Sistemas de Controle:', background = 'light gray')
        self.label24['font']= ("Arial", "12", "bold")
        self.label24.place(x= 50, y= 520)

        img23 = Image.open("MA.png")
        img23_resize =  img23.resize((375,112))
        self.imagem23 = ImageTk.PhotoImage(img23_resize)
        self.label25 = Label(self.frame_aba2, image= self.imagem23)
        self.label25.image= self.imagem23
        self.label25["background"]= "blue"
        self.label25.place( x= 125, y= 550)


        img24 = Image.open("MF.png")
        img24_resize =  img24.resize((375,112))
        self.imagem24 = ImageTk.PhotoImage(img24_resize)
        self.label27 = Label(self.frame_aba2, image= self.imagem24)
        self.label27.image= self.imagem24
        self.label27["background"]= "blue"
        self.label27.place( x= 125, y= 700)


        self.botao20 = Button(self.frame_aba2, relief ="ridge", borderwidth=3, foreground= "red", background = "blue")
        self.botao20["text"] = "?"
        self.botao20["font"] = ("Arial","6","bold")
        self.botao20["command"] = self.popup10
        self.botao20.place(x = 485  , y = 560)

        
        self.botao21 = Button(self.frame_aba2, relief ="ridge", borderwidth=3, foreground= "red", background = "blue")
        self.botao21["text"] = "?"
        self.botao21["font"] = ("Arial","6","bold")
        self.botao21["command"] = self.popup11
        self.botao21.place(x = 485 , y = 710)


        

    
        
        # Fim dessa seção   
        self.simulacaolabel = Label(self.frame_aba2,text = 'SIMULAÇÃO DO SISTEMA:', font = self.fontePadrao)
        self.simulacaolabel["font"]= ("Arial", "12", "bold")
        self.simulacaolabel.place(x=785,y=50)

        # Cria duas abas para a simulação do sistema, dentro da segunda aba geral
        # Cria as abas da interface de simulação do sistema
        
        self.abas2 = Notebook(self.frame_aba2, height= 600 ,width = 500)
        self.frame_aba21 = Frame(self.abas2)
        self.frame_aba22 = Frame(self.abas2)
        self.frame_aba23 = Frame(self.abas2)
        self.frame_aba24 = Frame(self.abas2)
        self.frame_aba25 = Frame(self.abas2)

        #Adiciona as respectivas abas
        self.abas2.add(self.frame_aba21,text= "Tempo")
        self.abas2.add(self.frame_aba22,text="Bode")
        self.abas2.add(self.frame_aba24, text = "Nyquist")
        self.abas2.add(self.frame_aba25, text = " L.G.R")
        self.abas2.place(x=740, y=100)
        
        # Cria os widgets da respectiva aba

        #Cria o Label do primeiro Combobox
        # Label para indicar a escolha do tipo de sistema
        self.sistemalabel = Label(self.frame_aba21, text = 'Sistema:')
        self.sistemalabel["font"]= ("Arial", "8", "bold")
        self.sistemalabel.place(x=0,y=0)

        # Define o combobox do tipo de malha
        self.combo_Malha = Combobox(self.frame_aba21)
        self.combo_Malha['values']= ( 'Malha Aberta', 'Malha Fechada')
        self.combo_Malha.current(0)  # define o item selecionado
        self.combo_Malha.place(x=75, y=0)

        # Label para indicar a escolha do tipo de sistema
        self.entradalabel = Label(self.frame_aba21, text = 'Entrada:')
        self.entradalabel["font"]= ("Arial", "8", "bold")
        self.entradalabel.place(x=0,y=25)

        # Define o combobox do tipo da entrada
        self.combo_Entrada = Combobox(self.frame_aba21)
        self.combo_Entrada['values']= ('Impulso','Degrau','Rampa','Parábola')
        self.combo_Entrada.current(1)  # define o item selecionado
        self.combo_Entrada.place(x=75, y=25)

        # Label para definir o tempo da simulação
        self.temposimulabel = Label(self.frame_aba21, text = 'Tempo (s):')
        self.temposimulabel["font"]= ("Arial", "8", "bold")
        self.temposimulabel.place(x=0,y=50)
        
        self.temposimu = Entry(self.frame_aba21, text = "Tempo (s)" ,borderwidth= 2, relief = 'ridge')
        self.temposimu["font"]= ("Arial", "8")
        self.temposimu.place(x=75,y=50)
        

        self.plotgrafico = Button(self.frame_aba21,borderwidth =1 , relief ="ridge", background ="blue", foreground ="white")
        self.plotgrafico["text"] =  "Plotar Gráfico"
        self.plotgrafico["font"] =  ("Arial", "8" , "bold")
        self.plotgrafico["width"] = 24
        self.plotgrafico["command"] = self.plotagrafico
        self.plotgrafico.place(x=275, y= 25)

        a =  [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.10]
        b =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        
        self.fig = Figure (figsize = (4.5,4.5), dpi = 100)
        self.plot1  = self.fig.add_subplot(111)
        self.line1, = self.plot1.plot(a,b)
        self.line2, = self.plot1.plot(a,b)
        self.plot1.grid(color ='b',linestyle = '-',linewidth=0.5)
        self.plot1.set_title("Resposta do Sistema", fontsize = 10, color ='r',)
        self.plot1.set_ylabel("Saída", color = 'r')
        self.plot1.set_xlabel("Tempo(s)", color = 'r')
        self.plot1.legend(['Resposta do Sistema','Entrada'])
        self.canvas1 = FigureCanvasTkAgg(self.fig, self.frame_aba21)   
        self.canvas1.draw() 
        self.canvas1.get_tk_widget().place(x=50, y=75)
        
        toolbar = NavigationToolbar2Tk(self.canvas1, self.frame_aba21)
        toolbar.update() 
        self.canvas1.get_tk_widget().place(x=50,y=75)
                

        
        # Conjunto de elemento da aba22 do sistema
        # Label para indicar a escolha do tipo de sistema
        self.sistemalabelf = Label(self.frame_aba22, text = 'Sistema:')
        self.sistemalabelf["font"]= ("Arial", "8", "bold")
        self.sistemalabelf.place(x=0,y=25)

        # Define o combobox do tipo de malha
        self.combo_Malhaf = Combobox(self.frame_aba22)
        self.combo_Malhaf['values']= ( 'Malha Aberta', 'Malha Fechada')
        self.combo_Malhaf.current(0)  # define o item selecionado
        self.combo_Malhaf.place(x=75, y=25)

        self.plotgraficof = Button(self.frame_aba22,borderwidth =1 , relief ="ridge", background ="blue", foreground ="white")
        self.plotgraficof["text"] =  "Plotar Gráfico"
        self.plotgraficof["font"] =  ("Arial", "8" , "bold")
        self.plotgraficof["width"] = 24
        self.plotgraficof["command"] = self.plotagraficof
        self.plotgraficof.place(x= 275, y= 25)

        self.fig22 = plt.figure("Diagrama de Bode", figsize = (4.8,4.5))
        ''']
        self.plot2 = self.fig22.add_subplot(111)
        self.line3, = self.plot2.plot(a,b)
        self.plot2.grid(color ='b',linestyle = '-',linewidth=0.5)
        self.plot2.set_title("Diagrama de Bode - Magnitude", fontsize = 10, color ='r',)
        self.plot2.set_ylabel("Magntude(dB)", color = 'r', fontsize = 8)
        self.plot2.set_xlabel("Frequência(rad/sec)", color = 'r')
        '''
        
        self.canvas2 = FigureCanvasTkAgg(self.fig22, self.frame_aba22)   
        self.canvas2.draw() 
        self.canvas2.get_tk_widget().place(x =0, y=75)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, self.frame_aba22)
        self.toolbar2.update() 
        self.canvas2.get_tk_widget().place(x= 50, y=75)
     


        #Criação dos elementos da aba24

        self.sistemalabel24 = Label(self.frame_aba24, text = 'Sistema:')
        self.sistemalabel24["font"]= ("Arial", "8", "bold")
        self.sistemalabel24.place(x=0,y=25)

        # Define o combobox do tipo de malha
        self.combo_Malha24 = Combobox(self.frame_aba24)
        self.combo_Malha24['values']= ( 'Malha Aberta', 'Malha Fechada')
        self.combo_Malha24.current(0)  # define o item selecionado
        self.combo_Malha24.place(x=75, y=25)

        self.plotgraficonyquist = Button(self.frame_aba24,borderwidth =1 , relief ="ridge", background ="blue", foreground ="white")
        self.plotgraficonyquist["text"] =  "Plotar Gráfico"
        self.plotgraficonyquist["font"] =  ("Arial", "8" , "bold")
        self.plotgraficonyquist["width"] = 24
        self.plotgraficonyquist["command"] = self.plotagrafnyquist
        self.plotgraficonyquist.place(x=275, y= 25)



        #Criação de uma figura diferente para o diagramama de nyquist.

        # Alternativa 02
        self.fig24 = plt.figure("Diagrama de Nyquist", figsize = (4.8,4.5))
        #

        ''' 
        self.fig24 = Figure (figsize = (4.5,4.5), dpi=100)
        self.plot4 = self.fig24.add_subplot(111)
        self.line5, = self.plot4.plot(a,b)
        self.plot4.grid(color ='b',linestyle = '-',linewidth=0.5)
        self.plot4.set_title("Diagrama de Nyquist", fontsize =10, color ='r')
        self.plot4.set_ylabel("Eixo Imaginário", color = 'r', fontsize = 8, loc = "center", labelpad= 5)
        self.plot4.set_xlabel("Eixo Real", color = 'r', loc = 'center',  labelpad =  5)
        '''

        self.canvas4 = FigureCanvasTkAgg(self.fig24,self.frame_aba24)
        self.canvas4.draw()
        self.canvas4.get_tk_widget().place(x=0 , y= 75 )
        self.toolbar4 = NavigationToolbar2Tk(self.canvas4,self.frame_aba24)
        self.toolbar4.update()
        self.canvas4.get_tk_widget().place(x = 50 , y=75)
        


        # Fim do diagrama de Nyquist


        # Elementos da aba de LGR

        self.botao25 = Button(self.frame_aba25, text = "Plotar")
        self.botao25['command'] = self.plotalgr
        self.botao25.place(x =0, y =0)
        

        self.fig25 =  plt.figure("Diagrama do Lugar das Raízes", figsize = (4.8,4.5))
        self.canvas5 = FigureCanvasTkAgg(self.fig25,self.frame_aba25)
        self.canvas5.draw()
        self.canvas5.get_tk_widget().place(x= 0 , y= 75 )
        self.toolbar5 = NavigationToolbar2Tk(self.canvas5,self.frame_aba25)
        self.toolbar5.update()
        self.canvas5.get_tk_widget().place(x =50, y=75)





        self.quit1 =  Button(self.frame_aba2, text = "Sair", command = root.destroy)
        self.quit1["font"] = ("Arial","10","bold") 
        self.quit1["background"] = ("grey")
        self.quit1.place(x = 632, y = 794)

        
        self.quit2 =  Button(self.frame_aba1, text = "Sair", command = root.destroy)
        self.quit2["font"] = ("Arial","10","bold") 
        self.quit2["background"] = ("grey")
        self.quit2.place(x = 632, y = 794)

        
        self.quit3 =  Button(self.frame_aba3, text = "Sair", command = root.destroy)
        self.quit3["font"] = ("Arial","10","bold")
        self.quit3["background"] = ("grey")
        self.quit3.place(x = 632, y = 794)

        



        # Conjunto de Elementos presentes na terceira aba da interface
    
        self.label_39 =  Label(self.frame_aba3, text = "CONTROLE DE VELOCIDADE:", background = "light gray")
        self.label_39["font"] = ("Arial","12","bold")
        self.label_39.place(x=120 , y= 590)


        self.referencialabel32 =  Label(self.frame_aba3, text = "SETPOINT (m/s):", font = "Arial 8", background= "light blue")
        self.referencialabel32["font"] = ("Arial","8","bold")
        self.referencialabel32.place( x= 275, y=680)    

        self.referencia = Entry(self.frame_aba3, width= 10, justify = 'center')
        self.referencia["font"] = ("Arial","8","bold")  
        self.referencia.place(x= 375, y= 680)

        self.botao_31 = Button(self.frame_aba3, width=10, text= "SET", command= self.Seta  ,background="yellow", borderwidth=3, relief="ridge")
        self.botao_31["font"] = ("Arial","10","bold")
        self.botao_31.place(x=300, y=620) #Posiciona a caixa de texto

        self.botao_32 = Button(self.frame_aba3, width=10, text= "DESLIGA", command= self.Desliga,background="red",borderwidth=3, relief= "ridge")
        self.botao_32["font"] = ("Arial","10","bold")
        self.botao_32.place(x=100, y= 670) #Posiciona a caixa de texto

        self.botao_33 = Button(self.frame_aba3, width=10, text = "LIGA", command = self.Liga, background= "green", borderwidth=3,relief= "ridge")
        self.botao_33["font"] = ("Arial","10","bold")
        self.botao_33.place(x=100,y=620)


        self.abas31 = Notebook(self.frame_aba3,height = 600 , width= 700)
        self.frame_aba31 = Frame(self.abas31) 
        self.frame_aba32 = Frame (self.abas31)



        # Aqui se inicia a função animate
        def animate(i,dataList,tempoList):
            global v_0, v_1, v_2, v_3, v_4, it, referencia,ref,ref_1,ref1,ref1_1,V,V1,T,U,R,ek_1,uk_1
            
            # Leitura e tratamento de velocidade
            try:
                self.ser.write(self.ler.encode())
                tempo = self.ser.readline()
                tempo = float(tempo)

            except:
                pass

        
            v_4 = v_3
            v_3 = v_2
            v_2 = v_1 
            v_1 = v_0

            if tempo == 0: 
                v_0 = v_1 
            else: 
                v_0 = (((np.pi)/3)/(tempo))*47.5

            # Tratamento de outliers presente na leitura da velocidade
            if  v_0 >= 0.200:
                v_0 = v_1

            if  (it >= 4):
                A = ((v_4 + v_3 + v_2 + v_1 + v_0)/5)
                V.append(A)
                V1.append(A)
                V = V[-100:]
                V1 = V1[-500:]
            else:
                A = v_0
                V.append(A)
                V1.append(A)
                V = V[-100:]
                V1 = V1[-500:]


            #Filtro do sinal de referência
            ref1 = 0.1*ref_1 + 0.9*ref1_1    # Calcula o  filtro digital do sinal de referência
            ref_1 = ref                        # Armazena a referencia atual
            ref1_1= ref1                       # Armazena a referencia filtrada atual 

            print("O valor de referência na entrada é:", ref)
            print("O valor de referência na saída é: ", ref1)

            
            # Cálculo do sinal de controle U
            ek =  ref - A   #Utiliza o novo valor de referência: caso contrário; ek = ref1 -A
            uk = uk_1 + self.kp31*(ek -ek_1) + self.ki31*0.213*ek
            
            '''
            uk = uk_1 + 600*(ek - 0.9*ek_1)  
            '''
            U.append(uk)
            U = U[-500:]
            uk_1 = uk
            ek_1 = ek

            # Envia o sinal de controle para a planta, com as devidas considerações
            print("Sinal de controle é: ", uk)
            Up = uk*(1023/100)

            
            if (Up>=1023):
                Up = 1023

            

            Up = 1023 - Up  # Verificar essa relação de controle
            Up = int(Up)
            Up_string = str(Up)
            Up_string = Up_string + 'w'
            # print(Up_string)
            self.ser.write(Up_string.encode())
            print("Controle")
            now = datetime.now()
            print(now)

            ts = it*0.213
            tempoList.append(ts)
            T.append(ts)
            tempoList = tempoList[-100:]  # Fixa o tamanho do vetor de tempo
            T = T[-500:]

            
            referencia.append(ref)
            R.append(ref)
            referencia = referencia[-100:]
            R = R[-500:]

            dataList = dataList[-100:]                            # Fixa o tamnaho do vetor de dados
          
            
            self.plot31.clear()                                   # Clear last data frame
            self.plot31.plot(tempoList,V)
            self.plot31.plot(tempoList,referencia) 
            # Plot new data frame

            self.plot31.set_ylim([0,0.150])  
            self.plot31.grid(color ='b',linestyle = '-',linewidth=0.5)
            self.plot31.set_title("Velocidade da Esteira Transportadora (m/s)")                   # Set title of figure
            self.plot31.set_ylabel("Velocidade Linear(m/s)")    
            self.plot31.set_xlabel("Tempo(s)")                           # Set title of y axis
            self.plot31.legend(['Velocidade linear','Referência'])
            

            it = it+1
            
    
            # Aqui finaliza-se a função animate
            
        
        dataList = [ ]
        tempoList = [ ]
        referencia = [ ]
        V = [ ]  # Velocidade a ser plotada no modo dinâmico
        V1 =[ ] # Velocidade a ser plotada no modo estático  
        T = [ ]  # Tempo decorrido da simulação
        U = [ ]  # Sinal de controle
        R = [ ]  # Uma lista incluindo as referências
        


        self.fig31 = plt.figure()                                      # Plota a figura
        self.plot31 = self.fig31.add_subplot(111)         
        self.ani = animation.FuncAnimation(self.fig31, animate, frames=200, fargs=(dataList,tempoList),interval=213)
        self.canvas31 = FigureCanvasTkAgg(self.fig31, self.frame_aba31)   
        self.canvas31.draw() 
        self.canvas31.get_tk_widget().place(x = 50, y=50)
        self.ani.pause()


        #Inserção de uma nova figura para armazenar e plotar as variavéis de modo estático
        # Testando essa nova modalidade

        A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.fig32 = plt.figure()
        self.plot32 = self.fig32.add_subplot(111)
        self.line31, = self.plot32.plot(A,B) 
        self.line32, = self.plot32.plot(A,B)
        self.plot32.set_ylim([0,0.150])  
        self.plot32.grid(color ='b',linestyle = '-',linewidth=0.5)
        self.plot32.set_title("Velocidade da Esteira Transportadora (m/s)")                   # Set title of figure
        self.plot32.set_ylabel("Velocidade Linear(m/s)")    
        self.plot32.set_xlabel("Tempo(s)")                           # Set title of y axis
        self.plot32.legend(['Velocidade linear','Referência'])
        self.canvas32 = FigureCanvasTkAgg(self.fig32, self.frame_aba32)   
        self.canvas32.draw() 
        self.canvas32.get_tk_widget().place(x = 50, y=50)
        toolbar32 = NavigationToolbar2Tk(self.canvas32, self.frame_aba32)
        toolbar32.update()
        self.canvas32.get_tk_widget().place(x=50 ,y=50)


        # Cria botão e uma combobox para selecionar características do gráfico a ser plotado
        self.botao_34 =  Button(self.frame_aba32, width = 10, text = " Plotar", command = self.plot_32, borderwidth=3,  relief = "ridge", background = "blue", foreground = "white")
        self.botao_34.place(x=  500 , y =10)

        '''
        # Cria o botão que reseta as informações armazenada na lista de valores
        self.botao2_32 =  Button(self.frame_aba32,width=10, text = " Reset", command = self.reset_32, borderwidth=3, relief = "ridge" )
        self.botao2_32.place(x = 100  , y = 100)
        '''

        # Cria o label que informa sobre o tipo de dado
        self.label_33 = Label(self.frame_aba32, width= 10, text = "Dado: " )
        self.label_33["font"] =  ("Arial","8","bold")
        self.label_33.place( x=50, y=10)

    
        # Cria uma combobox que define o tipo de informação a ser plotado
        self.escolha_34 = Combobox(self.frame_aba32, justify = 'center', font = "Arial", values = ['Velocidade', 'Sinal de controle'])
        self.escolha_34.place(x = 110, y = 10)


        
        # Seleção dos parâmetro do controlador:
        self.label_34 =  Label(self.frame_aba3, text = "PARÂMETROS DO CONTROLADOR P.I:", background = "light gray")
        self.label_34["font"] = ("Arial","12","bold")
        self.label_34.place(x=100 , y=100)

        img31 = Image.open("PI.png")
        img31_resize =  img31.resize((277,112))
        self.imagem31 = ImageTk.PhotoImage(img31_resize)
        self.label39 = Label(self.frame_aba3, image= self.imagem31)
        self.label39.image= self.imagem31
        self.label39["background"]= "blue"
        self.label39.place( x= 110, y= 130)

        # Colocar uma figura representando um controlador P.I

        self.label_35 =  Label(self.frame_aba3, text = "Kp: ", background = "light gray")
        self.label_35["font"] = ("Arial","10","bold")
        self.label_35.place(x= 185 , y = 270)

        self.label_36 = Entry(self.frame_aba3, borderwidth = 2, relief= 'ridge', width = 5)
        self.label_36.place(x = 210 , y= 270)

        self.label_37 =  Label(self.frame_aba3, text = "Ki: ", background = "light gray")
        self.label_37["font"] = ("Arial","10","bold")
        self.label_37.place(x= 260 , y = 270)

        self.label_38 = Entry(self.frame_aba3, borderwidth= 2, relief = 'ridge', width=5)        
        self.label_38.place(x= 280 ,y=270)

        self.botao35 = Button(self.frame_aba3, text = "PLOTAR C(S)", background = 'blue', foreground = 'white', command = self.plot_cmf, borderwidth=1, relief = 'ridge')
        self.botao35.place(x = 215, y= 320)

        self.mensagem31 = Label(self.frame_aba3, text = "" , borderwidth= 6, relief= 'ridge')
        self.mensagem31["font"] = ("Arial","12",'bold')
        self.mensagem31.place(x = 130 , y= 370 )


        # Fim da seleção dos parâmetros
     
        self.abas31.add(self.frame_aba31, text = "Dinâmico")
        self.abas31.add(self.frame_aba32, text = "Estático")
        self.abas31.place(x =550, y =100)

    




        #Adiciona as respectivas abas
        self.abas.add(self.frame_aba1,text= "Início")
        self.abas.add(self.frame_aba2,text="Simulação")
        self.abas.add(self.frame_aba3,text="Controle")
        self.abas.place(x=15, y=100)


    def popup01(self):
        messagebox.showinfo("Inversor de Frequência", "O inversor de frequência é programado para acionar o motor trifásico com uma frequência proporcional ao sinal de tensão recebido em sua entrada analógica")


    def popup02(self):
        messagebox.showinfo("Esteira Transportadora", "A planta do sistema consiste em uma esteira transportadora, com diversas aplicações em linhas de produção industrial")

    def popup03(self):
        messagebox.showinfo("Sensor de Proximidade Indutivo", "O sensor indutivo detecta a presença de material metálico, alterando o estado lógico da saída. O equipamento utilizado trabalha com lógica invertida: a saída é 24V na ausência de material metálico e 0V na preseça de material metálico. ")
    
    def popup04(self):
        messagebox.showinfo("Motor de Indução Trifásico", "O motor de indução é acionado via inversor de frequência. Possui uma velocidade nominal, uma fator de potência, um rendimento. É acoplado em uma caixa de redução com relação de transformação igual a 80")

    def popup05(self):
        messagebox.showinfo("Artefato Metálico", "Artefato metálico fabricado para a detecção da rotação da esteira via sensor indutivo")

    def popup06(self):
        messagebox.showinfo("Circuito de Leitura", "O objetivo do circuito de leitura é adequar os níveis de tensão do sensor indutivo, para níveis compatíveis com a placa ESP-32")

    def popup07(self):
        messagebox.showinfo("ESP-32", "A placa ESP-32 é o microcontrolador do sistema. Ele é responsável por: realizar a leitura do sinal do sensor;  realizar a comunicação com o serial com a interface programada em Python; Enviar o sinal de controle para o acionamento da planta do sistema")

    def popup08(self):
        messagebox.showinfo("Circuito de Acionamento","O circuito de acionamento tem o propósito de adequar os níveis de tensão do sinal de controle enviado para o inversor de frequência")
        

    def popup09(self):
        messagebox.showinfo("Computador", "O computador é responsável por processar os dados de entrada e saída, e implementar o controlador no sistema das esteiras")

    def popup10(self):
        messagebox.showinfo("Malha Aberta", "Sistema de Controle em Malha Aberta")

    def popup11(self):
        messagebox.showinfo("Malha Fechada", "Sistema de Controle em Malha Fechada")

    def plotatfplanta(self):
        self.N0 = float(self.n0.get())
        self.N1 = float(self.n1.get())
        self.N2 = float(self.n2.get())
        self.N3 = float(self.n3.get())
        self.D0 = float(self.d0.get())
        self.D1 = float(self.d1.get())
        self.D2 = float(self.d2.get())
        self.D3 = float(self.d3.get())
        
        self.numerador = [self.N3, self.N2, self.N1, self.N0]
        self.denominador = [self.D3, self.D2, self.D1, self.D0]
        self.H_s = ctl.tf(self.numerador,self.denominador)
        self.mensagem["text"]= f"\n > Função de Transferência G(s): {self.H_s}"
    
    # Plota a Função de Transferência do Controlador
    def plotatfcontrolador(self):
        self.Kp = float(self.kp.get())
        self.Ki= float(self.ki.get())
        self.Kd = float(self.kd.get()) 

        self.C_s = ctl.tf([self.Kd,self.Kp,self.Ki],[1,0])
        
    
        self.mensagem2["text"] = f"\n >Função de Transferência C(S): {self.C_s}"

    
    def plotagrafico(self):
        global z
        # Adquire as características da simulação
        Temp_simu= float(self.temposimu.get())
        G1_s =ctl.series(self.H_s,self.C_s)
        MF_s=ctl.feedback(G1_s,sign = -1)
        
        if  (self.combo_Malha.get() == 'Malha Aberta'):
            MF_s = self.H_s


        if  (self.combo_Entrada.get() == 'Impulso'):
            T_mf,yout_mf = ctl.impulse_response(MF_s,Temp_simu)
            # Impulso
            n = np.arange(-2,Temp_simu,1)
            impulso = (n==0)*1
            degrau = impulso
            Temp_deg = n

        elif  (self.combo_Entrada.get() == 'Degrau'):
            T_mf,yout_mf = ctl.step_response(MF_s,Temp_simu)               
            # Degrau unitário
            Temp_deg = np.linspace(-0.2, Temp_simu, 1000)
            degrau = np.ones_like(Temp_deg)
            degrau[Temp_deg < 0] = 0

        elif  (self.combo_Entrada.get() == 'Rampa'):
            num = [1]
            den = [1, 0]
            self.I_s = ctl.tf(num,den)
            MFR_s= ctl.series(self.I_s, MF_s)
            T_mf,yout_mf = ctl.step_response(MFR_s,Temp_simu)  

            # Rampa
            Temp_deg = np.linspace(-0.2, Temp_simu, 1000)
            degrau = Temp_deg
            degrau[Temp_deg < 0] = 0

        elif (self.combo_Entrada.get() == 'Parábola'):
            num = [1]
            den = [1, 0, 0]
            self.I_s =  ctl.tf(num,den)
            MFP_s = ctl.series(self.I_s,MF_s)
            T_mf, yout_mf = ctl.step_response(MFP_s,Temp_simu)

            # Parábola
            Temp_deg = np.linspace(-0.2, Temp_simu, 1000)
            degrau = Temp_deg*Temp_deg
            degrau[Temp_deg < 0] = 0


        # Limpa o gráfico anterior e cria o novo
        # Fazendo alguns testes
        
        self.line1.set_data(T_mf, yout_mf)
        self.line2.set_data(Temp_deg,degrau)
        self.plot1.set_ylim(0,1.2*max(yout_mf))
        self.plot1.set_xlim(-2,Temp_simu)
        self.canvas1.draw()

        
    def plotagraficof(self):

        N0 = self.N0
        N1 = self.N1
        N2 = self.N2
        N3 = self.N3
        D0 = self.D0
        D1 = self.D1
        D2 = self.D2
        D3 = self.D3

        # Testa se o gráfico desejado é em Malha aberta ou Fechada
        if (self.combo_Malhaf.get() == "Malha Aberta"):
            # Cria o sistema em malha aberta 

            # Alternativa 02
            sysgenerico = self.H_s


            ###
            '''
            sysplanta = signal.TransferFunction([N3,N2,N1,N0],[D3,D2,D1,D0])
            sysgenerico = sysplanta
            '''

        elif (self.combo_Malhaf.get() == "Malha Fechada"):
            # Cria o sistema em malha fechada
            
            # Alternativa 02
            G1_s =ctl.series(self.H_s,self.C_s)
            MF_s=ctl.feedback(G1_s,sign = -1)
            sysgenerico = MF_s
            
            ###
            '''
            # Primeiro coloca o controlador e a planta em série
            Kp = self.Kp
            Ki = self.Ki
            Kd = self.Kd

            numeradorf   = [Kd*N3, N3*Kp+N2*Kd, N3*Ki+N2*Kp+N1*Kd,N2*Ki+N1*Kp+N0*Kd,N1*Ki+N0*Kp,N0*Ki]
            denominadorf = [Kd*N3, D3+N3*Kp+N2*Kd, D2+N3*Ki+N2*Kp+N1*Kd,D1 +N2*Ki+N1*Kp+N0*Kd, D0+N1*Ki+N0*Kp, N0*Ki]  
            sysmff = signal.TransferFunction(numeradorf,denominadorf)
            sysgenerico = sysmff
            '''

            
        '''
        w,mag,phase = signal.bode(sysgenerico)
        self.plot2.set_xscale('log')
        self.line3.set_data(w,mag)
    
        if ( (max(w))<0):
        self.plot2.set_ylim(1.2*min(mag), 0.8*max(w))

        else:
        self.plot2.set_ylim(1.2*min(mag), 1.2*max(w))

        
            '''
        self.fig22.clear()
        self.fig22 = plt.figure("Diagrama de Bode")
        ctl.bode_plot(sysgenerico, dB = True, deg = True)
        self.canvas2.draw()
        self.toolbar2.update()

    


    def plotagrafnyquist(self):

        N0 = self.N0
        N1 = self.N1
        N2 = self.N2
        N3 = self.N3
        D0 = self.D0
        D1 = self.D1
        D2 = self.D2
        D3 = self.D3

        
        # Testa se o gráfico desejado é em Malha aberta ou Fechada
        if (self.combo_Malha24.get() == "Malha Aberta"):
            # Cria o sistema em malha aberta 
            
            # Alternativa 02
            sysgenerico = self.H_s
            ##

            '''
            sysplanta = signal.TransferFunction([N3,N2,N1,N0],[D3,D2,D1,D0])
            sysgenerico = sysplanta
            '''

        elif (self.combo_Malha24.get() == "Malha Fechada"):
            # Cria o sistema em malha fechada
            # Primeiro coloca o controlador e a planta em série
            
            # Alternativa 02
            G1_s =ctl.series(self.H_s,self.C_s)
            MF_s=ctl.feedback(G1_s,sign = -1)
            sysgenerico = MF_s

            ##

            '''
            Kp = self.Kp
            Ki = self.Ki
            Kd = self.Kd

            numeradorf   = [Kd*N3, N3*Kp+N2*Kd, N3*Ki+N2*Kp+N1*Kd,N2*Ki+N1*Kp+N0*Kd,N1*Ki+N0*Kp,N0*Ki]
            denominadorf = [Kd*N3, D3+N3*Kp+N2*Kd, D2+N3*Ki+N2*Kp+N1*Kd,D1 +N2*Ki+N1*Kp+N0*Kd, D0+N1*Ki+N0*Kp, N0*Ki]  
            sysmff = signal.TransferFunction(numeradorf,denominadorf)
            sysgenerico = sysmff
            '''



        # Alternativa 02
        self.fig24.clear()
        self.fig24 = plt.figure("Diagrama de Nyquist")
        control.matlab.nyquist(sysgenerico)
        self.canvas4.draw()
        self.toolbar4.update()
        
        #

        '''
        W, H = signal.freqresp(sysgenerico)

        self.line5.set_data(H.real, H.imag)
        self.canvas4.draw()
        '''
    
    def plotalgr(self):

       
        G1_s = ctl.series(self.H_s,self.C_s)
       
        self.fig25.clear()
        self.fig25 = plt.figure("Diagrama do Lugar das Raízes", figsize =  (4.5,4.5), dpi=100)
        ctl.root_locus(G1_s,print_gain = True, grid = True)
        self.canvas5.draw()
        self.toolbar5.update()
        print("Teste")
        
        '''
        self.canvas5.draw()
        self.toolbar5.update()  
        '''

    def Seta(self):		#Seta a referência da interface
        global ref        
        '''
        self.ser.write(b'x')  # Reseta as informações de velocidade da placa
        self.ani.resume()
        ''' 
        ref = float(self.referencia.get())



    def Desliga(self):		#Define a atuação do primeiro 
        global V, T, U, referencia, ref, ek_1, uk_1, ek_1, tempoList, v_0, v_1, v_2, v_3, it,ref1_1,ref_1

        # Pausa a animação e para a esteira transportadora
        self.ani.pause()
        self.ser.write(b'1023w')
        self.botao_32["foreground"] = ("green")
        self.botao_33["foreground"] = ("black")

        # Jogar as variáveis para as condições iniciais nulas
        v_0, v_1, v_2, v_3, ek_1, uk_1, it, ref,ref_1,ref1_1 = 0,0,0,0,0,0,0,0,0,0
        V = [None]*100
        tempoList = [None]*100
        referencia = [None]*100



        # Limpa as informações do gráfico e cria um novo e estático
        self.plot31.clear()
        self.plot31.set_ylim([0,0.150])  
        self.plot31.grid(color ='b',linestyle = '-',linewidth=0.5)
        self.plot31.set_title("Velocidade da Esteira Transportadora (m/s)")                   # Set title of figure
        self.plot31.set_ylabel("Velocidade Linear(m/s)")    
        self.plot31.set_xlabel("Tempo(s)")
        
        # Reseta as variáveis calculadas encontradas




    	# Manda o número 01 pela porta serial

    def Liga(self):
        global V1,R,T,U
        V1 = [ ]
        R = [ ]
        T = [ ]
        U = [ ]

        self.ser.write(b'x') # Reseta as informações de velocidade da placa

        self.ani.resume()
        self.botao_33["foreground"] = ("red")
        self.botao_32["foreground"] = ("black")

    def plot_32(self):
        global V1,R,T,U
        self.dado = self.escolha_34.get()
        self.min = min(T)
        self.max = max(T)
        if (self.dado == "Velocidade"):
            self.line31.set_data(T,V1)
            self.line32.set_data(T,R)
            self.line32.set_visible(TRUE)
            self.plot32.set_xlim(self.min,self.max)
            self.plot32.set_ylim(0,0.150)
            self.plot32.set_ylabel("Velocidade Linear (m/s)")
            self.plot32.set_title("Velocidade da Esteira Transportadora (m/s)")
            self.plot32.legend(['Velocidade linear','Referência'])
            self.canvas32.draw()

        elif (self.dado == "Sinal de controle"):
            self.line31.set_data(T,U)
            self.line32.set_visible(FALSE)
            self.plot32.set_ylim(0,200)
            self.plot32.set_xlim(self.min,self.max)
            self.plot32.set_title("Sinal de controle")
            self.plot32.set_ylabel(" Sinal de controle (%V)")
            self.plot32.legend(['Sinal de Controle'])
            self.canvas32.draw()

    def plot_cmf(self):
        self.kp31 = float(self.label_36.get())
        self.ki31 = float(self.label_38.get())
        
        self.numerador31 = [self.kp31, self.ki31 ]
        self.denominador31 = [1,0]
        self.C_s31 = ctl.tf(self.numerador31,self.denominador31)
        self.mensagem31["text"]= f"\n > Função de Transferência C(s): {self.C_s31}"
    
        
        
            
    
root = Tk()
root.configure(background="light blue")
Interface(root)
root.mainloop()