#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 12:14:00 2021

@author: Sebastian
"""

import socket
import os
import time
import hashlib
from _thread import *
import os
import datetime;
  
# Fecha y hora actual
ct = datetime.datetime.now()
print("current time:-", ct)

# Creamos carpeta para guardar log si no existe
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'Logs')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

lineas_log = []

#Creamos socket servidor
localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 1024
ThreadCount = 0
all_connections = []
all_address = []
tiempos_inicio = []
tiempos_fin = []
enviado = False


#msgFromServer       = "Hello UDP Client"

#bytesToSend         = str.encode(msgFromServer)


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

try:
    UDPServerSocket.bind((localIP, localPort))
except socket.error as e:
    print(str(e))

print("UDP server up and listening")


# Seleccion del archivo a enviar
file_name = input("Archivo a enviar:")
file_size = os.path.getsize(file_name)

#Seleccion de a cuantos clientes en simultaneo enviar
clientes_simultaneo = input("Enviar a cuantos clientes en simultaneo?:")

lineas_log.append("Archivo a enviar:"+file_name)
lineas_log.append("Tamaño del archivo:"+str(file_size))

#Creamos archivo de log
log_actual = final_directory+"/"+str(ct)+'-log.txt'

#Escribimos en el log el nombre de archivo y tamaño
"""
with open(log_actual, 'x') as f:
    f.write("Archivo a enviar:"+file_name)
    f.write('\n')
    f.write("Tamaño del archivo:"+str(file_size))
    f.write('\n')"""

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]


    clientIP  = "Cliente:{}".format(address)+",Mensaje:{}".format(message)
    
    ThreadCount += 1
    
    #Enviar tamano archivo
    #bytesToSend         = str.encode(str(file_size)+";"+str(ThreadCount))
    bytesToSend         = str.encode(str(file_size))
    UDPServerSocket.sendto(bytesToSend, address)
    
    all_address.append(address)

    
    
    print('Thread Number: ' + str(ThreadCount))
    
    print(clientIP)
    
    if int(ThreadCount) >= int(clientes_simultaneo) and enviado==False:
        print("Enviando archivo")
        
        continuar = True
        # Opening file and sending data.
        with open(file_name, "rb") as file:
            c = 0
            # Starting the time capture.
            
            paquetes=0
            
            # Running loop while c != file_size.
            #while c <= file_size:
            while continuar == True:
                print("Enviando:"+str(c))
                data = file.read(bufferSize)
                if not (data):
                    #break
                    for adds in all_address:
                        end_time = time.time()
                        tiempos_fin.append(end_time)
                    continuar = False
                    continue
                    
                for adds in all_address:
                    if paquetes==0:
                        start_time = time.time()
                        tiempos_inicio.append(start_time)
                    UDPServerSocket.sendto(data, adds)
                c += len(data)
                paquetes+=1
        
            # Ending the time capture.
            end_time = time.time()
            enviado= True
        print("Archivo Enviado")
        print("paquetes:"+str(paquetes))
        
        lineas_log.append("Archivo a enviar:"+file_name)
        
        print(all_address)
        print(tiempos_inicio)
        print(tiempos_fin)
        
        for a, i, f in zip(all_address, tiempos_inicio, tiempos_fin):
            tiempo = f-i
            linea = "cliente:"+str(a[1])+"-Tiempo_transferencia:"+str(tiempo)
            lineas_log.append(linea)
            
            
        with open(log_actual, 'w') as f:
            f.write('\n'.join(lineas_log))   
        

        """
        for adds in all_address:

            UDPServerSocket.sendto(file_name,adds)
            
            f=open(file_name,"rb")
            data = f.read(buf)
            while (data):
                if(UDPServerSocket.sendto(data,adds)):
                    print ("sending ...")
                    data = f.read(buf)
            f.close()"""
   
 
    
UDPServerSocket.close()

