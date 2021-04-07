import xmlrpc.client
import os
from tinytag import TinyTag, TinyTagException
## Python 3_7
## Servidor RPC

s = xmlrpc.client.ServerProxy('http://localhost:9999')

print("Servidor escuchando...")

print (s.buscarAlbum()) 
print (s.buscarCancion())