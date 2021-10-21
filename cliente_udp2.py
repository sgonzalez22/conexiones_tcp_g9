#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:34:19 2021

@author: Sebastian
"""
import socket
import os
import time
import hashlib
import os




serverAddressPort   = ("127.0.0.1", 20001)
bufferSize          = 1024

print('Conectando al servidor...')
try:
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
except socket.error as e:
    print(str(e))
    

 
# Enviar mensaje listo para recibir al servidor

msgFromClient       = "Listo para recibir"
bytesToSend         = str.encode(msgFromClient)
UDPClientSocket.sendto(bytesToSend, serverAddressPort)



#RECIBIR MENSAJE

msgFromServer = UDPClientSocket.recvfrom(bufferSize)
file_size = (msgFromServer[0])
#x=format(mensaje)
#x = mensaje.split(";")
#file_size = x[0]
#clientes = x[1]
print(file_size)



while True:
    direccion = UDPClientSocket.getsockname()
    print(direccion[1])
        

    print(os.getcwd())
    # Running the loop while file is recieved.
    continuar = True
    #ruta_recepcion = os.getcwd()+"/ArchivosRecibidos _udp/" + str(direccion[1])+"-Prueba-"+".txt"
    ruta_recepcion = os.getcwd()+"/ArchivosRecibidos/" + str(direccion[1])+"-Prueba-"+".xlsx"
    with open( ruta_recepcion, "wb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()
    
        # Running the loop while file is recieved.
        #continuar = True
        #while c <= int(file_size)+2*bufferSize:
        while continuar == True:
            print("Recibiendo:"+str(c))
            data,addr = UDPClientSocket.recvfrom(bufferSize)
            if not (data):
                #break
                continuar = False
                continue
            file.write(data)
            c += len(data)
            #if c==int(file_size):
                #continuar = False
    
        # Ending the time capture.
        end_time = time.time()
        print(end_time-start_time)
    
    print("File transfer Complete.Total time: ", end_time - start_time)



UDPClientSocket.close()