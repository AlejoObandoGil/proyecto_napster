from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import os
from tinytag import TinyTag, TinyTagException
# Python 3_7
# Cliente RCP

# -------------------------------------------------CONFIGURACION CONEXION--------------------------------------------------

host = "localhost"
port = 9999
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Crear Servidor
server = SimpleXMLRPCServer((host, port), requestHandler=RequestHandler) 
server.register_introspection_functions()

print("Cliente conectado...")

# ---------------------------------------FUNCIONES BUSCAR EN CARPETA LOCAL CLIENTE-----------------------------------------

# Esta funcion busca albumes. Los albumes estan en una carpeta diferente de las canciones individuales.
def searchTrack():
    lsNameTracks = []
    lsDataTracks = []
    lsTracks = []
    # Este for lee el directorio raiz, sus subcarpetas y archivos. El metodo walk sirve para leer un directorio
    numTracks = 0
    for root, dirs, files, in os.walk("D:\\musica\\Musica alejo"):

        for name in files:
            # Si extension del archivo es tipo musica agregamos a lista
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma")):
                lsNameTracks.append(name)
                try:
                    # Creamos un objeto tinyTag por cada cancion y obtenemos sus metadatos y los guardamos en una lista
                    temp_track = TinyTag.get(root + "\\" + name)
                    duration = str(temp_track.duration)
                    # durationMinute = int(duration) / 60.00
                    lsDataTracks = [temp_track.artist, temp_track.title, duration]
                    lsTracks.append(lsDataTracks)
                    numTracks = numTracks + 1                   
                    
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")
        # lista.clear()
               
    print("\nLISTA DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)
    print("\nNUMERO DE CANCIONES: ", lsNameTracks)

    return lsTracks, numTracks, host, port


def searchAlbum():
    lsAlbums = []
    tracksDuration = []
    # tag = TinyTag.get('D:\\musica\\ares\\167.mp3')
    # print('This track is by %s.' % tag.artist)
    # print('It is %c seconds long.' % tag.duration)

    # Con este for buscaremos en la carpeta raiz luego las subcarpetas y archivos
    # Es for hace la funcion de buscar las canciones
    for root, dirs, files, in os.walk("D:\\musica\\alejo\\Albumes"):

        for name in dirs:
            lsAlbums.append(name)
            print(name)
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac")):
                
                try:
                    temp_track = TinyTag.get(root + "\\" + name)

                    # print(temp_track.artist, "-", temp_track.title, "-", temp_track.duration)                    
                    tracksDuration.append(temp_track.duration)
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")

    return lsAlbums, tracksDuration

# --------------------------------------------EJECUCION E HILOS------------------------------------------------------

searchTrack()
searchAlbum()    

# Funciones registradas para enviar a Servidor Principal
server.register_function(searchTrack)
server.register_function(searchAlbum)

print("\nCliente escuchando...")
# Ejecutar servidor escuchando
server.serve_forever()
