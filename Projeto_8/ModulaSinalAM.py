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
from funcoes_LPF import *

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def normaliza(array):
    return array/np.max(array)




def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    objSignal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    audio_arquivo = 'CardiB.wav'
    freqDeAmostragem = 44100


    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem#taxa de amostragem
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duracao = 4 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = freqDeAmostragem*duracao

    # 1 - leitura de audio

    audio, samplerate = sf.read(audio_arquivo,frames=numAmostras)
    yAudio = audio[:,0]
    samplesAudio = len(yAudio)
    # sd.play(audio)
    # sd.wait()
    # print("...     FIM")

    # 2 - normalização do audio

    yAudio_normalizado  = normaliza(yAudio)


    # 3 - Filtra as frequência acima de 4kHz

    audio_filtrado = filtro(yAudio_normalizado,freqDeAmostragem,4000)

    # 4 - Reproduzindo signal e verificando se ainda está audível

    sd.play(audio_filtrado)
    sd.wait()
    print("...     FIM DO AUDIO\n")


    # 5 - Modulando sinal de AM com portadora de 14kHz

    fp = 14000 # Frequência da senoide portadora

    portadora = [sin(2*pi*fp*t)*fp for t in np.linspace(0,duracao,numAmostras)]

    sinalAM = [(1+audio_filtrado[t])*portadora[t] for t in range(0,numAmostras)]

    # 6 - Executando e verificando que não está perfeitamente audível

    sd.play(sinalAM)
    sd.wait()
    print("...     FIM DO AUDIO\n")

    # 7 - envie o arquivo modulado 
    sf.write('audio_modulado_am.wav', sinalAM, freqDeAmostragem)   


    


    

    
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    # t = np.linspace(inicio,fim,numPontos)
    # t = np.linspace(-duration/2,duration/2,fs*duration)

    # plot do gravico  áudio vs tempo!

    # plt.plot(y)
    # plt.grid()

    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias

    # xf, yf = objSignal.calcFFT(y, fs)
    # plt.figure("F(y)")
    # plt.plot(xf,yf)
    # plt.grid()
    # plt.title('Fourier audio')
    

    #esta funcao analisa o fourier e encontra os picos
    #voce deve aprender a usa-la. ha como ajustar a sensibilidade, ou seja, o que é um pico?
    #voce deve tambem evitar que dois picos proximos sejam identificados, pois pequenas variacoes na
    #frequencia do sinal podem gerar mais de um pico, e na verdade tempos apenas 1.
    


    
    
    
    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    #print a tecla.
    
  
    ## Exibe gráficos
    # plt.show()

if __name__ == "__main__":
    main()
