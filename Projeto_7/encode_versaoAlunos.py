

#importe as bibliotecas
from suaBibSignal import *
import sys
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np7
from scipy import signal
from scipy.fftpack import fft, fftshift


def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def main():
    print("Inicializando encoder")
    
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

    #declare um objeto da classe da sua biblioteca de apoio (cedida)
    objSignal = signalMeu()

    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs = 44100
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = fs
    sd.default.channels = 1
    
    duration = 10 #tempo em segundos que ira emitir o sinal acustico 
      
    #relativo ao volume. Um ganho alto pode saturar sua placa... comece com .3    
    gainX  = 0.3
    gainY  = 0.3

    

    print("Gerando Tons base")
    
    #gere duas senoides para cada frequencia da tabela DTMF ! Canal x e canal y
    
   

    #use para isso sua biblioteca (cedida)
    #obtenha o vetor tempo tb.
    #deixe tudo como array
    t = np.linspace(-duration/2, duration/2, duration*fs)

    #printe a mensagem para o usuario teclar um numero de 0 a 9. 
    waitEntrada = True
    while waitEntrada:
        NUM = int(input('Insira um valor entre 0 e 9\n'))

        if type(NUM) == int:
            if (NUM >= 0) and (NUM <= 9):
               print('A entrada foi inserida correntamente')
               waitEntrada = False
        else:
            print('A entrada inserida não é um inteiro')


    #nao aceite outro valor de entrada.
    print("Gerando Tom referente ao símbolo : {}".format(NUM))

    freq = dictNumbers[NUM]
    print('As frequências são {0} + {1}'.format(freq[0], freq[1]))
    
    x1, y1 = objSignal.generateSin(freq[0],0.5,duration,fs)
    x2, y2 = objSignal.generateSin(freq[1],0.5,duration,fs)

    y = y1 + y2
  

    plt.figure()
    plt.plot(t[0:100], y[0:100], '.-')
    plt.grid()
    plt.show()
    
    X, Y = objSignal.calcFFT(y,fs)
    plt.figure("Fourier DTMF")
    plt.plot(X, np.abs(Y))
    plt.grid()
    plt.xlabel('Frequencia')
    plt.xlim(0,1500)
    plt.show()

    #construa o sunal a ser reproduzido. nao se esqueca de que é a soma das senoides
    
    #printe o grafico no tempo do sinal a ser reproduzido
    myrecording = sd.playrec(y, fs, channels=1)
    sd.wait()
    sd.play(myrecording)
    # reproduz o som
    #sd.play(tone, fs)
    # Exibe gráficos
    #plt.show()
    # aguarda fim do audio
    #sd.wait()

if __name__ == "__main__":
    main()
