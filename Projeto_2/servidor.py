#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np

import random

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName1 = "COM4"
serialName2 = "COM5"  
                # Windows(variacao de)
def computeBytes(bytearray):
    sum = 0
    for i in bytearray:
        sum += len(bytearray)
    return sum

def main():
    try:
        #com1 = enlace(serialName1)
        com2 = enlace(serialName2)
        #txtBuffer = ''
    
        com2.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação iniciada com sucesso")
     
        print('Vai começar a recepção')
        print("-------------------------")        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        rxBuffer, nRx = com2.getData(1)

        if rxBuffer == b'\n':
            comandoAnterior = b'\n'
            print("-------------------------")       
            print("O byte de inicio {} foi recebido".format((rxBuffer)))

            contaByte = 0
            LOOP = 1
            lenBuffer = com2.rx.getBufferLen()

            print("-------------------------")
            print("O tamanho da mensagem é {} comandos".format(lenBuffer))

            while lenBuffer > 0:
                print("O comando anterior foi {}".format(comandoAnterior))
                print("O buffer tem {} comandos".format(lenBuffer))

                if comandoAnterior != (b'\x04'):
                    comandoAnterior, nRxLoop = com2.getData(1)
                    lenBuffer -= 1
                    contaByte += 1
                
                else:
                    mensagem, nRxLoop = com2.getData(2)
                    comandoAnterior = mensagem[1]
                    lenBuffer -= 2
                    contaByte += 1
                
            print(contaByte)
                
      
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
