# ---------------------FUNCIONES BUSCAR MUSICA EN CARPETA LOCAL CLIENTE---------------------------------------
import os
import xmlrpc.client
import datetime
from tinytag import TinyTag, TinyTagException

# Esta funcion busca canciones invididuales o sin album en la carpeta local del cliente
def sendTrack(username):

    lsNameTracks = []
    lsDataTracks = []
    lsTracks = []
    lsFileTracks = []
    numTracks = 0
    data = ""   
    # Este for lee el directorio raiz, sus subcarpetas y archivos. El metodo walk sirve para leer un directorio    
    for root, dirs, files, in os.walk("musica\\cliente2\\canciones2"):

        for name in files:
            # Si extension del archivo es tipo musica agregamos a lista
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):
                lsNameTracks.append(name)
                try:
                    # Creamos un objeto tinyTag por cada cancion y obtenemos sus metadatos y los guardamos en una lista
                    temp_track = TinyTag.get(root + "\\" + name)

                    d = str(temp_track.duration)
                    durationMinute = round(float(d), 2)
                    duration = str(datetime.timedelta(seconds=durationMinute))
                    file = open("musica\\cliente2\\canciones2\\" + name, "rb")
                    file_data = file.read(1024)
                    lsFileTracks.append(file_data)
                    if file:
                        print("Archivo leido: ", file)
                    file.close()
                    
                    # Creamos una lista con los metadatos de cada cancion y agregamos estas listas a otra lista para tener una matriz de canciones
                    lsDataTracks = [temp_track.title, temp_track.artist, duration, temp_track.filesize, username]
                    lsTracks.append(lsDataTracks)
                    numTracks += 1                   
                    
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")
        # lista.clear()
        # data = open("doc\\proy.txt", "rb")
        # data = data.read(1024)

        # file = open("doc\\proy.txt", "wb")
        # file.write(data)
        # file.close()
        # print("HEcho")
    
    print("\nLISTA DE CANCIONES: ", lsFileTracks)            
    print("\nLISTA DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)
    print("\nLISTA DE NOMBRES DE CANCIONES: ", lsNameTracks)

    return lsTracks, numTracks, lsFileTracks  


# Esta funcion busca albumes en la carptea lcoal del cliente. Los albumes estan en una carpeta diferente de las canciones individuales.
def sendAlbum(username):

    lsAlbums = []
    lsDataTracks = []
    lsTracks = []
    lsAT = []
    numAlbums = 0
    numTracks = 0   

    # Con este for buscaremos en la carpeta raiz luego las subcarpetas y archivos
    # Es for hace la funcion de buscar las canciones
    for root, dirs, files, in os.walk("musica\\cliente2\\Albums2"):

        for dirName in dirs:
            lsAlbums.append(dirName)
            numAlbums += 1
            for root, dirs, files, in os.walk("musica\\cliente2\\Albums2\\" + dirName):
                for trackName in files:                              
                    if trackName.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):               
                        try:
                            temp_track = TinyTag.get(root + "\\" + trackName)

                            d = str(temp_track.duration)
                            durationMinute = round(float(d), 2)
                            duration = str(datetime.timedelta(seconds=durationMinute))
                            
                            lsDataTracks = [temp_track.title, temp_track.artist, dirName, duration, temp_track.filesize, username]
                            lsTracks.append(lsDataTracks)
                            numTracks += 1
                            
                        except TinyTagException:
                            print("Error. No se puede leer el archivo.")               

    print("\nLISTA DE ALBUMS: ", lsAlbums)
    print("\nNUMERO DE ALBUMS: ", numAlbums) 
    print("\nLISTA DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)                 

    return lsAlbums, numAlbums, lsTracks, numTracks