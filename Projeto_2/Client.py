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
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName1 = "COM4"                 # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        com1 = enlace(serialName1)
        listaComandos = [255, 0, 15, 240, 255, 255]
        mensagem = bytearray(b'\n')
        contaBytes = 0
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        t0 = time.time()
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunicação iniciada com sucesso")
        
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        numeroDeBytes = random.randint(10,30)

        print("-------------------------")
        print("Vai começar a criar a mensagem")
        print("-------------------------")

        for num in range(0, numeroDeBytes):
            escolha = random.randint(0,5)

            comd = listaComandos[escolha]
            if (escolha == 0):
                mensagem.append(4)
                mensagem.append(0)
                mensagem.append(255)
                contaBytes += 2

            elif (escolha == 4):
                mensagem.append(4)
                mensagem.append(255)
                mensagem.append(0)
                contaBytes += 2

            else:
                mensagem.append(comd)
                contaBytes += 1
        
        #adicionando codigo de finalização da mensagem
        mensagem.append(5)

        print("Mensagem criada")
        print("-------------------------")

        print(bytearray(mensagem))
        
        print("Tamanho da mensagem")
        print("O tamanho da mensagem é de {}".format(len(mensagem)))
        
        print("-------------------------")
        #mensagemFinal = bytearray(mensagem)
        
        

        print("Enviando os dados")
        print("-------------------------")
        com1.sendData(mensagem)
        

        print("O tamanho de bytes enviado foi de {}".format(contaBytes))
        print("-------------------------")

        #agora vamos perguntar ao servidor se deu tudo certo com a mensagem
        print("Pedindo para o servidor a resposta!")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        
        rxBuffer, nRx = com1.getData(2)


        print("A resposta foi {} bytes".format(rxBuffer[1]))
        print("~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(1)

        
        print("VAMOS COMPARAR O NUMERO DE BYTES RECEBIDOS E ENVIADOS")
        time.sleep(1)
        print("-------------------------")
        print("Foram enviados {} bytes e foram recebidos {} bytes.".format(contaBytes, rxBuffer[1]))
        print("-------------------------")

        time.sleep(1)
        if (contaBytes) == (rxBuffer[1]):
            print("Deu tudo certo! A comunicação foi feita com sucesso!!!!")
        
        else: 
            print("Ops! Algo deu errado!")


        time.sleep(1)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        t1 = time.time()

        fullTime = t1-t0-4
        print("************************")
        print("O tempo de comunicação entre o client e o servidor foi de {}".format(fullTime))
        print("************************")
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
