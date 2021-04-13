from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import os
from sendAudioData2 import sendTrack, sendAlbum, sendTrackClient, sendAlbumClient
# Python 3.7
# Cliente RPC

# ----------------------------------------------------CLIENTE--------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------CONFIGURACION CONEXION----------------------------------------------------
# direcciones para los servidores
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

print("\n****************************NAPSTER RPC**********************************")  

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

def main():
   
    while True:
        print("\nMENU PRINCIPAL DE NAPSTER")
        print(" 1. Buscar por canción")
        print(" 2. Buscar por artista")
        print(" 3. Buscar por álbum") 
        print(" 0. Salir") 
        opcion = input("Escribe el número de la opción para buscar: ")

        if opcion == "1":            
            song = input("Escribe el nombre de una cancion: ")
            songServer, titleServer, artistServer, durationServer, sizeServer, userServer, hostServer, portServer, message = cliente1.searchTrack(song)
            print(message)

            if durationServer == "":
                song = input("Escribe el nombre de una cancion: ")
                
            else:               
                print ("\n- Nombre cancion:",songServer,"- Titulo:", titleServer, "- artista:",artistServer,  "- duracion:",durationServer, "- tamaño:",sizeServer, "- usuario:",userServer)
                print ("host usuario:",hostServer, "port usuario:",portServer)

                clienteCliente = xmlrpc.client.ServerProxy('http://' + hostServer + ':' + str(portServer), allow_none=True)
                print("\nCliente local conectando a cliente" + username)

                file = clienteCliente.shareSong(song)
                print("Archivo listo")
                # print(file)
                while True:
                    print("\nMENU DE DESCARGA NAPSTER")
                    print(" 1. Descargar canción")
                    print(" 0. <- Atras")
                    opcion2 = input("Escribe el número de la opción: ")

                    if opcion == "1":
                        print("\nDescargando cancion...")
                        dir = "musica\\cliente1\\descargas\\" + song + ".mp3"
                        try:
                            download = open("musica\\cliente1\\descargas\\" + song + ".mp3", "wb")
                            download.write(file.data)
                        except:
                            print("Error al descargar cancion.")

                        download.close()
                        print("\nCancion descargada con exito!\nLa ubicacion del archivo es: ", dir)
                    elif opcion == "0":
                        break
            
        elif opcion == "2":
            song = input("Escribe el nombre de un artista: ")
                    
        elif opcion == "3":
            song = input("Escribe el nombre de un album: ")

        elif opcion == "0":
            print("\nCerrando cliente NAPSTER...")   
            break
    return song
# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class ClientThread(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         username, host, port = dataClient()
         lsTracks, numTrack = sendTrack(username)
         lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum = sendAlbum(username)
         
         cliente1.listenClientData(username, host, port)
         cliente1.listenClientSong(lsTracks, numTrack)
         cliente1.listenClientAlbum(lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum)
         print("\nSe han compartido tus archivos locales con el servidor Principal.")
         main()
         print("\nPetición ejecutada con exito!")   

# Hilo Responsable de enviar informacion al servidor2
class ClientThread2(threading.Thread):
	def _init_(self):
		threading.Thread._init_(self)      

	def run(self):
         username, host, port = dataClient()       
         lsTracks, numTrack, lsFileTracks  = sendTrack(username)
         lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA = sendAlbum(username)

         cliente2.listenClientData(username, host, port)
         cliente2.listenClientSong(lsTracks, numTrack, lsFileTracks)
         cliente2.listenClientAlbum(lsAlbums, numAlbum, lsTrackAlbums, numTrackAlbum, lsFileTracksA)
         print("\nSe han compartido tus archivos locales con el servidor Secundarios.") 
         main()
         print("\nPetición ejecutada con exito!")   

# Dependiendo el servidor a que este conectado Ejecuta los hilos 
if clientConnected == True: 
    clientSend = ClientThread()
    clientSend.start()
    # clientSearch = ClientThread3()
    # clientSearch.start()
elif clientConnected2 == True:
    clientSend2 = ClientThread2()
    clientSend2.start()
    # clientSearch = ClientThread3()
    # clientSearch.start()
else :
    print("\nError fatal al ejecutar servicios del cliente!")
#--------------------------------------FINAL CLIENTE-----------------------------------------------    

#--------------------------------------------SERVIDOR-----------------------------------------------
#---------------------------------------------------------------------------------------------------

#conexion tipo servidor para el cliente que quiere descargar una cancion 
serverCli = SimpleXMLRPCServer((host3, port3), requestHandler=RequestHandler, allow_none=True) 
serverCli.register_introspection_functions()

def shareSong (nameFile):
    file = ""
    lsTracks = sendTrackClient()
    for track in lsTracks:
        if track[0] == nameFile or track[1] == nameFile:
            file = track[2]
            print("Archivo listo")

    if file == "":
        print("\nEl archivo no fue encontrado")

    return file

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
