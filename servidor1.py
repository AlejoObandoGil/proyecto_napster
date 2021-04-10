import os
import xmlrpc.client
from tinytag import TinyTag, TinyTagException
## Python 3.7
## Servidor Principal RPC: Los clientes se conectan en primera instancia con este servidor, si falla, los clientes conectaran con el servidor2

cliente1 = xmlrpc.client.ServerProxy('http://127.0.0.1:9999', allow_none=True)
# cliente2 = xmlrpc.client.ServerProxy('http://localhost:9998', allow_none=True)

print("\nBETA NAPSTER RPC")
print("Servidor Principal escuchando...")

lsNameTracks = []
lsDataTracks = []
lsTracks = []
lsFileTracks = []
numTracks = 0

print (cliente1.dataClient)
print (cliente1.searchTrack()) 
print (cliente1.searchAlbum()) 

print("\nLISTA DE CANCIONES: ", lsFileTracks)            
print("\nLISTA DE CANCIONES: ", lsTracks) 
print("\nNUMERO DE CANCIONES: ", numTracks)
print("\nLISTA DE NOMBRES DE CANCIONES: ", lsNameTracks)

# print (cliente2.dataClient)
# print (cliente2.searchTrack()) 
# print (cliente2.searchAlbum()) 


