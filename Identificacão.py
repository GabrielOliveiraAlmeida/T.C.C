import numpy as np
from scipy import *
import time
import serial
import scipy.io
from datetime import datetime 

# Programa que recebe um vetor de porcentagens [0 à 100 %] e coloca na entrada da planta através da comunicação serial
# Os intervalos entre duas amostras consecutivas é o tempo de amostragem Ts 
# O tempo que determinado sinal é mantido na saída será chamado de Tbs

# Inicialmente ler uma planilha no Excel e armazena os valores como um vetor coluna
 


# Primeiro conjunto de dados
P  = [20, 20, 20, 80, 20, 20, 80, 20, 80, 80, 20, 20, 80, 80, 80, 80, 80, 20, 20, 20, 80, 80, 20, 80, 80 , 80, 20, 80, 20, 80, 20, 20, 20, 20, 80,20,20,80,20,80,80,20,20,80,80,80,80,80,20,20,20,80,80,20,80,80,80,20,80,20,80,20,20,20,20,80,20,20,80,20,80,80,20,20,80,80,80,80,80,20,20,20,80,80,20,80,80,80,20,80,20,80,20,20,20,20,80,20,20,80] 

'''
# Segundo conjunto de dados (Validação)
P = [30, 30, 30, 50, 30, 30 , 50 , 30, 50, 50, 30, 30, 50, 50, 50, 50, 50, 30, 30, 30, 50, 50, 30, 50, 50, 50, 30, 50, 30, 50, 30, 30, 30, 30, 50, 30, 30, 50, 30, 50, 50, 30, 30, 50, 50, 50, 50, 50, 30, 30, 30, 50, 50, 30, 50, 50, 50, 30, 50, 30, 50, 30, 30, 30, 30, 50, 30, 30, 50, 30, 50, 50, 30, 30, 50, 50, 50, 50, 50, 30, 30, 30, 50, 50, 30, 50, 50, 50, 30, 50, 30 , 50 , 30 , 30 , 30,30 , 50, 30, 30, 50]
'''

n = 0
d = 2500
C = [None]*2500
V = [None]*2500
pi = 3.14159


for i in range(100):
    for l in range (25):
        
        C[l+n*25] =  P[i]
    n =  n + 1



ser = serial.Serial('COM3', 9600)
ler =  'r'
r = 0.0475 # Fator de conversão do eixo da esteira
t_0 = 0
t_1 = 0
t_2 = 0
t_3 = 0
t_4 = 0
n= 0 


for i in range(2500):
    C2 = C[i]*(1023/100)
    C2 = 1023 - C2 
    C2 = int(C2)
    Cstring = str(C2)
    Cstring = Cstring + 'w'
    try:
        
        ser.write(Cstring.encode())
        ser.write(ler.encode())
        tempo = ser.readline()
        tempo =  float(tempo)
    
    except:
        pass

    t_4 = t_3
    t_3 = t_2
    t_2 = t_1
    t_1 = t_0
    
    if (tempo == 0):
        t_0 = t_1
    else: 
        t_0 = (((pi)/3)/(tempo))*47.5
     

    if (t_0 >= 0.200):
        t_0 = t_1

    if  (n >= 4):
        V[i] = (t_4 + t_3 + t_2 + t_1 + t_0)/5
    else:
        V[i] = 0
    
    n= n + 1
    now = datetime.now()
    print(now)
    time.sleep(0.2) #Usar algum delay aqui

print(C)
print(V)
print("Identificação PRBS terminou")


    

    
    
    
    