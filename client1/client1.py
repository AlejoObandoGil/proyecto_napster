import os
import sys
import threading
import json
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from sendAudioData1 import sendTrack, sendAlbum, sendTrackClient, sendAlbumClient
from menu1 import menu
# Python 3.7
# Cliente RPC
# ----------------------------------------------------CLIENTE--------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------CONFIGURACION CONEXION----------------------------------------------------
# Globales 
# Servidor 1
host1 = "127.0.0.1"
port1 = 9999
# Servidor2
host2 = "127.0.0.1"
port2 = 9899

portTest = 2869
# direcciones para los clientes que se conecten
global host3
global port3
host3 = "127.0.0.1"
port3 = 9799
host4 = "127.0.0.1"
port4 = 9699

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

print("\n**************************************************NAPSTER RPC************************************************************")  

# Funcion que configura la conexion con los dos servidores
# Variables bandera para conocer el servidor al que esta conectado este cliente
def serverConection():
    global clientConnected 
    clientConnected = False
    global clientConnected2
    clientConnected2 = False
    # Si el servidor1 esta activo se conecta con ese
    if clientConnected == False:
        try:
            # Crear conexion para un Servidor RPC, con el metodo client de xmlrpc 
            cliente = xmlrpc.client.ServerProxy('http://' + host1 + ':' + str(port1), allow_none=True)
            print("\nCliente conectando a servidor Principal...")
            clientConnected = True
            cliente.connectionExist(clientConnected)
            
        except:
            print("\nError. No se puede establecer conexion a servidor Principal.")
            clientConnected = False
            # Si el servidor1 esta inactivo intenta conectar con servidor2
            if clientConnected == False: 
                try:          
                    cliente = xmlrpc.client.ServerProxy('http://' + host2 + ':' + str(port2), allow_none=True)
                    print("\nCliente conectando a servidor Secundario...")
                    clientConnected2 = True
                    cliente.connectionExist(clientConnected2)
                except:
                    print("\nError fatal. No consiguio conectarse con ningun servidor.")
                    clientConnected2 = False
            else:
                print("\nError. No se puede establecer conexion a servidor Secundario.")  
                clientConnected2 = False
    else:
        print("\nError fatal. No consiguio conectarse con ningun servidor.")             

    return cliente

def dataClient():

    global username
    username = "Natalia" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")

    if clientConnected == True:  
        print("\n", username, "ha iniciado sesion.\nTe conectaste al servidor Principal desde: Direccion: ", host1, " Puerto: ", port1)    
        print("La Direccion de ", username, "para escuchar a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3  

    if clientConnected2 == True:  
        print("\n", username, "ha iniciado sesion.\nTe conectaste desde el servidor Secundario desde: Direccion: ", host2, " Puerto: ", port2)    
        print("La Direccion de ", username, "para escuchar a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3  

    return 0         

# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class ClientThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         global desconected
         desconected = False
         global client
         client = serverConection()
         if clientConnected:
             
             username, host, port = dataClient()
             lsTracks, numTrack = sendTrack(username)
             lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum = sendAlbum(username)
            
             json_username = json.dumps(username)
             json_host = json.dumps(host)
             json_port = json.dumps(port)  

             json_lsTracks = json.dumps(lsTracks)
             json_numTrack = json.dumps(numTrack)

             json_lsAlbums = json.dumps(lsAlbums)
             json_numAlbum = json.dumps(numAlbum)
             json_lsTrackAlbums = json.dumps(lsTrackAlbums)
             json_numTrackAlbum = json.dumps(numTrackAlbum)  
            
             client.listenClientData(json_username, json_host, json_port)
             client.listenClientSong(json_lsTracks, json_numTrack)
             client.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
             print("\nSe han compartido tus archivos locales con el servidor Principal de NAPSTER RPC.")

             desconected = menu(client, username)
              
        
            #  print(desconected)
            #  print("chao") 



# Hilo Responsable de enviar informacion al servidor2
class ClientThread2(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         global desconected
         desconected = False
         global client
         client = serverConection()
         if clientConnected2: 
             
             username, host, port = dataClient()       
             lsTracks, numTrack = sendTrack(username)
             lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum = sendAlbum(username)

             json_username = json.dumps(username)
             json_host = json.dumps(host)
             json_port = json.dumps(port)  

             json_lsTracks = json.dumps(lsTracks)
             json_numTrack = json.dumps(numTrack)

             json_lsAlbums = json.dumps(lsAlbums)
             json_numAlbum = json.dumps(numAlbum)
             json_lsTrackAlbums = json.dumps(lsTrackAlbums)
             json_numTrackAlbum = json.dumps(numTrackAlbum)  
            
             client.listenClientData(json_username, json_host, json_port)
             client.listenClientSong(json_lsTracks, json_numTrack)
             client.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
             print("\nSe han compartido tus archivos locales con el servidor Secundario de NAPSTER RPC.")

             desconected = menu(client, username)

            #  print(desconected)

        #  else:
        #      print("\nError fatal al ejecutar servicios del cliente!")                      

#----------------------------------------FINAL CLIENTE----------------------------------------------    
#-------------------------------------------SERVIDOR------------------------------------------------
#---------------------------------------------------------------------------------------------------

#conexion tipo servidor para el cliente que quiere descargar una cancion 
serverCli = SimpleXMLRPCServer((host3, port3), requestHandler=RequestHandler, allow_none=True) 
serverCli.register_introspection_functions()


def shareSong(json_nameFile, json_op):

    nameFile = json.loads(json_nameFile)
    op = json.loads(json_op)

    file = ""
    lsTracks = sendTrackClient()
    lsTrackAlbums, lsAlbums = sendAlbumClient()
    for track in lsTracks:
        if track[0] == nameFile or track[op] == nameFile:
            file = track[3]

            print("\nCompartiste un archivo! Nombre: ", track[0])

    for track in lsTrackAlbums:
        if track[0] == nameFile or track[op] == nameFile:
            file = track[3]
            print("\nCompartiste un archivo! Nombre: ", track[0])       

    if file == "":
        print("\nError. El archivo no fue encontrado!")

    return file 


def shareAlbum(json_lsNameFile, json_op):

    lsnameFile = json.loads(json_lsNameFile)
    op = json.loads(json_op)

    lsFile = []
    lsTracks = sendTrackClient()
    lsTrackAlbums, lsAlbums = sendAlbumClient()

    for nf in lsNameFile:
        for track in lsTracks:
            if track[0] == nf or track[op] == nf:
                lsFile.append(track[3])
                print("\nCompartiste un archivo! Nombre: ", track[0])

        for track in lsTrackAlbums:
            if track[0] == nf or track[op] == nf:
                lsFile.append(track[3])
                print("\nCompartiste un archivo! Nombre: ", track[0])       

    if len(lsFile) == 0:
        print("\nError. El archivo no fue encontrado!")

    return lsFile    


#--------------------------------------------------HILOS----------------------------------------------------------

# Hilo Servidor que atiende a otros clientes
class ClientServerThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self): 
        #  close = menu(client, username)

         serverCli.register_function(shareSong) 
         serverCli.register_function(shareAlbum)  
         serverCli.serve_forever()

    
#----------------------------------------------FINAL SERVIDOR-----------------------------------------------  


if __name__=="__main__":
    
    clientSend = ClientThread()
    clientSend.start()
    clientSend2 = ClientThread2()
    clientSend2.start()
    clientServer = ClientServerThread()
    clientServer.start()       

