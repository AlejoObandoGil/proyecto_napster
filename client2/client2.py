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
port3 = 9798
host4 = "127.0.0.1"
port4 = 9698

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

print("\n**************************************************NAPSTER RPC************************************************************")    

# Funcion que configura la conexion con los dos servidores
# Variables bandera para conocer el servidor al que esta conectado este cliente
global clientConnected 
clientConnected = False
global clientConnected2
clientConnected2 = False
# Si el servidor1 esta activo se conecta con ese
if clientConnected == False:
    try:
        # Crear conexion para un Servidor RPC, con el metodo client de xmlrpc 
        cliente1 = xmlrpc.client.ServerProxy('http://' + host1 + ':' + str(port1), allow_none=True)
        print("\nCliente conectando a servidor Principal...")
        clientConnected = True
        cliente1.connectionExist(clientConnected)
    except:
        print("\nError. No se puede establecer conexion a servidor Principal.")
        clientConnected = False
        # Si el servidor1 esta inactivo intenta conectar con servidor2
        if clientConnected == False: 
            global cliente2           
            cliente2 = xmlrpc.client.ServerProxy('http://' + host2 + ':' + str(port2), allow_none=True)
            print("\nCliente conectando a servidor Secundario...")
            clientConnected2 = True
            cliente2.connectionExist(clientConnected2)
        else:
            print("\nError. No se puede establecer conexion a servidor Secundario.")  
            clientConnected2 = False
else:
    print("\nError fatal. No consiguio conectarse con ningun servidor.")             


def dataClient():

    global username
    username = "Thanos" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")

    if clientConnected == True:  
        print("\n", username, " ha iniciado sesion.\nTe conectaste al servidor Principal desde: Direccion: ", host1, " Puerto: ", port1)    
        print("La Direccion de ", username, "para conectarse a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3   

    if clientConnected2 == True:  
        print("\n", username, "ha iniciado sesion.\nTe conectaste desde el servidor Secundario desde: Direccion: ", host2, " Puerto: ", port2)    
        print("La Direccion de ", username, "para conectarse a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3    

    return 0        

# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class ClientThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
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
         
         cliente1.listenClientData(json_username, json_host, json_port)
         cliente1.listenClientSong(json_lsTracks, json_numTrack)
         cliente1.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
         print("\nSe han compartido tus archivos locales con el servidor Principal.")
         menu(cliente1, username) 

# Hilo Responsable de enviar informacion al servidor2
class ClientThread2(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         username, host, port = dataClient()       
         lsTracks, numTrack, lsFileTracks  = sendTrack(username)
         lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA = sendAlbum(username)

         json_username = json.dumps(username)
         json_host = json.dumps(host)
         json_port = json.dumps(port)  

         json_lsTracks = json.dumps(lsTracks)
         json_numTrack = json.dumps(numTrack)

         json_lsAlbums = json.dumps(lsAlbums)
         json_numAlbum = json.dumps(numAlbum)
         json_lsTrackAlbums = json.dumps(lsTrackAlbums)
         json_numTrackAlbum = json.dumps(numTrackAlbum)  
         
         cliente2.listenClientData(json_username, json_host, json_port)
         cliente2.listenClientSong(json_lsTracks, json_numTrack)
         cliente2.listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTrackAlbums, json_numTrackAlbum)
         
         print("\nSe han compartido tus archivos locales con el servidor Secundarios.") 
         menu(cliente2, username)
         print("\nPetición ejecutada con exito!")   

# Dependiendo el servidor a que este conectado Ejecuta los hilos 
if clientConnected == True: 
    clientSend = ClientThread()
    clientSend.start()

elif clientConnected2 == True:
    clientSend2 = ClientThread2()
    clientSend2.start()

else :
    print("\nError fatal al ejecutar servicios del cliente!")
#---------------------------------------FINAL CLIENTE-----------------------------------------------    
#------------------------------------------SERVIDOR-------------------------------------------------
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

    # json_file = json.dumps(file)

    return file # xmlrpc.client.Binary(file)

#--------------------------------------------------HILOS----------------------------------------------------------

# Hilo Servidor que atiende a otros clientes
class ClientServerThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self): 
         serverCli.register_function(shareSong)  

         serverCli.serve_forever()

clientServer = ClientServerThread()
clientServer.start()

#----------------------------------------------FINAL SERVIDOR-------------------------------------------------------
