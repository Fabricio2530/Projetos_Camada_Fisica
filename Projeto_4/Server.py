#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from typing import Type
from enlace import *
import time
import numpy as np
from math import *
from datetime import datetime

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName1 = "COM4"
serialName2 = "COM5"                    # Windows(variacao de)

server_id = 27
sensor_id = 42
payload_max_size = 114
n_packages = 0
n_head = 10
eopSize = 4

def server(server,com,type,packageSize,n,n_packages=n_packages,CRC="0000"):
    if type == 3:
        line =  str(datetime.today())+" / "+str(com)+" / "+str(type)+" / "+str(packageSize)+" / "+str(n)+" / "+str(n_packages)+" / "+str(CRC)
    else:
        line =  str(datetime.today())+" / "+str(com)+" / "+str(type)+" / "+str(packageSize)
    
    newFile = open(f"Server{server}.txt", "a")
    newFile.writelines(line+"\n")
    newFile.close()



def head(n_packages,n,type,nh6,nh7):
    global server_id, sensor_id,payload_max_size

 # h0 - tipo de mensagem
    h0 = type
    
 # h1 - id do sensor
    h1 = sensor_id

# h2 - id do servidor
    h2 = server_id

# h3 - número total de pacotes do arquivo
    h3 = n_packages

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
    h5 = 0

# h7 - último pacote recebido com sucesso
    if type == 6:
        h7 = nh7
    elif n == 0:
        h7 = 1
    else:
        h7 = n-1

# h8 e h9 - CRC ( por enquanto 00 )
    h8 = 0
    h9 = 0

    if int(type) == 0:
        # h0 - tipo de mensagem
        h0 = 1
        # h5 :
            # id do arquivo -> se tipo for handshake
        h5 = 0
    
    return bytearray([h0,h1,h2,h3,h4,h5,h6,h7,h8,h9])

def eop():
    return bytearray([255,170,255,170])

def datagrama(n_packages,n_bytes,n,type,nh6,nh7):
    #Define o tamanho da mensagem e a quantidade de bytes a serem enviados
   
    

    #Geração do datagrama
    
    package = []

    package.extend(head(n_packages,n,type,nh6,nh7))
    package.extend(eop())

    if type == 2:
        print(f"Enviando pacote de número {n}")
    elif type == 1:
        print(f"\nO número de pacotes a serem enviados são: {n_packages}.\n")
        print("\n-----------------------------------------------------------\n")
    elif type == 5:
        print("Devido a demora de resposta, a comunicação será encerrada")
    
    
    return bytearray(package)

def envia (server_,com2,n_packages,type,n,nh6=0,nh7=0):
    data = datagrama(n_packages,payload_max_size,n,type,nh6,nh7)
    com2.sendData(np.asarray(data))
    server(server_,"envia",type,len(data),n)

def recebe (server_,com2,sizebuffer):
    
    rxBuffer, nRx = com2.getData(sizebuffer)
    if len(rxBuffer) == sizebuffer:
        type = rxBuffer[0]
        server(server_,"recebe",type,len(rxBuffer),rxBuffer[4])
        return (True,type,rxBuffer)
        
    else:
        print(f"Erro:Tamanho do buffer é {len(rxBuffer)}")
        return (False,[0],[0])
    
    

payload_list = bytearray()
def main():
    global n_packages,payload_list
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com2 = enlace(serialName2)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com2.enable()
        print("Comunicação serial inciada.\n\n")
        
        ocioso = True
        receiving = True
        n = 0
        print("\nocioso...\n")
        while receiving:
            while ocioso:
                # Mensagem do tipo 1
                sucesso,tipo,msg=recebe(1,com2,14)
                print("\nEsperando a confirmação...\n")
                if sucesso:
                    if tipo == 1 and msg[2] == server_id:
                        n_packages = msg[3]
                        ocioso = False
                        envia(1,com2,n_packages,2,n,nh7=0)
                        print("\n Mensagem recebida. Comunicação começaram em instantes.\n")
                        nh7 = n
                        n+=1
                time.sleep(1)
                
            if n <= n_packages:
                it1 = True
                timer1 = time.time()
                timer2 = time.time()
                t = time.time()
                while it1:
                   sucesso,tipo,msg= recebe(1,com2,n_head)
                   if sucesso:
                       if n == msg[4]:

                           payloadSize = msg[5]
                           print(f"\n\n\n\n n---> {n} payload-->{payloadSize}")
                           sucesso,tipo,msg=recebe(1,com2,payloadSize+eopSize)
                           print(f"\npacote ne número correto: {n}\n")
                           print(f"confirmando o número de payload: {len(msg)-4}")
                           print(f"ta funfando: {msg[payloadSize:payloadSize+eopSize]==eop()}")
                           print(f"{msg[payloadSize:payloadSize+eopSize]}")
                           print(f"{eop()}")
                           if sucesso and msg[payloadSize:payloadSize+4] == eop():
                               print(f"\nO package {n} foi recebido com sucesso\n")
                               payload_list+=msg[0:payloadSize]
                               envia(1,com2,n_packages,4,n,nh7=n)
                               nh7 = n
                               n+= 1
                               it1 = False
                        #    else:
                        #         print("\npacote enviado com conteudo errado, ou pacote errado\n")
                        #         print(f"\nesperando o pacote de número :{n}")
                        #         recebe(com2,118)
                        #         envia(com2,n_packages,6,n,nh6=n)
                        #         it1 = False
                       else:
                           if tipo == [0]:
                               pass
                           else:
                                print("\npacote errado\n")
                                print(f"\nesperando o pacote de número :{n}")
                                recebe(2,com2,118)
                                envia(2,com2,n_packages,6,n,nh6=n)
                                it1 = False
                   else:
                      time.sleep(1)
                      if time.time()-timer2 > 20:
                          ocioso = True
                          envia(5,com2,n_packages,5,n)
                          it1 = False
                          print("\n\nTime out.\n\n")
                          break
                      else:

                          if time.time()-timer1 >2:
                              envia(2,com2,n_packages,4,n,nh7=n)
                              timer1 = time.time()



            else:
                envia(1,com2,n_packages,4,n,nh7=n)
                print("Dados recebidos com sucesso")
                receiving= False
                break
            
            with open("img_server.jpg",'wb') as f:
                f.write(payload_list)
            
            


            
            


        
    
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
