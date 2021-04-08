import xmlrpc.client
import os
from tinytag import TinyTag, TinyTagException
## Python 3.7
## Servidor Secundario o Espejo RPC: Los clientes se conectan en segunda instancia con este servidor, si falla el servidor1

cliente1 = xmlrpc.client.ServerProxy('http://localhost:9899', allow_none=True)
# cliente2 = xmlrpc.client.ServerProxy('http://localhost:9898', allow_none=True)

print("\nBETA NAPSTER RPC")
print("Servidor Secundario escuchando...")

print (cliente1.dataClient)
print (cliente1.searchTrack()) 
print (cliente1.searchAlbum()) 

# print (cliente2.dataClient)
# print (cliente2.searchTrack()) 
# print (cliente2.searchAlbum()) 