# ---------------------FUNCIONES BUSCAR MUSICA EN CARPETA LOCAL CLIENTE---------------------------------------
import os
from tinytag import TinyTag, TinyTagException
import datetime
# Esta funcion busca canciones invididuales o sin album
def sendTrack():

    lsNameTracks = []
    lsDataTracks = []
    lsTracks = []
    numTracks = 0
    data = ""   
    # Este for lee el directorio raiz, sus subcarpetas y archivos. El metodo walk sirve para leer un directorio    
    for root, dirs, files, in os.walk("musica\\cliente1\\canciones1"):

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
                    
                    # Creamos una lista con los metadatos de cada cancion y agregamos estas listas a otra lista para tener una matriz de canciones
                    lsDataTracks = [temp_track.artist, temp_track.title, duration, temp_track.filesize]
                    lsTracks.append(lsDataTracks)
                    numTracks += 1                   
                    
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")
        # lista.clear()              
    print("\nLISTA DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)
    print("\nLISTA DE NOMBRES DE CANCIONES: ", lsNameTracks)

    return lsTracks, numTracks  

# Esta funcion busca albumes. Los albumes estan en una carpeta diferente de las canciones individuales.
def sendAlbum():

    lsAlbums = []
    lsDataTracks = []
    lsTracks = []
    lsAT = []
    numAlbums = 0
    numTracks = 0   
    # tag = TinyTag.get('D:\\musica\\ares\\167.mp3')
    # print('This track is by %s.' % tag.artist)
    # print('It is %c seconds long.' % tag.duration)

    # Con este for buscaremos en la carpeta raiz luego las subcarpetas y archivos
    # Es for hace la funcion de buscar las canciones
    for root, dirs, files, in os.walk("musica\\cliente1\\Albums1"):

        for named in dirs:
            lsAlbums.append(named)
            numAlbums += 1
            for root, dirs, files, in os.walk("musica\\cliente1\\Albums1\\" + named):
                for namet in files:                              
                    if namet.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):               
                        try:
                            temp_track = TinyTag.get(root + "\\" + namet)

                            d = str(temp_track.duration)
                            durationMinute = round(float(d), 2)
                            duration = str(datetime.timedelta(seconds=durationMinute))
                            
                            lsDataTracks = [named, temp_track.artist, temp_track.title, duration, temp_track.filesize]
                            lsTracks.append(lsDataTracks)
                            numTracks += 1
                            
                        except TinyTagException:
                            print("Error. No se puede leer el archivo.")               

    print("\nLISTA DE ALBUMS: ", lsAlbums)
    print("\nNUMERO DE ALBUMS: ", numAlbums) 
    print("\nLISTA DE CANCIONES: ", lsTracks) 
    print("\nNUMERO DE CANCIONES: ", numTracks)                 

    return lsAlbums, numAlbums, numTracks