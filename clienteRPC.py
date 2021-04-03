import xmlrpc.client
import os
from tinytag import TinyTag, TinyTagException
## Python 3_7
## Cliente RPC

s = xmlrpc.client.ServerProxy('http://localhost:9999')
print (s.conexionCli()) 
print (s.main()) 

