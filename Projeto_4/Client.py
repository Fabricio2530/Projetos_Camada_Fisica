#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import sys
from termcolor import colored, cprint
from enlace import *
import time
import numpy as np
from math import *
from datetime import datetime
from crccheck.crc import Crc16, CrcXmodem
from crccheck.checksum import Checksum16


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName1 = "COM4"
serialName2 = "COM5"                # Windows(variacao de)

server_id = 27
sensor_id = 42
payload_max_size = 114
archive = "archive"
n_packages = 0

def crc(archive,n):

    data =  payload(archive,n,3)
    crc16 = Crc16.calc(bytearray(data))
    crc_ = crc16.to_bytes(2,"little")

    h8 = crc_[0]
    h9 = crc_[1]
    return h8,h9

def head(messageSize,n,type,nh6,nh7,h8=0,h9=0):
    global server_id, sensor_id,payload_max_size

 # h0 - tipo de mensagem
    h0 = type
    
 # h1 - id do sensor
    h1 = sensor_id

# h2 - id do servidor
    h2 = server_id

# h3 - número total de pacotes do arquivo
    h3 = ceil(messageSize/payload_max_size)

# h4 - número do pacote sendo enviado

    h4 = n

# h6 - pacote solicitado para recomeço quando há erro no envio
    if type == 6:
        h6 = nh6
    elif n == 0:
        h6 = 1
    else:
        h6 = n-1

# h5 :
    # tamanho do payload -> se tipo for dados
    if n == ceil(messageSize/payload_max_size):
        h5 = messageSize%payload_max_size
    else:
        h5 = payload_max_size

# h7 - último pacote recebido com sucesso
    if type == 6:
        h7 = nh7
    elif n == 0:
        h7 = 1
    else:
        h7 = n-1

# h8 e h9 - CRC ( por enquanto 00 )

    if int(type) == 1:
        # h0 - tipo de mensagem
        h0 = type
        # h5 :
            # id do arquivo -> se tipo for handshake
        h5 = 0
    else:
        print(f"\no tamanho do payload é de {h5}.")
    
    return bytearray([h0,h1,h2,h3,h4,h5,h6,h7,h8,h9])
    
def payload(archive,n,type):
    # A função pega a messagem e divide em pacotes de 114 bytes.
    payload_list = []
    if type == 3:
        n_bytes = payload_max_size
        payload_list= archive[n_bytes*(n-1):n_bytes*(n)]

    return payload_list

def eop():
    return bytearray([255,170,255,170])


def datagrama(archive,n_bytes,n,type,nh6,nh7):
    #Define o tamanho da mensagem e a quantidade de bytes a serem enviados
    messageSize = len(archive)
    packages = ceil(messageSize/n_bytes)
    # Calula CRC de 16 bits
    h8,h9 = crc(archive,n)
    #Geração do datagrama
    
    package = []

    package.extend(head(messageSize,n,type,nh6,nh7,h8=h8,h9=h9))

    package.extend(payload(archive,n,type))
    package.extend(eop())

    if type == 3:
        print(f"\nEnviando pacote de número {n}\n")
    elif type == 5:
        print("\nDevido a demora de resposta, a comunicação será encerrada\n")
    
    
    return bytearray(package)

def envia (client_,com1,archive,type,n,nh6=0,nh7=0):
    data = datagrama(archive,payload_max_size,n,type,nh6,nh7)
    # print(f"\n\n\n\n {data}\n\n\n")
    com1.sendData(np.asarray(data))
    h8 = data[8]
    h9 = data[9]
    CRC = str(h8.to_bytes(1, 'little') + h9.to_bytes(1,'little'))
    client(client_,"envia",type,len(data),n,CRC=CRC)

def recebe (client_,com1):
    rxBuffer, nRx = com1.getData(14)
    if len(rxBuffer) == 14:
        type = rxBuffer[0]
        h8 = rxBuffer[8]
        h9 = rxBuffer[9]
        CRC = str(h8.to_bytes(1, 'little') + h9.to_bytes(1,'little'))
        client(client_,"recebe",type,len(rxBuffer),rxBuffer[4],CRC=CRC)
        return (True,type,rxBuffer)
    else:
        return (False,[0],[0])

def client(client_,com,TYPE,packageSize,n,n_packages=n_packages,CRC=0000):
    if TYPE != 0:
        if TYPE == 3:
            line =  str(datetime.today())+" / "+str(com)+" / "+str(TYPE)+" / "+str(packageSize)+" / "+str(n)+" / "+str(n_packages)+" / "+str(CRC)
        else:
            line =  str(datetime.today())+" / "+str(com)+" / "+str(TYPE)+" / "+str(packageSize)
        
        newFile = open(f"Client1_2.txt", "a") #tem que ficar hardcoded pra cada tipo de teste
        newFile.writelines(line+"\n")
        newFile.close()
    else:
        pass
    




    

def main():
    global n_packages
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName1)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()

        archivePath = "img.jpg"

        with open(archivePath, "rb") as file:
            archive = file.read()
        
        archiveSize = len(archive)
        n_packages = ceil(archiveSize/payload_max_size)
        n = 0
        protocol = True
        inicia = False
        nh7 = 0

        # while True :
            #print(datagrama(archive,payload_max_size,67,3,0,0))
            # print(f"\n{payload(archive,1,3)}\n")
            # print("\n")
            # print(len(payload(archive,1,3)))
            # time.sleep(5)

        print("\nIniciando o protocolo de envio.\n")
        print(f"\nO número de pacotes a serem enviados são: {n_packages}.\n")
        print("\n-----------------------------------------------------------\n")
        print(f"Tamanho total do arquivo: {archiveSize}\n")
        while protocol :
            #Handshake
            t_hand = time.time()
            if not(inicia) :
                #Mensagem do tipo 1
                envia(1,com1,archive,1,n)
                time.sleep(5)
                t_hand_20 = (time.time()-t_hand)
                if t_hand_20 > 20:
                    sucesso,tipo,rxBuffer=recebe(3,com1)
                    print("Passaram-se 20 segundos e não recebida resposta de Hans Shake.\n")
                    t_hand = time.time()
                else:
                    sucesso,tipo,rxBuffer=recebe(1,com1)
                

                if sucesso and len(rxBuffer)==14 and rxBuffer[2] == server_id and tipo == 2:
                    print("\nHandshake feito com sucesso.\n")
                    print("\nprocesso de começará em instantes.\n")
                    print("------------------------------------\n\n\n")
                    n+=1
                    inicia = True
                    time.sleep(1)
                else :
                    print("\n...")

            else:
                
                if n <= n_packages:
                    # Mensagem do Tipo 3
                    envia(1,com1,archive,3,n,nh7=nh7)
                    it1 = True
                    timer1 = time.time()
                    timer2 = time.time()
                    t = time.time()
                    # Aguarda a resposta de recebimento
                    print("\nEsperando a confirmação...\n")
                    while (t - timer1  < 5)or(it1):
                        sucesso,type,msg = recebe(1,com1)
                        if sucesso:
                            it1 = False
                            break
                        t = time.time()
                        
                    # if sucesso:

                    if type == 4:
                        #Mensagem dizendo que recebeu o pacote com os dados corretos
                        nh7 = msg[7]
                        print(f"pacote {nh7}enviado corretamente")
                        client(1,"envio",msg[0],len(msg),n)
                        n = nh7 + 2
                    elif type == 6:
                        print("Pacote errado ou corrompido. Reenviando mensagem")
                        n = msg[6]

                    else:
                        it2 = True
                        envia(1,com1,archive,3,n)
                        timer1 = time.time()
                        t = time.time()
                        # Aguarda a resposta de recebimento
                        while (t - timer2  < 20)or(it2):
                            sucesso,type,msg = recebe(1,com1)
                            if sucesso:
                                it2 = False
                                break
                            t =time.time()
                        # if sucesso:
                        if type == 4:
                            #Mensagem dizendo que recebeu o pacote com os dados corretos
                            nh7 = msg[7]
                            n = nh7 + 1
                        elif type == 6:
                            print("Pacote errado ou corrompido. Reenviando mensagem")
                            n = msg[6]
                        else:
                            envia(5,com1,archive,5,n)
                            print("\nTime out\n")


                else:
                    print("\nDados enviados com sucesso.\n")
                    protocol = False
                    break


            
            
  
        #acesso aos bytes recebidos
        # txLen = len(txBuffer)
        # rxBuffer, nRx = com1.getData(txLen)
        # print("recebeu {}" .format(rxBuffer))
            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
