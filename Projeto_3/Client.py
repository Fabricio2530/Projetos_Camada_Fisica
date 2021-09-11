#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import time
import random 
from enlace import *
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName1 = "COM4"    
             # Windows(variacao de)

def DATAGRAMA(n_id, mensagemInteira):
    #criando o bit inicial de toda mensagem
    package = bytearray(b'\x01')
    #adicionando o id
    package.append(n_id)
    
    if n_id == 0:
        #adicionando o tamanho do PayLoad
        package.append(0)
        #adicionando o tamanho do EOP
        package.append(4)
        #adicionando se é ou não handshake
        package.append(1)
        #adicionando o total de pacotes
        package.append(len(mensagemInteira))
        #adicionando 4 bytes vazios para completar o HEAD
        for num in range(4):
            package.append(0)

        #vamos adicionar agora o PayLoad
        package.append(0)

        #vamos adicionar o restante: o EOP
        for num in range(2):
            package.append(2)
            package.append(4)
    
    else:
        #adicionando o tamanho do PayLoad
        n = n_id-1
        print('O tamanho do payload é de {}\n'.format(len(mensagemInteira[n])))
        
        package.append(len(mensagemInteira[n]))
        #adicionando o tamanho do EOP
        package.append(4)
        #adicionando se é ou não handshake
        package.append(0)
        #adicionando o total de pacotes
        package.append(len(mensagemInteira))
        #adicionando 4 bytes vazios para completar o HEAD
        for num in range(4):
            package.append(0)

        #vamos adicionar agora o PayLoad
        package += (mensagemInteira[n_id-1])

        #vamos adicionar o restante: o EOP
        for num in range(2):
            package.append(2)
            package.append(4)

    return package
        

    

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.


        print('iniciando a comunicação')
        print('-----------------------')
        
        #iniciando o CLIENT
        com1 = enlace(serialName1)
        com1.enable()
       
        #lendo o arquivo que será enviado para o SERVER    
        with open('lua.jpg', 'rb') as binaryImage:
            binImage = binaryImage.read()
        
        #criando variáveis importantes
        fragmentacao = False
        NUM_ID = 0
        TAMANHO_PAYLOAD = 114
        
        #lista de PAYLOADS
        FRAGMENTO = [binImage[i: i+TAMANHO_PAYLOAD] for i in range(0, len(binImage), TAMANHO_PAYLOAD)]

        print("O total de pacotes necessários será de {}".format(len(FRAGMENTO)))
        print('------------------------')

        mensagem = DATAGRAMA(NUM_ID, FRAGMENTO) 

        print("Mensagem feita com sucesso!!")
        print("Vamos enviar o seguinte handshake:\n {}".format(mensagem))
        com1.sendData(mensagem)
        
        handshake = True

        while handshake:
            response, nResponse = com1.getData(15)
            print(response)
            if ((response == "")):
                question = input("Você quer tentar de novo? S/N\n")
                if question == "S":
                    pass
                else:
                    break
            else:

                print("---------------------------")
                print("HandShake feito com sucesso")
                print(len(response))
                handshake = False
                fragmentacao = True 
                NUM_ID += 1
        '''
            LOOP para envio do conteúdo da mensagem
        '''
        while fragmentacao:
            print("---------------------------")
            print("Estamos no package de id: {}".format(NUM_ID))
            if (NUM_ID > len(FRAGMENTO) ):
                fragmentacao = False
            else:
                mensagem = DATAGRAMA(NUM_ID, FRAGMENTO)
                print("---------------------------")
                print("O seguinte pacote foi criado:")
                print(mensagem)
                print("---------------------------")
                print("O pacote tem tamanho {}\n".format(len(mensagem)))
                
                #AGORA É PRECISO ENVIAR A MENSAGEM
                com1.sendData(mensagem)
                waitResponse = True 
                while waitResponse:
                    print('ESPERANDO RESPOSTA DO SERVIDOR\n')
                    response, nresponse = com1.getData(15)
                    
                    print('RESPOSTA RECEBIDA\n')
                    
                    nPacote = response[1]
                    resultadoEnvio = response[4]

                    if resultadoEnvio == 1:
                        print('O ENVIO DO PACOTE {} FOI UM SUCESSO\n'.format(NUM_ID))
                        NUM_ID += 1
                        waitResponse = False
                    
                    else:
                        print('O pacote não foi enviado corretamente\n')
                        waitResponse = False

        print('terminando a comunicação')
        print('------------------------')
        com1.disable()
       
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
