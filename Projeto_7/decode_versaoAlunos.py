#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from suaBibSignal import *
import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy import signal
from scipy.fftpack import fft, fftshift
from math import *
import peakutils

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

dictNumbers = {
        0: [1336, 941],
        1: [1209, 697],
        2: [1336, 697],
        3: [1477, 697],
        4: [1209, 770],
        5: [1336, 770],
        6: [1477, 770],
        7: [1209, 852],
        8: [1336, 852],
        9: [1477, 852],
    }
list_Dig_freq_big = [1336,1209,1477]
list_Dig_freq_little = [941,697,770,852]

def encontra_digito(lista_freq):
    digit = ""
    u = 10
    big_freq = 0
    little_freq = 0
    global list_Dig_freq_big, list_Dig_freq_little
    for freq in lista_freq:
        for big in list_Dig_freq_big:
            if abs(big-freq) < u:
                big_freq = big
        
        for little in list_Dig_freq_little:
            if abs(little-freq) < u:
                little_freq = little
    
    digit_values_list = [big_freq,little_freq]

    for digit_, digit_value  in dictNumbers.items(): 
        if digit_values_list == digit_value:
            digit = digit_
    
    return digit

def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    objSignal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    freqDeAmostragem = fs
    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs#taxa de amostragem
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duration = 4 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print(" A captação de audio começará em 5 segundos")
    time.sleep(5)
   
   #faca um print informando que a gravacao foi inicializada
    print("A gravação foi inicializada")
    time.sleep(0.5)
   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 
    duracao = duration

   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs*duracao
   
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    dados = audio[:,0]
    y = dados

    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    # t = np.linspace(inicio,fim,numPontos)
    t = np.linspace(-duration/2,duration/2,fs*duration)

    # plot do gravico  áudio vs tempo!
    plt.plot(y)
    plt.grid()

    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = objSignal.calcFFT(y, fs)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
    freq_list = []
    index = peakutils.indexes(np.abs(yf), thres=0.2, min_dist=200)
    print("index de picos {}" .format(index))
    #printe os picos encontrados! 
    for freq in xf[index]:
        print("freq de pico sao {}" .format(freq))
        freq_list.append(freq)
    
    digito = encontra_digito(freq_list)


    
    
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    print(digito)
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
