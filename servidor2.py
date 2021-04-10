from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import os
import threading
from tinytag import TinyTag, TinyTagException
## Python 3.7
## Servidor Secundario o Espejo RPC: 
# Los clientes se conectan en segunda instancia con este servidor,
# si el servidor Principal tiene una excepcion o falla

# ----------------------------------- CONFIGURACION DE SERVIDOR -----------------------------------------
# ---------------------------- CONFIGURACION PARTE CLIENTE DEL SERVIDOR-------------------------------------

cliente1 = xmlrpc.client.ServerProxy('http://127.0.0.1:9899', allow_none=True)
cliente2 = xmlrpc.client.ServerProxy('http://127.0.0.1:9898', allow_none=True)

print("\n*****************************BETA NAPSTER RPC*************************************")    
print("Servidor NAPSTER Secundario escuchando...")

# socket.gethostname
host1 = "127.0.0.1"
port1 = 9799
host2 = "127.0.0.1"
port2 = 9798
portTest = 2869

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server1 = SimpleXMLRPCServer((host1, port1), requestHandler=RequestHandler, allow_none=True) 
server1.register_introspection_functions()

# Variables globales
username = ""
host = ""
port = 0
lsDataCli = []
lsNameTracks = []
lsDataTracks = []
lsTracks = []
lsFileTracks = []
lsTotalDataCli = []
lsTotalTracks = []
numTracks = 0

# Funcion que recibe los datos de las canciones de los clientes 
def dowloadDataClient(cliente):
    # Datos del cliente
    print("\n_______________________________________________________________________________________\n")
    print("\nCargando datos de cliente...")
    print(".....")
    # Recibimos la informacion de los clientes
    username = cliente.dataClient()
    lsTracks, numTracks, lsFileTracks = cliente.sendTrack(username) 
    lsAlbums, numAlbums, lsTracksAlbums, numTracksAlbums = cliente.sendAlbum(username) 


    global lsTotalDataCli
    lsTotalDataCli+=username 

    global lsTotalTracks
    lsTotalTracks+=lsTracks
    lsTotalTracks+=lsTracksAlbums

    print(username)

    # print("\nLISTA ARCHIVOS DE CANCIONES : ", lsFileTracks)            
    print("\nLISTA METADATOS DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)

    # print("\nLISTA DE ALBUMS: ", lsAlbums)
    # print("\nNUMERO DE ALBUMS: ", numAlbums) 
    print("\nLISTA METADATOS DE CANCIONES EN ALBUMS: ", lsTracksAlbums) 
    print("\nNUMERO DE CANCIONES EN ALBUMS: ", numTracksAlbums)  

    print("\nDatos del cliente " + username[0] +" cargados con exito!")
    print("\n______________________________________________________________________________________\n")

    
def searchTrack(song):
    newSong = ""
    for track in lsTotalTracks:
        if track[0] == song:
            newSong = track[0]
            print("\nCancion encontrada!")
    if newSong == "":
        print("\nNombre incorrecto. La cancion no se encuentra.")   
    print(newSong)


# Hilo Responsable de enviar informacion al servidor1
class clientThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
        # Ejecutando funciones de servidor  
         dowloadDataClient(cliente1)
         dowloadDataClient(cliente2)       

         print("\nLISTA TOTAL DE CLIENTES EXISTENTES AL SERVIDOR: ", lsTotalDataCli)
         print("\nNUMERO DE CLIENTES EXISTENTES EN EL SERVIDOR: ", len(lsTotalDataCli))

         print("\nLISTA TOTAL DE CANCIONES EXISTENTES AL SERVIDOR: ", lsTotalTracks)
         print("\nNUMERO DE CANCIONES EXISTENTES EN EL SERVIDOR: ", len(lsTotalTracks))

         
# Hilo Responsable de enviar informacion al servidor1
class serverThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
        # Ejecutando funciones de servidor  
         server1.register_function(searchTrack)
         print("Servidor Conectado...")
         server1.serve_forever()

clientSend = clientThread()
clientSend.start()   
serverSend = serverThread()
serverSend.start()          
    
         