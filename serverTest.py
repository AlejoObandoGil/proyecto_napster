# server.py
from xmlrpc.server import SimpleXMLRPCServer
# from SimpleXMLRPCServer import SimpleXMLRPCServer
import os

server = SimpleXMLRPCServer(('localhost', 9000))

def server_receive_file(arg):
    with open("musica/cliente1/descargas/prueba.mp3", "wb") as handle:
        handle.write(arg.data)
        
        return True          

print("Server on")
server.register_function(server_receive_file)
server.serve_forever()



