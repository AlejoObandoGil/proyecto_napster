# client.py
import sys
import xmlrpc.client

proxy = xmlrpc.client.Server('http://localhost:9000')
with open("musica/cliente1/canciones1/acdc - back in black.mp3", "rb") as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
proxy.server_receive_file(binary_data)
# handle.close()

print("Client on")


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

    json_lsTracks = json.dumps(lsTracks)
    json_numAlbum = json.dumps(numAlbum)
    json_lsAlbums = json.dumps(lsAlbums)
    json_numTrack = json.dumps(numTrack)  

    lsTrackeños = json.loads(json_lsTracks)
    print("py:", lsTracks)    
    print("json:", json_lsTracks) 
    print("py:", lsTrackeños)
    print(type("json:", json_lsTracks)) 
    print(type("py:", lsTrackeños))

    return json_lsAlbums, json_numAlbum, json_lsTracks, json_numTrack

sendAlbum("username")  




# data = open("musica\\cliente2\\canciones2\\damian marley - welcome to jam rock.mp3", "rb")
# dataFile = data.read()
# print(dataFile)
# song = "kukis"
# file = open("musica\\cliente1\\descargas\\" + song + ".mp3", "wb")
# file.write(dataFile)
# print(file)
# file.close()
# print("HEcho")