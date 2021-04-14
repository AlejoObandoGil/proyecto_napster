from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xmlrpc.client
import os
from musicPlayer2 import playMusic

def menu(client):
    # Primer menu es el menu principal 

    while True:
        global download
        download = 0
        print("\n_______________________________________________________________________________________________________________________________________________________")      
        print("\nMENU PRINCIPAL DE NAPSTER")
        print(" 1. Buscar por canción")
        print(" 2. Buscar por artista")
        print(" 3. Buscar por álbum") 
        print(" 0. Salir") 
        opcion = input("Opcion >>> ")

        if opcion == "1":            
            song = input("Escribe el nombre de una canción: ")
            # Instancia de la funcion buscar del servidor y guardamos datos de la cancion y usuario en cliente
            lsNewSong, lsNewDir, message = client.searchTrack(song)
            print("\n", message)

            if message  != "Cancion encontrada!":
                pass
                
            else:     
                print("\n_______________________________________________________________________________________________________________________________________________________")            
                # Segundo menu de descarga
                while True:
                    userServer = ""
                    hostServer = ""
                    portServer = 0
                    print("\nMENU DE DESCARGA NAPSTER")
                    print("\nLista de canciones encontradas.")
                    for Track in lsNewSong:
                        print ("\n- Nombre cancion:", Track[0],"- Titulo:", Track[1], "- Artista:", Track[2],  "- Duracion:", Track[3], "- Tamaño:", Track[4], "Bytes - Usuario:", Track[5])
                    for direction in lsNewDir:
                        userServer = direction[0]
                        hostServer = direction[1]
                        portServer = direction[2]
                        
                        print ("\nhost usuario:", direction[1], "port usuario:", direction[2])

                    print("\n 1. Descargar canción")
                    print(" 2. Reproducir canción")
                    print(" 0. Volver a Menu principal")
                    opcion2 = input("Opción >>> ")

                    if opcion2 == "1":
                        try:
                            # Establecemos una nueva conexion tipo cliente con el cliente que posee la cancion 
                            clienteCliente = xmlrpc.client.ServerProxy('http://' + hostServer + ':' + str(portServer), allow_none=True)
                            print("\nConexión establecida con el usuario " + userServer)
                        except: 
                            print("\nError. Usuario desconectado")

                        print("\nDescargando canción... Por favor espere...")
                        try:
                            # Llamamos la funcion que busca el archivo en la carpeta del cliente de donde se descargara
                            file_data = clienteCliente.shareSong(song)
                            # Guardamos la cancion en el directorio
                            dirDownload = "musica\\cliente2\\descargas\\" + song + ".mp3"                       
                            file = open(dirDownload, "wb")
                            file.write(file_data.data)
                            print("\nCanción descargada con éxito!\nLa ubicación del archivo es: ", dirDownload)
                            download = 1
                            # Cerramos el archivo
                            file.close()
                        except:
                            print("\nError al descargar canción. Presiona 1 para volver a intentarlo.")
                            download = 0                      
                        
                    elif opcion2 == "2":
                        # llamamos la funcion reproductor de musica
                        if download == 1:
                            playMusic(song)
                        else:
                            print("\nLa canción # ", song, " # no esta descargada.\n" )    
                        
                    elif opcion2 == "0":
                        break

                    else:
                        print("Digite una opción válida!")

                    print("\n_______________________________________________________________________________________________________________________________________________________")      

        elif opcion == "2":
            song = input("Escribe el nombre de un artista: ")
                    
        elif opcion == "3":
            song = input("Escribe el nombre de un álbum: ")

        elif opcion == "0":
            print("\nCerrando cliente NAPSTER...")   
            break
        else:
            print("Digite una opción válida!")
    return 0