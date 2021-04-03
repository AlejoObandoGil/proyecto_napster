from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os
from tinytag import TinyTag, TinyTagException
## Python 3_7
## Servidor RCP

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Create server
server = SimpleXMLRPCServer(("localhost", 9999),
                            requestHandler=RequestHandler)
server.register_introspection_functions()

def conexionCli ():
    suma = 3 + 5 
    print("conectado con el clente, la suma es: ", suma)
    return suma


def main():

    tracks = []
    tracksDuration = []
    # tag = TinyTag.get('D:\\musica\\ares\\gondwana - mi princesa(2)167.mp3')
    # print('This track is by %s.' % tag.artist)
    # print('It is %c seconds long.' % tag.duration)

    for root, dirs, files, in os.walk("D:\\musica\\alejo\\alejo"):
        
        for name in files:
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac")):
                tracks.append(name)
                try:
                    temp_track = TinyTag.get(root + "\\" + name)
                    print(temp_track.artist, "-", temp_track.title, "-", temp_track.duration)
                    tracksDuration.append(temp_track.duration)
                except TinyTagException:
                    print("Error")

    return tracks, tracksDuration
main()    
    
server.register_function(conexionCli)
server.register_function(main)

print ("Server listening...")
# Run the server's main loop
server.serve_forever()
