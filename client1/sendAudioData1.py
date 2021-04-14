# ---------------------BUSCAR Y ENVIAR METADATOS MUSICA EN CARPETA LOCAL CLIENTE---------------------------------------
import os
import datetime
from tinytag import TinyTag, TinyTagException

# Esta funcion busca canciones invididuales o sin album en la carpeta local del cliente
def sendTrack(username):

    lsDataTracks = []
    lsTracks = []
    numTrack = 0
  
    # Este for lee el directorio raiz, sus subcarpetas y archivos. El metodo walk sirve para leer un directorio    
    for root, dirs, files, in os.walk("musica\\cliente1\\canciones1"):

        for name in files:
            # Si extension del archivo es tipo musica agregamos a lista
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):
                
                try:
                    # Creamos un objeto tinyTag por cada cancion y obtenemos sus metadatos y los guardamos en una lista
                    temp_track = TinyTag.get(root + "\\" + name)

                    d = str(temp_track.duration)
                    durationMinute = round(float(d), 2)
                    duration = str(datetime.timedelta(seconds=durationMinute))
                    
                    # Creamos una lista con los metadatos de cada cancion y agregamos estas listas a otra lista para tener una matriz de canciones
                    lsDataTracks = [name, temp_track.title, temp_track.artist, duration, temp_track.filesize, username]
                    lsTracks.append(lsDataTracks)
                    numTrack += 1                   
                    
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")
        # lista.clear()
        # data = open("doc\\proy.txt", "rb")
        # data = data.read(1024)

        # file = open("doc\\proy.txt", "wb")
        # file.write(data)
        # file.close()
        # print("HEcho")
                
    # print("\nLISTA DE CANCIONES: ", lsTracks) 
    # print("\nNUMERO DE CANCIONES: ", numTracks)
    # print("\nLISTA DE NOMBRES DE CANCIONES: ", lsNameTracks)

    return lsTracks, numTrack  


# Esta funcion busca albumes en la carptea lcoal del cliente. Los albumes estan en una carpeta diferente de las canciones individuales.
def sendAlbum(username):

    lsAlbums = []
    lsDataTracks = []
    lsTracks = []
    numAlbum = 0
    numTrack = 0   

    # Con este for buscaremos en la carpeta raiz luego las subcarpetas y archivos
    # Es for hace la funcion de buscar las canciones
    for root, dirs, files, in os.walk("musica\\cliente1\\Albums1"):

        for dirName in dirs:
            lsAlbums.append(dirName)
            numAlbum += 1
            for root, dirs, files, in os.walk("musica\\cliente1\\Albums1\\" + dirName):
                for trackName in files:                              
                    if trackName.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):               
                        try:
                            temp_track = TinyTag.get(root + "\\" + trackName)

                            d = str(temp_track.duration)
                            durationMinute = round(float(d), 2)
                            duration = str(datetime.timedelta(seconds=durationMinute))
                            
                            lsDataTracks = [trackName, temp_track.title, temp_track.artist, duration, temp_track.filesize, username, dirName]
                            lsTracks.append(lsDataTracks)
                            numTrack += 1
                            
                        except TinyTagException:
                            print("Error. No se puede leer el archivo.")                               

    return lsAlbums, numAlbum, lsTracks, numTrack

# ---------------------BUSCAR Y ENVIAR ARCHIVOS DE MUSICA EN CARPETA LOCAL CLIENTE---------------------------------------

# Esta funcion busca canciones invididuales o sin album en la carpeta local del cliente
def sendTrackClient():

    lsDataTracks = []
    lsTracks = []
  
    # Este for lee el directorio raiz, sus subcarpetas y archivos. El metodo walk sirve para leer un directorio    
    for root, dirs, files, in os.walk("musica\\cliente1\\canciones1"):

        for name in files:
            # Si extension del archivo es tipo musica agregamos a lista
            if name.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):

                try:
                    # Creamos un objeto tinyTag por cada cancion y obtenemos sus metadatos y los guardamos en una lista
                    temp_track = TinyTag.get(root + "\\" + name)
                    try:
                        file = open("musica\\cliente1\\canciones1\\" + name, "rb")
                        file_data = file.read()
                        file.close()
                        #print(file_data)
                    except:
                        print("Error al leer archivo.")
                    # Creamos una lista con los metadatos de cada cancion y agregamos estas listas a otra lista para tener una matriz de canciones
                    lsDataTracks = [name, temp_track.title, temp_track.artist, file_data]
                    lsTracks.append(lsDataTracks)                   
                    
                except TinyTagException:
                    print("Error. No se puede leer el archivo.")
                
    # print("\nLISTA DE CANCIONES: ", lsTracks) 

    return lsTracks

# sendTrackClient()

# Esta funcion busca albumes en la carptea lcoal del cliente. Los albumes estan en una carpeta diferente de las canciones individuales.
def sendAlbumClient():

    lsAlbums = []
    lsDataTracks = []
    lsTracks = []
    # Con este for buscaremos en la carpeta raiz luego las subcarpetas y archivos
    # Es for hace la funcion de buscar las canciones
    for root, dirs, files, in os.walk("musica\\cliente1\\Albums1"):

        for dirName in dirs:
            lsAlbums.append(dirName)
            for root, dirs, files, in os.walk("musica\\cliente1\\Albums1\\" + dirName):
                for trackName in files:                              
                    if trackName.endswith((".mp3", ".mp4a", ".flac", ".alac", ".wav", ".wma", ".ogg")):               
                        try:
                            temp_track = TinyTag.get(root + "\\" + trackName)
                            try:
                                file = open("musica\\cliente1\\Albums1\\" + dirName + "\\" + trackName, "rb")
                                file_data = file.read()
                                file.close()
                            except:
                                print("Error al leer el archivo.")
                            lsDataTracks = [trackName, temp_track.title, temp_track.artist, file_data, dirName]
                            lsTracks.append(lsDataTracks)
                            
                        except TinyTagException:
                            print("Error. No se puede leer el archivo.")                        

    return lsTracks, lsAlbums



# data = open("musica\\cliente2\\canciones2\\damian marley - welcome to jam rock.mp3", "rb")
# dataFile = data.read()
# print(dataFile)
# song = "kukis"
# file = open("musica\\cliente1\\descargas\\" + song + ".mp3", "wb")
# file.write(dataFile)
# print(file)
# file.close()
# print("HEcho")