from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import threading
import os
from enviarDatos import sendTrack, sendAlbum
# Python 3.7
# Cliente RPC

# -------------------------------------------------CONFIGURACION CONEXION--------------------------------------------------
# socket.gethostname
host1 = "127.0.0.1"
port1 = 9999
host2 = "127.0.0.1"
port2 = 9899
portTest = 2869

cliente1 = xmlrpc.client.ServerProxy('http://127.0.0.1:9799', allow_none=True)


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

print("\n************************BETA NAPSTER RPC*******************************")  

def menu():
    print("\nMENU PRINCIPAL DE NAPSTER\n")
    song = input("Escribe el nombre de una cancion: ")

    return song

# Funcion que conecta con servidores
def conectionServer():
    # Variables bandera para conocer el servidor al que esta conectado este cliente
    global clientConnected 
    clientConnected = False
    global clientConnected2
    clientConnected2 = False
    # Si el servidor1 esta activo conecta con ese
    if clientConnected == False:
        try:
            # Crear conexion Servidor RPC 
            server1 = SimpleXMLRPCServer((host1, portTest), requestHandler=RequestHandler, allow_none=True) 
            server1.register_introspection_functions()
            print("\nCliente conectando a servidor Principal...")
            clientConnected = True

            return server1
        except:
            print("\nError. No se puede establecer conexion a servidor Principal")
            clientConnected = False
            # Si el servidor1 esta inactivo intenta conectar con servidor2
            if clientConnected == False:            
                server2 = SimpleXMLRPCServer((host2, port2), requestHandler=RequestHandler, allow_none=True) 
                server2.register_introspection_functions()
                print("\nCliente conectando a servidor Secundario...")
                clientConnected2 = True

                return server2
            else:
                print("\nError. No se puede establecer conexion a servidor Secundario")  
                clientConnected2 = False 
    else:
        pass 


def dataClient():

    global username
    username = "El_haker" # input("Digita un nombre de usuario para identificarte en NAPSTER: ")
    
    if clientConnected == True:  
        print("\nHola", username, "Bienvenido a NAPSTER.\nTe conectaste desde Direccion: ", host1, " Puerto: ", port1)    
    
        return username, host1, port1
    elif clientConnected2 == True:  
        print("\nHola", username, "Bienvenido a NAPSTER.\nTe conectaste desde Direccion: ", host2, " Puerto: ", port2)    
    
        return username, host2, port2 



# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

# Hilo Responsable de enviar informacion al servidor1
class serverThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
         # Ejecutando funciones de servidor  
        #  dataClient() 
        #  sendTrack(username)
        #  sendAlbum(username)
         # Funciones registradas para enviar a Servidor Principal
         server.register_function(dataClient)
         server.register_function(sendTrack)
         server.register_function(sendAlbum)  
        #  server.register_instance(instance)
         if clientConnected == True:
             print("\nDatos compartidos con servidor Principal correctamente...")   
         else:
             print("\nDatos compartidos con servidor Secundario correctamente...")          
        # Ejecutar servidor en escucha
         server.handle_request()

server = conectionServer()

# # Hilo Responsable de enviar informacion al servidor1
# class clientThread(threading.Thread):
# 	def __init__(self):
# 		threading.Thread.__init__(self)

# 	def run(self):
         

# Dependiendo el servidor a que este conectado Ejecuta los hilos 
if clientConnected == True or clientConnected2 == True:
    serverSend = serverThread()
    serverSend.start()   
    song = menu()
    cliente1.searchTrack(song)
else :
    print("Error fatal al ejecutar servicios del cliente.") 



# if 
# clientSend = clientThread()
# clientSend.start()




