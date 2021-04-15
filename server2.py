import os
import threading
import json
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

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

# Variables globales
lsTotalDataCli = []
lsTotalTracks = []

print("\n**************************************************NAPSTER RPC************************************************************")  
print("\nServidor NAPSTER Secundario escuchando...")


def connectionExist(clientConnected):
    print("Cliente conectado: ", clientConnected)

    return 0


def listenClientData(json_username, json_host, json_port):
    # Datos del cliente
    print("\n_____________________________________________________________________________________________________________________________________________________\n")
    print("\nCargando datos de cliente...")
    print(".....")
    # Recibimos la informacion de los clientes
    username = json.loads(json_username)
    host = json.loads(json_host)
    port = json.loads(json_port)

    global user
    user = username
    h = host
    p = port
    lsDataClient = [user, h, p]

    global lsTotalDataCli
    lsTotalDataCli.append(lsDataClient)

    print("DATOS DEL CLIENTE: ", lsDataClient)


def listenClientSong(json_lsTracks, json_numTrack):

    lsTracks = json.loads(json_lsTracks)
    numTrack = json.loads(json_numTrack)

    global lsTotalTracks
    lsTotalTracks+=lsTracks
               
    print("\nLISTA METADATOS DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTrack)
    

def listenClientAlbum(json_lsAlbums, json_numAlbum, json_lsTracksAlbums, json_numTrackAlbum):

    lsAlbums = json.loads(json_lsAlbums)
    numAlbum = json.loads(json_numAlbum)   
    lsTracksAlbums = json.loads(json_lsTracksAlbums)
    numTrackAlbum = json.loads(json_numTrackAlbum)

    global lsTotalTracks
    lsTotalTracks+=lsTracksAlbums

    print("\nLISTA DE ALBUMS: ", lsAlbums)
    print("\nNUMERO DE ALBUMS: ", numAlbum) 
    print("\nLISTA METADATOS DE CANCIONES EN ALBUMS: ", lsTracksAlbums) 
    print("\nNUMERO DE CANCIONES EN ALBUMS: ", numTrackAlbum)  

    print("\nDatos del cliente " + user +" cargados con exito!")
    print("\n_____________________________________________________________________________________________________________________________________________________\n")

    print("\nLISTA TOTAL DE CLIENTES EXISTENTES EN EL SERVIDOR: ", lsTotalDataCli)
    print("\nNUMERO DE CLIENTES EXISTENTES EN EL SERVIDOR: ", len(lsTotalDataCli))

    print("\nLISTA TOTAL DE CANCIONES EXISTENTES EN EL SERVIDOR: ", lsTotalTracks)
    print("\nNUMERO DE CANCIONES EXISTENTES EN EL SERVIDOR: ", len(lsTotalTracks))
    
    
# Funcion para buscar una cancion alojada en el servidor
def searchTrack(search, op):
    newSong = []
    lsNewSong = []
    lsNewDir = []
    # Recorre la lista lsTotalTracks e itera cada cancion en track
    for track in lsTotalTracks:
        # Se busca la cancion por los dos primeros posiciones de la lista
        # nombre del archivo y titulo del archivo
        if track[0] == search or track[op] == search:
            newSong = [track[0], track[1], track[2], track[3], track[4], track[5]]
            # S la cancion se encuentra gardamos todos sus datos en una lista y guardamos en una lista de listas
            lsNewSong.append(newSong)
            # Ahora comparamos los usuarios para conocer su puerto y direccion
            for usern in lsTotalDataCli:
                if usern[0] == newSong[5]:
                    # Guardamos en una lisat de listas
                    lsNewDir.append(usern)
            if op == 1:
                message = "Cancion encontrada!"           
                print("\n" + message)
            else:
                message = "Artista encontrado!"           
                print("\n" + message)

    # Si la lista esta vacia no encontro ninguna cancion        
    if len(lsNewSong) == 0 and op == 1:
        message = "Nombre incorrecto. La cancion no se encuentra!"
        print("\n" + message)
    elif  len(lsNewSong) == 0 and op == 2:
        message = "Nombre incorrecto. El artista no se encuentra!"
        print("\n" + message)   

    print(lsNewSong)

    json_lsNewSong = json.dumps(lsNewSong)
    json_newDir = json.dumps(lsNewDir)   
    json_message = json.dumps(message)

    return json_lsNewSong, json_newDir, json_message
# ------------------------------------PROGRAMA PRINCIPAL E HILOS SERVIDOR----------------------------------------
                 
# Hilo Responsable de recibir infomacion de los clientes
class ServerThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)

	def run(self):
        # Ejecutando funciones de servidor  
         server1.register_function(connectionExist)      
         server1.register_function(listenClientData)
         server1.register_function(listenClientSong)
         server1.register_function(listenClientAlbum)
        #  server1.handle_request()

         server1.register_function(searchTrack)
         server1.serve_forever()
         
        
# Hilo Responsable del buscador de musica y enviar datos de musica encontrada
class ServerThread2(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)

	def run(self):
        
         server2.register_function(connectionExist)    
         server2.register_function(listenClientData)
         server2.register_function(listenClientSong)
         server2.register_function(listenClientAlbum)
         print("Servidor Conectado...")

         server2.register_function(searchTrack)
         print("Esperando Peticion del cliente...")

         server2.serve_forever()
        
# class ServerThread2(threading.Thread):
# 	def _init_(self):
# 		threading.Thread._init_(self)

# 	def run(self):         
        # server3.register_function(listenClientData)
        #  server3.register_function(listenClientSong)
        #  server3.register_function(listenClientAlbum)
        #  server3.register_function(searchTrack)
        #  print("Servidor Conectado...")
        #  server3.handle_request()
        #  server3.handle_request()
        #  server3.handle_request()
        #  print("cerrado")

if __name__=="__main__":

    serverReceive1 = ServerThread()
    serverReceive1.start()  
    serverReceive2 = ServerThread2()
    serverReceive2.start()    


  





      
    
         


