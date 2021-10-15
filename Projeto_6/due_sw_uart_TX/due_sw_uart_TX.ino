#include "sw_uart.h"

due_sw_uart uart;

void setup() {
  Serial.begin(9600);
  sw_uart_setup(&uart, 4, 1, 8, SW_UART_EVEN_PARITY);
  pinMode(3,OUTPUT);
  digitalWrite(3,HIGH);
}

void loop() {
 send_byte();
 delay(1000);
}

void espera(){
    for(int i = 0; i < 2*1093; i++)
        asm("NOP");
}; 



void send_byte(){
    //vamos escrever de um modo "hardcoded"
    //a em ASCII = 01100001
    digitalWrite(3, LOW); //startBit
    espera();
    digitalWrite(3, HIGH); //0
    espera();
    digitalWrite(3,LOW); //1
    espera();
    digitalWrite(3,LOW); //1
    espera();
    digitalWrite(3,LOW); //0
    espera();
    digitalWrite(3,LOW); //0
    espera();
    digitalWrite(3,HIGH); //0
    espera();
    digitalWrite(3,HIGH); //0
    espera();
    digitalWrite(3,LOW); //1
    espera();
    digitalWrite(3,HIGH); //1 //paridade
    espera();
    digitalWrite(3,HIGH); //stopbit

}
