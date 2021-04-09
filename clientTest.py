# client.py
import sys
import xmlrpc.client

proxy = xmlrpc.client.Server('http://localhost:9000')
with open("doc\\proy.txt", "rb") as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
proxy.server_receive_file(binary_data)
handle.close()

print("Client on")