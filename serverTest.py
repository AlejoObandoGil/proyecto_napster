# server.py
from xmlrpc.server import SimpleXMLRPCServer
import os

server = SimpleXMLRPCServer(('localhost', 9000))

def server_receive_file(self,arg):
        with open("doc\\proy.txt", "wb") as handle:
            handle.write(arg.data)
            handle.close()
            return True          

print("Server on")
server.register_function(server_receive_file, "server_receive_file")
server.serve_forever()



