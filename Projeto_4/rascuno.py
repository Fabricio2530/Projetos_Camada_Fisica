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
from math import *

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

def head(messageSize,n,type,nh6=0,nh7=0):
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
    else:
        h6 = n-1

# h5 :
    # tamanho do payload -> se tipo for dados
    if messageSize-payload_max_size*n < payload_max_size:
        h5 = messageSize%payload_max_size
    else:
        h5 = payload_max_size

# h7 - último pacote recebido com sucesso
    if type == 6:
        h7 = nh7
    else:
        h7 = n-1

# h8 e h9 - CRC ( por enquanto 00 )
    h8 = 0
    h9 = 0

    if int(type) == 1:
        # h0 - tipo de mensagem
        h0 = type
        # h5 :
            # id do arquivo -> se tipo for handshake
        h5 = 0
    
    return bytearray([h0,h1,h2,h3,h4,h5,h6,h7,h8,h9])
    
def payload(archive,n,type):
    # A função pega a messagem e divide em pacotes de 114 bytes.
    payloas_list = []
    if type == 3:
        n_bytes = payload_max_size
        payload_list= archive[n_bytes*n:n_bytes*(n + 1)]

    return payload_list

def eop():
    return bytearray([255,170,255,170])


def datagrama(archive,n_bytes,n,type):
    #Define o tamanho da mensagem e a quantidade de bytes a serem enviados
    messageSize = len(archive)
    packages = ceil(messageSize/n_bytes)

    #Geração do datagrama
    
    package = []

    package.extend(head(messageSize,n,type))
    package.extend(payload(archive,n,type))
    package.extend(eop())
    
    if type == 3:
        # Messagens da Imagem
        pass
    elif type == 1:
        print(f"\nO número de pacotes a serem enviados são: {packages}.\n")
        print("\n-----------------------------------------------------------\n")
        # Handshake
        package.extend(head(messageSize,n,type))
        package.extend(eop())
    elif type == 5:
        print("Devido a demora de resposta, a comunicação será encerrada")
        package.extend(head(messageSize,n,type))
        package.extend(eop())
    
    
    return bytearray(package)
    

n = 0
for data in data_list:
    txBuffer = data
    if exit_for :
        break
    if n == 0:
        print(data)
        com1.sendData(np.asarray(data))
        ocioso = True
        tempo_hand = time.time()
        tempo_hand_relative = 0.0
        while ocioso:
            com1.sendData(np.asarray(data))
            tempo_hand_now = time.time()
            tempo_hand_relative = tempo_hand_now-tempo_hand
            print(tempo_hand_relative)

            if tempo_hand_relative >= 5:
                answer = input("Você quer tentar estabelecer conexão novamente. Aperte S para sim e N para não.").lower()
                if answer == "s":
                    tempo_hand = time.time()
                if answer == "n":
                    exit_for = True
                    problem_received = False
            else:
                    rxBuffer, nRx = com1.getData(14)
                    if len(rxBuffer) == 14 :
                        print("Handshake realizado com sucesso")
                        problem_received = False
        n += 1
    else:
        print(f'{n}//{len(data)}')
        n+= 1
    
print('saiu do loop')