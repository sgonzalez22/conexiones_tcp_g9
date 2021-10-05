#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 10:45:14 2021

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
   
# Creamos carpeta para guardar hash si no existe
final_directory2 = os.path.join(current_directory, r'Hash')
if not os.path.exists(final_directory2):
   os.makedirs(final_directory2)

    
lineas_log = []

    

#Creamos socket servidor
ServerSideSocket = socket.socket()
host = '127.0.0.1'
port = 2004
ThreadCount = 0
all_connections = []
all_address = []
enviado = False

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Socket is listening..')
ServerSideSocket.listen(5)


# Seleccion del archivo a enviar
file_name = input("Archivo a enviar:")
file_size = os.path.getsize(file_name)
lineas_log.append("Archivo a enviar:"+file_name)
lineas_log.append("Tamaño del archivo:"+str(file_size))

#Creamos archivo de log
log_actual = final_directory+"/"+str(ct)+'-log.txt'


#Seleccion de a cuantos clientes en simultaneo enviar
clientes_simultaneo = input("Enviar a cuantos clientes en simultaneo?:")

#Lectura del archivo y creacion de hash
BLOCK_SIZE = 65536 # The size of each read from the file
file_hash = hashlib.md5()
#file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
with open(file_name, 'rb') as f: # Open the file to read it's bytes
    fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
    while len(fb) > 0: # While there is still data being read from the file
        file_hash.update(fb) # Update the hash
        fb = f.read(BLOCK_SIZE) # Read the next block from the file

hash1 = file_hash.hexdigest()
hash2 = str.encode(hash1).hex()


#print (file_hash.hexdigest()) # Get the hexadecimal digest of the hash
print(hash2)
print(len(hash1))

#Escribimos en el log el nombre de archivo y tamaño
with open(log_actual, 'x') as f:
    f.write("Archivo a enviar:"+file_name)
    f.write('\n')
    f.write("Tamaño del archivo:"+str(file_size))
    #f.write("Hash:"+hash1)
    
#Escribimos en el archivo de hash
with open(final_directory2+"/"+'hash.txt', 'w') as f:
    f.write("Hash_servidor:"+hash1)

# Funcion para crear conexion con un cliente
def multi_threaded_client(connection):
    #connection.send(str.encode('Server is working:'))
    print("enviando nombre")
    connection.sendall(str.encode(file_name))
    print("enviando tamano")
    connection.sendall(str.encode(str(file_size)))

    
    #print("enviando hash")
    #connection.sendall(str.encode(hash1))

    while True:
        """data = connection.recv(2048)
        response = 'Server message: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(response))"""
        # Sending file_name and detail.
        #connection.send(file_name.encode())
        #connection.send(str(file_size).encode())
        #connection.sendall(str.encode(add))
    connection.close()


#Correr servidor y manejo de conexiones
while True:
    Client, address = ServerSideSocket.accept()
    all_connections.append(Client)
    all_address.append(address)
    
    actual = address[0] +":" +str(address[1])
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    #time.sleep(1)
    #print("enviando cliente")
    #Client.sendall(str.encode(str(ThreadCount)))    
    print("enviando conexiones")
    #Client.sendall(str.encode(str(clientes_simultaneo)))
    
    if int(ThreadCount) >= int(clientes_simultaneo) and enviado==False:
        print("Enviando archivo")
        
        # Opening file and sending data.
        with open(file_name, "rb") as file:
            c = 0
            # Starting the time capture.
            start_time = time.time()
        
            # Running loop while c != file_size.
            while c <= file_size:
                print("Enviando:"+str(c))
                data = file.read(1024)
                if not (data):
                    break
                for cliente in all_connections:
                    cliente.sendall(data)
                
                c += len(data)
        
            # Ending the time capture.
            end_time = time.time()
            enviado= True
        print("Archivo Enviado")
        
with open(log_actual, 'w') as f:
    f.write('\n'.join(lines))       
    
ServerSideSocket.close()