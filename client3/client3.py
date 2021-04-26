import os
import threading
import json
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from sendAudioData2 import sendTrack, sendAlbum, sendTrackClient, sendAlbumClient
from menu2 import menu
# Python 3.7
# Cliente RPC
# ----------------------------------------------------CLIENTE--------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------CONFIGURACION CONEXION----------------------------------------------------
# Globales
# Servidor 1
host1 = "127.0.0.1"
port1 = 9998
# Servidor2
host2 = "127.0.0.1"
port2 = 9898

portTest = 2869
# direcciones para los clientes que se conecten
global host3
global port3
host3 = "127.0.0.1"
port3 = 9797
host4 = "127.0.0.1"
port4 = 9697
host5 = "127.0.0.1"
port5 = 9597

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

print("\n**************************************************NAPSTER RPC************************************************************")    

# Funcion que configura la conexion con los dos servidores
# Variables bandera para conocer el servidor al que esta conectado este cliente
def serverConection1():
    global clientConnected 
    clientConnected = False

    # Si el servidor1 esta activo se conecta con ese
    if clientConnected == False:
        try:
            # Crear conexion para un Servidor RPC, con el metodo client de xmlrpc 
            client = xmlrpc.client.ServerProxy('http://' + host1 + ':' + str(port1), allow_none=True)
            print("\nCliente conectando a servidor Principal...")
            clientConnected = True
            client.connectionExist(clientConnected)            
        except:
            print("\nError. No se puede establecer conexion a servidor Principal.")
            clientConnected = False
            
    return client

 # Si el servidor1 esta inactivo intenta conectar con servidor2
def serverConection2():
    global clientConnected2
    clientConnected2 = False
    if clientConnected2 == False: 
        try:          
            client = xmlrpc.client.ServerProxy('http://' + host2 + ':' + str(port2), allow_none=True)
            print("\nCliente conectando a servidor Secundario...")
            clientConnected2 = True
            client.connectionExist(clientConnected2)
        except:
            print("\nError. No se puede establecer conexion a servidor Secundario.")
            clientConnected2 = False
    else:
        print("\nError fatal. No consiguio conectarse con ningun servidor.")  
        clientConnected2 = False

    return client        
  

def dataClient1():

    global username
    username = "JonAlejo" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")

    if clientConnected:  
        print("\n", username, "ha iniciado sesion.\nTe conectaste al servidor Principal desde: Direccion: ", host1, " Puerto: ", port1)    
        print("La Direccion de ", username, "para escuchar a otros clientes es: ", host3, " y el puerto es: ", port3)
    return username, host3, port3  

def dataClient2():

    global username
    username = "JonAlejo" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")
 
    if clientConnected2 and clientConnected == False:  
        print("\n", username, "ha iniciado sesion.\nTe conectaste desde el servidor Secundario desde: Direccion: ", host2, " Puerto: ", port2)    
        print("La Direccion de ", username, "para escuchar a otros clientes es: ", host3, " y el puerto es: ", port3)
    return username, host3, port3  


# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class ClientThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         global desconected
         desconected = False
         global client1
         client1 = serverConection1()
         if clientConnected:
             
             username, host, port = dataClient1()
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
            
             client1.listenClientData(json_username, json_host, json_port)
             client1.listenClientSong(json_lsTracks, json_numTrack)
             client1.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
             print("\nSe han compartido tus archivos locales con el servidor Principal de NAPSTER RPC.")

             desconected = menu(client1, username)
  

# Hilo Responsable de enviar informacion al servidor2
class ClientThread2(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         global desconected
         desconected = False
         global client2
         client1 = serverConection1()
         client2 = serverConection2()
         if clientConnected2:           
             username, host, port = dataClient2()       
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
            
             client2.listenClientData(json_username, json_host, json_port)
             client2.listenClientSong(json_lsTracks, json_numTrack)
             client2.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
             print("\nSe han compartido una copia de tus archivos locales con el servidor Secundario de NAPSTER RPC.")
             if clientConnected == False:
                desconected = menu(client2, username)

#----------------------------------------FINAL CLIENTE----------------------------------------------    
#-------------------------------------------SERVIDOR------------------------------------------------
#---------------------------------------------------------------------------------------------------

#conexion tipo servidor para el cliente que quiere descargar una cancion 
serverCli = SimpleXMLRPCServer((host3, port3), requestHandler=RequestHandler, allow_none=True) 
serverCli.register_introspection_functions()
#conexion tipo servidor para el cliente que quiere descargar una cancion 
serverCli = SimpleXMLRPCServer((host4, port4), requestHandler=RequestHandler, allow_none=True) 
serverCli.register_introspection_functions()

def shareSong(json_nameFile, json_op):

    nameFile = json.loads(json_nameFile)
    op = json.loads(json_op)

    file = ""
    newNameFile = ""
    lsTracks = sendTrackClient()
    lsTrackAlbums, lsAlbums = sendAlbumClient()
    for track in lsTracks:
        if track[0] == nameFile or track[op] == nameFile:
            file = track[3]
            newNameFile = track[0]
            print("\nCompartiste un archivo! Nombre: ", track[0])

    for track in lsTrackAlbums:
        if track[0] == nameFile or track[op] == nameFile:
            file = track[3]
            newNameFile = track[0]
            print("\nCompartiste un archivo! Nombre: ", track[0])       

    if file == "":
        print("\nError. El archivo no fue encontrado!")

    return file, newNameFile


def shareAlbum(json_lsNameFile, json_op):

    lsNameFile = json.loads(json_lsNameFile)
    op = json.loads(json_op)

    lsFile = []
    lsNewNameFile = []
    lsTracks = sendTrackClient()
    lsTrackAlbums, lsAlbums = sendAlbumClient()

    for nf in lsNameFile:
        for track in lsTracks:
            if track[0] == nf[0] or track[op] == nf[0]:
                file = [track[0], track[1], track[2], track[3], track[4]]
                lsFile.append(file)

                print("\nCompartiste un archivo! Nombre: ", track[0])

        for track in lsTrackAlbums:
            if track[0] == nf[0] or track[op] == nf[0]:
                file = [track[0], track[1], track[2], track[3], track[4]]
                lsFile.append(file)
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

# Principal
if __name__=="__main__":

    clientSend = ClientThread()
    clientSend.start()
    clientSend2 = ClientThread2()
    clientSend2.start()
    clientServer = ClientServerThread()
    clientServer.start()        