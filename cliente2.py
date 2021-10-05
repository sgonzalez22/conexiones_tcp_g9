#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 10:46:24 2021

@author: Sebastian
"""
import socket
import os
import time
import hashlib
import os




ClientMultiSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')
try:
    ClientMultiSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#res = ClientMultiSocket.recv(1024)
#ClientMultiSocket.send(str.encode("listo para empezar la recepción"))
#res = ClientMultiSocket.recv(100)
#print(res.decode('utf-8'))

#res = ClientMultiSocket.recv(1024)
#direccion = res.decode('utf-8')
while True:
    direccion = ClientMultiSocket.getsockname()
    print(direccion[1])

    # Send file details.
    print("Recibiendo nombre")
    file_name = ClientMultiSocket.recv(100).decode()
    
    print("Recibiendo tamano")
    file_size = ClientMultiSocket.recv(100).decode()
        
    #print("Recibiendo numero cliente")
    #num_cliente = ClientMultiSocket.recv(100).decode()
    
    #print("Recibiendo cantidad conexiones")
    #conexiones = ClientMultiSocket.recv(100).decode()
    
    #print("Recibiendo hash")
    #hash1 = ClientMultiSocket.recv(1024).hex()
    #hash1 = ClientMultiSocket.recv(32).hex()
   # print(hash1)
    

    #[Número  cliente]–Prueba- [Cantidad de conexiones].txt
    #("./ArchivosRecibidos/" + str(direccion[1])+"-Prueba-"+file_name , "wb")
    # Opening and reading file.
    #ruta_recepcion = "./ArchivosRecibidos/" + str(num_cliente)+"-Prueba-"+str(conexiones)+".txt" 
    ruta_recepcion = "./ArchivosRecibidos/" + str(direccion[1])+"-Prueba-"+".txt"
    with open( ruta_recepcion, "wb") as file:
        c = 0
        # Starting the time capture.
        start_time = time.time()
    
        # Running the loop while file is recieved.
        continuar = True
        while c <= int(file_size):
        #while continuar:
            print("Recibiendo:"+str(c))
            data = ClientMultiSocket.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)
            #if c==int(file_size):
                #continuar = False
    
        # Ending the time capture.
        end_time = time.time()
    
    print("File transfer Complete.Total time: ", end_time - start_time)
    #Lectura del archivo y creacion de hash
    BLOCK_SIZE = 65536 # The size of each read from the file
    file_hash = hashlib.md5()
    #file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
    with open(ruta_recepcion, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
        while len(fb) > 0: # While there is still data being read from the file
            file_hash.update(fb) # Update the hash
            fb = f.read(BLOCK_SIZE) # Read the next block from the file
    hash1 = file_hash.hexdigest()
    
    #Escribimos en el archivo de hash
    current_directory = os.getcwd()
    final_directory2 = os.path.join(current_directory, r'Hash')
    with open(final_directory2+"/"+'hash.txt', 'a') as f:
        f.write('\n'+"Hash_cliente:"+hash1)

#while True:
    #Input = input('Hey there: ')
    #ClientMultiSocket.send(str.encode("listo para empezar la recepción"))
    #res = ClientMultiSocket.recv(1024)
    #print(res.decode('utf-8'))

ClientMultiSocket.close()