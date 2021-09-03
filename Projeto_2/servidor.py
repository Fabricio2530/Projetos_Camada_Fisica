#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import time
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
        t0 = time.time()
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

            while comandoAnterior != (b'\x05'):
                print("O comando anterior foi {}".format(comandoAnterior))
                
                if comandoAnterior != (b'\x04'):
                    comandoAnterior, nRxLoop = com2.getData(1)
                    contaByte += 1
                
                else:
                    mensagem, nRxLoop = com2.getData(2)
                    comandoAnterior = mensagem[1]
                    contaByte += 1
            #É preciso retirar 1 byte da contagem no final porque ele contabiliza o byte de fim!
            contaByte -= 1

            print("-------------------------")
            print("O comando de fim da mensagem ({}) foi recebido".format(comandoAnterior))
            print("-------------------------")
            print("Foi recebido um total de {} bytes através da mensagem".format(contaByte))
                
        #agora vamos enviar de volta o que foi recebido, contando que deu tudo certo!
        print("-------------------------")
        print("Enviando ao client quantos bytes foram recebidos")
        response = bytearray(b'\n')
        response.append(contaByte)
        print(response)
        com2.sendData(response)
               
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")

        t1 = time.time()
        fullTime = t1-t0
        com2.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
