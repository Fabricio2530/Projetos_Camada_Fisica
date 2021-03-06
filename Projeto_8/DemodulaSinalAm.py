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

def main():
 
    #declare um objeto da classe da sua biblioteca de apoio (cedida)    
    objSignal = signalMeu()
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    audio_arquivo = 'audio_modulado_am.wav'
    freqDeAmostragem = 44100    
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = freqDeAmostragem#taxa de amostragem
    sd.default.channels = 1  #voce pode ter que alterar isso dependendo da sua placa
    duracao = 4 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = freqDeAmostragem*duracao

    audio, samplerate = sf.read(audio_arquivo,frames=numAmostras)
    print(samplerate)
    audioAm = audio

    print(len(audioAm))

    # 9 - Verificando que o sinal possui frequência entre 10kHz e 18kHz

    xf, yf = objSignal.calcFFT(audioAm,freqDeAmostragem)
    plt.plot(xf, np.abs(yf))
    plt.title('Sinal modulado no regime da frequencia')
    plt.xlabel('frequencia hz')
    plt.ylabel('Amplitude')
    plt.show()

    # 10 - Filtrando frequências superiores a 4kHz

    audio_filtrado = filtro(audioAm, freqDeAmostragem, 4000)

    # 11 - Demodulando o audio Am e tocando ele

    fc = freqDeAmostragem
    fp = 14000
    portadora = objSignal.generateSin(14000, 1, 4, freqDeAmostragem)[1]
    #portadora = [sin(2*pi*fp*t)*fp for t in np.linspace(0,duracao,numAmostras)]

    sinal_demodulado = audio*portadora

    xf, yf = objSignal.calcFFT(sinal_demodulado,freqDeAmostragem)
    plt.plot(xf, np.abs(yf))
    plt.title('Sinal demodulado no regime da frequencia')
    plt.xlabel('frequencia hz')
    plt.ylabel('Amplitude')
    plt.show()

    #sinalDemodulado = [(sinal_filtrado[t])*(portadora[t]) for t in range(0,numAmostras)]
    audio_filtrado = LPF(sinal_demodulado,4000,freqDeAmostragem)

    xf, yf = objSignal.calcFFT(audio_filtrado,freqDeAmostragem)
    plt.plot(xf, np.abs(yf))
    plt.title('Sinal demodulado e filtrado no regime da frequencia')
    plt.xlabel('frequencia hz')
    plt.ylabel('Amplitude')
    plt.show()

    sd.play(audio_filtrado)
    sd.wait()
    print("...     FIM DO AUDIO\n")

if __name__ == "__main__":
    main()

    