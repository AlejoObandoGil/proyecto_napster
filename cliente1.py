from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import os
from enviarDatos1 import sendTrack, sendAlbum
# Python 3.7
# Cliente RPC

# -------------------------------------------------CONFIGURACION CONEXION--------------------------------------------------
# socket.gethostname
# direcciones para los servidores
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

print("\n************************BETA NAPSTER RPC*******************************")  

# Funcion que conecta con servidores

# Variables bandera para conocer el servidor al que esta conectado este cliente
global clientConnected 
clientConnected = False
global clientConnected2
clientConnected2 = False
# Si el servidor1 esta activo se conecta con ese
if clientConnected == False:
    try:
        # Crear conexion para un Servidor RPC, con el metodo client de xmlrpc 
        cliente1 = xmlrpc.client.ServerProxy('http://127.0.0.1:9000', allow_none=True)
        print("\nCliente conectando a servidor Principal...")
        clientConnected = True
        cliente1.connectionExist(clientConnected)
    except:
        print("\nError. No se puede establecer conexion a servidor Principal.")
        clientConnected = False
        # Si el servidor1 esta inactivo intenta conectar con servidor2
        if clientConnected == False: 
            global cliente2           
            cliente2 = xmlrpc.client.ServerProxy('http://127.0.0.1:9899', allow_none=True)
            print("\nCliente conectando a servidor Secundario...")
            clientConnected2 = True
            cliente2.connectionExist(clientConnected2)

        else:
            print("\nError. No se puede establecer conexion a servidor Secundario.")  
            clientConnected2 = False
else:
    print("Error fatal. No consiguio conectarse con ningun servidor.")             


def dataClient():

    global username
    username = "Socrates" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")
    print("sdfsdsds")
    print(clientConnected)

    if clientConnected == True:  
        print("\nHola", username, "Bienvenido a NAPSTER.\nTe conectaste al servidor Principal desde: Direccion: ", host1, " Puerto: ", port1)    
        print("La Direccion de ", username, "para conectarse a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3  

    print(clientConnected2) 

    if clientConnected2 == True:  
        print("\nHola", username, "Bienvenido a NAPSTER.\nTe conectaste desde el servidor Secundario desde: Direccion: ", host2, " Puerto: ", port2)    
        print("La Direccion de ", username, "para conectarse a otros clientes es: ", host3, " y el puerto es: ", port3)
        return username, host3, port3       
    

def menu():
    print("\nMENU PRINCIPAL DE NAPSTER\n")
    song = input("Escribe el nombre de una cancion: ")

    return song

# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class clientThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)      

	def run(self):
         username, host, port = dataClient()
         lsTracks, numTrack, lsFileTracks  = sendTrack(username)
         lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA = sendAlbum(username)
         
         cliente1.listenClientData(username, host, port)
         cliente1.listenClientSong(lsTracks, numTrack, lsFileTracks)
         cliente1.listenClientAlbum(lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA)
         print("\nSe han compartido tus archivos locales con el servidor Principal de NAPSTER RPC.")

# Hilo Responsable de enviar informacion al servidor2
class clientThread2(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)      

	def run(self):
         username, host, port = dataClient()       
         lsTracks, numTrack, lsFileTracks  = sendTrack(username)
         lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA = sendAlbum(username)

         cliente2.listenClientData(username, host, port)
         cliente2.listenClientSong(lsTracks, numTrack, lsFileTracks)
         cliente2.listenClientAlbum(lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA)
         print("\nSe han compartido tus archivos locales con el servidor Secundarios de NAPSTER RPC.")          

# Dependiendo el servidor a que este conectado Ejecuta los hilos 
if clientConnected == True: 
    clientSend = clientThread()
    clientSend.start()
elif clientConnected2 == True:
    clientSend2 = clientThread2()
    clientSend2.start()
else :
    print("Error fatal al ejecutar servicios del cliente!") 






