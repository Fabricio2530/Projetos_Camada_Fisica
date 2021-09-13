#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

def DATAGRAMA(nPacote, resposta=0):
    package = bytearray(b'\x01')
    package.append(nPacote) #numero do pacote
    package.append(0) #tamanho do payload
    package.append(4) 
    package.append(resposta)#resposta do servidor se deu certo ou nao 1-> deu certo 0-> Vish. Deu ruim!
    package.append(0) #Como servidor não precisa de payload, o numero de pacotes totais é 0
    for num in range(4):
        package.append(0)
    #adicionando o payload
    package.append(0)
    #adicionando o EOP
    for num in range(2):
        package.append(2)
        package.append(4)
        
    return package

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
        com2 = enlace(serialName2)
        com2.enable()
        print("Comunicação iniciada com sucesso")
        print("---------------------------")
        
     
        EOP_PADRAO = bytearray()
        EOP_PADRAO.append(2)
        EOP_PADRAO.append(4)
        EOP_PADRAO.append(2)
        EOP_PADRAO.append(4)


        '''
            ESPERANDO PELO HANDSHAKE
        '''
        #lendo a primeira parte da mensagem, o HEAD
        
        rxBuffer, nRx = com2.getData(10)
        
        if rxBuffer[4] == 1:
            print("HandShake recebido!!\n")
            #COM BASE NO HEAD DO HANDSHAKE, VAMOS CRIAR AS VARIAVEIS DA MENSAGEM
            NUM_ID = rxBuffer[1]
            TAMANHO_PAYLOAD = rxBuffer[2]
            TAMANHO_EOP = rxBuffer[3]
            TOTAL_PACKAGES = rxBuffer[5]
            print("SERAO RECEBIDOS AO TODO {}".format(TOTAL_PACKAGES))
            MENSAGEM = bytearray(b'\x01')

        TOTAL_PAYLOAD = bytearray()
        #Vamos terminar a leitura da primeira mensagem

        #mesmo se for dito que não tem nada no PAYLOAD, vai haver um valor 0

        if TAMANHO_PAYLOAD != 0:
            rxBuffer, nRx = com2.getData(TAMANHO_PAYLOAD)
        else:
            rxBuffer, nRx = com2.getData(1)
        print("PAYLOAD RECEBIDO NO HANDSHAKE:\n {}".format(rxBuffer))

        rxBuffer, nRx = com2.getData(TAMANHO_EOP)
        print("EOP RECEBIDO NO HANDSHAKE:\n {}".format(rxBuffer))

        #AGORA QUE JÁ VERIFICAMOS TUDO, PRECISAMOS RESPONDER O CLIENT
        response  = DATAGRAMA(NUM_ID, 1)
        com2.sendData(response)
        time.sleep(0.5)

        '''
            recepção da mensagem
        '''

        while NUM_ID < TOTAL_PACKAGES:
            print("Estamos no package {}\n".format(NUM_ID))
            #vamos tentar receber o primeiro pacote
            time.sleep(1)
            mensagem, nMensagem = com2.getData(10) #primeiro temos que ler o HEAD, ele quem diz quantos BYTES temos
            print(mensagem)
            print(mensagem[0])
            if (mensagem[0] == b'\x01') or (mensagem[0] == 1):
                if (mensagem[1] <= NUM_ID):
                    print('FOI ENVIADO O MESMO PACOTE, POR FAVOR ENVIAR O PRÓXIMO\n')
                    reenvio = DATAGRAMA(NUM_ID)
                    com2.sendData(mensagem)

                else:
                    print('byte inicial recebido com sucesso\n')
                    tamanhoPayLoad = mensagem[2]
                    print('O tamanho do payload é de {}\n'.format(tamanhoPayLoad))
                    payload, npayLoad = com2.getData(tamanhoPayLoad)
                    print('Esse foi o payload recebido: \n{}\n'.format(payload))
                    tamanhoEOP = mensagem[3]
                    print('O tamanho do EOP é de {}\n'.format(tamanhoEOP))
                    eop, nEOP = com2.getData(tamanhoEOP)
                    print('Esse foi o payload recebido: \n{}\n'.format(eop))

                    if eop == EOP_PADRAO:
                        print('O EOP foi recebido CORRETAMENTE\n')
                        TOTAL_PAYLOAD += payload
                        NUM_ID += 1
                        mensagem = DATAGRAMA(NUM_ID, 1)
                        #agora é preciso enviar a mensagem dizendo que deu tudo certo!!
                        com2.sendData(mensagem)

                    else:
                        print('O EOP NÃO FOI ENVIADO DA MANEIRA ADEQUADA, POR FAVOR REENVIAR O PACOTE\n')
                        reenvio = DATAGRAMA(NUM_ID)
                        com2.sendData(mensagem)

            else:
                print('Houve um erro com o envio do pacote')  

        newFile = open("IMG_SERVER.png", "xb")
        newFile.write(TOTAL_PAYLOAD)
        newFile.close()      

        

        



        
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
