import xmlrpc.client
import os
from tinytag import TinyTag, TinyTagException
## Python 3.7
## Servidor Principal RPC: Los clientes se conectan en primera instancia con este servidor, si falla, los clientes conectaran con el servidor2

cliente1 = xmlrpc.client.ServerProxy('http://localhost:9999', allow_none=True)
# cliente2 = xmlrpc.client.ServerProxy('http://localhost:9998', allow_none=True)

print("\nBETA NAPSTER RPC")
print("Servidor Principal escuchando...")

print (cliente1.dataClient)
print (cliente1.searchTrack()) 
print (cliente1.searchAlbum()) 

# print (cliente2.dataClient)
# print (cliente2.searchTrack()) 
# print (cliente2.searchAlbum()) 


