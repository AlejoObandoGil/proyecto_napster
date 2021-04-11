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

# socket.gethostname
# Direcciones para cada cliente
# CLiente1
host1 = "127.0.0.1"
port1 = 9899
# Cliente2
host2 = "127.0.0.1"
port2 = 9898
# CLiente3
host3 = "127.0.0.1"
port3 = 9897

# Direccion de servidor Secundario
# hostS = "127.0.0.1"
# portS = 8999

portTest = 2869

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Conexion para clientes
server1 = SimpleXMLRPCServer((host1, port1), requestHandler=RequestHandler, allow_none=True) 
server1.register_introspection_functions()
server2 = SimpleXMLRPCServer((host2, port2), requestHandler=RequestHandler, allow_none=True) 
server2.register_introspection_functions()
# server3 = SimpleXMLRPCServer((host3, port3), requestHandler=RequestHandler, allow_none=True) 
# server3.register_introspection_functions()

# # Conexion servidor secundario
# serverS = SimpleXMLRPCServer((hostS, portS), requestHandler=RequestHandler, allow_none=True) 
# serverS.register_introspection_functions()

# Variables globales
lsTotalDataCli = []
lsTotalTracks = []

print("\n*****************************BETA NAPSTER RPC*************************************")    
print("Servidor NAPSTER Secundario escuchando...")

def connectionExist(clientConnected):
    print("Cliente conectado: ", clientConnected)

    return 0

def listenClientData(username, host, port):
    # Datos del cliente
    print("\n______________________________________________________________________________________________________________________\n")
    print("\nCargando datos de cliente...")
    print(".....")
    # Recibimos la informacion de los clientes
    global user
    user = username
    h = host
    p = port
    lsDataClient = [user, h, p]

    global lsTotalDataCli
    lsTotalDataCli.append(lsDataClient)

    print("DATOS DEL CLIENTE: ", lsDataClient)

def listenClientSong(lsTracks, numTrack, lsFileTracks):

    global lsTotalTracks
    lsTotalTracks+=lsTracks
               
    print("\nLISTA METADATOS DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTrack)
    
def listenClientAlbum(lsAlbums, numAlbum, lsTracksAlbums, numTrackAlbum, lsFileTracksA):
    global lsTotalTracks
    lsTotalTracks+=lsTracksAlbums

    print("\nLISTA DE ALBUMS: ", lsAlbums)
    print("\nNUMERO DE ALBUMS: ", numAlbum) 
    print("\nLISTA METADATOS DE CANCIONES EN ALBUMS: ", lsTracksAlbums) 
    print("\nNUMERO DE CANCIONES EN ALBUMS: ", numTrackAlbum)  

    print("\nDatos del cliente " + user +" cargados con exito!")
    print("\n______________________________________________________________________________________________________________________\n")
    
# Funcion para buscar una cancion
def searchTrack(song):
    newSong = ""
# recorre la lista lsTotalTracks e itera cada cancion en track
    for track in lsTotalTracks:
        if track[0] == song:
            newSong = track[0]
            print("\nCancion encontrada!")
    if newSong == "":
        print("\nNombre incorrecto. La cancion no se encuentra.")   
    print(newSong)

    return newSong

# ------------------------------------HILOS SERVIDOR----------------------------------------
                 
# Hilo Responsable de recibir infomacion de los clientes
class serverThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
        # Ejecutando funciones de servidor  
         server1.register_function(connectionExist)      
         server1.register_function(listenClientData)
         server1.register_function(listenClientSong)
         server1.register_function(listenClientAlbum)
         server1.register_function(searchTrack)
         print("Servidor Conectado...")
         server1.handle_request()
         server1.handle_request()
         server1.handle_request()
         print("cerrado")

         server2.register_function(connectionExist)      
         server2.register_function(listenClientData)
         server2.register_function(listenClientSong)
         server2.register_function(listenClientAlbum)
         server2.register_function(searchTrack)
         print("Servidor Conectado...")
         server2.handle_request()
         server2.handle_request()
         server2.handle_request()
         print("cerrado")
         
        #  server3.register_function(connectionExist)  
        #  server3.register_function(listenClientData)
        #  server3.register_function(listenClientSong)
        #  server3.register_function(listenClientAlbum)
        #  server3.register_function(searchTrack)
        #  print("Servidor Conectado...")
        #  server3.handle_request()
        #  server3.handle_request()
        #  server3.handle_request()
        #  print("cerrado")

         print("\nLISTA TOTAL DE CLIENTES EXISTENTES EN EL SERVIDOR: ", lsTotalDataCli)
         print("\nNUMERO DE CLIENTES EXISTENTES EN EL SERVIDOR: ", len(lsTotalDataCli))

         print("\nLISTA TOTAL DE CANCIONES EXISTENTES EN EL SERVIDOR: ", lsTotalTracks)
         print("\nNUMERO DE CANCIONES EXISTENTES EN EL SERVIDOR: ", len(lsTotalTracks))

# Hilo Responsable de enviar copia de seguridad al servidor2
# class serverThread2(threading.Thread):
# 	def __init__(self):
# 		threading.Thread.__init__(self)

# 	def run(self):
#         # Ejecutando funciones de servidor 

# clientSend = clientThread()
# clientSend.start()   
# serverReceive = serverThread()
# serverReceive.start() 

serverReceive = serverThread()
serverReceive.start()          
    
         


