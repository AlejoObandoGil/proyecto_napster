import os
import sys
import json
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from musicPlayer2 import playMusic

# Servidor2
host2 = "127.0.0.1"
port2 = 9899

def downloadMenu(client, username, op, song):

    option = int(op)
    global download
    download = 0

    json_song = json.dumps(song)
    json_option = json.dumps(option)

    try:
        # Instancia de la funcion buscar del servidor y guardamos datos de la cancion y usuario en cliente   
        json_lsNewSong, json_lsNewDir, json_message = client.searchTrack(json_song, json_option)
    except:
        # Crear conexion para un Servidor RPC, con el metodo client de xmlrpc 
        client = xmlrpc.client.ServerProxy('http://' + host2 + ':' + str(port2), allow_none=True)
        print("\nEl servidor principal no responde...Cliente conectando a servidor Secundario...")   
        # Instancia de la funcion buscar del servidor y guardamos datos de la cancion y usuario en cliente   
        json_lsNewSong, json_lsNewDir, json_message = client.searchTrack(json_song, json_option) 

    lsNewSong = json.loads(json_lsNewSong)
    lsNewDir = json.loads(json_lsNewDir)
    message = json.loads(json_message)

    print("\n", message)

    if message == "Cancion encontrada!" or message == "Artista encontrado!" or message == "Album encontrado!":
        print("\n_______________________________________________________________________________________________________________________________________________________")            
        # Segundo menu de descarga
        while True:
            userServer = ""
            hostServer = ""
            portServer = 0
            print("\nMENU DE DESCARGA NAPSTER  *** ", username, " ***")
            print("\nLista de canciones encontradas.")
            for Track in lsNewSong:
                print("\n- Nombre cancion:", Track[0],"- Titulo:", Track[1], "- Artista:", Track[2], "- Álbum:", Track[3])
                print("- Duracion: ", Track[4], "- Tamaño:", Track[5], "Bytes - Usuario:", Track[6])
            for direction in lsNewDir:
                userServer = direction[0]
                hostServer = direction[1]
                portServer = direction[2]
                print ("\nhost usuario:", direction[1], "port usuario:", direction[2])

            print("\n 1. Descargar canción")
            print(" 2. Reproducir canción")
            print(" 0. Volver a Menu principal")
            option2 = input("Opción >>> ")

            if option2 == "1":
                if userServer == username:
                    print("Estas intentando descargar una canción que ya tienes.")
                else:    
                    try:
                        # Establecemos una nueva conexion tipo cliente con el cliente que posee la cancion 
                        clienteCliente = xmlrpc.client.ServerProxy('http://' + hostServer + ':' + str(portServer), allow_none=True)
                        print("\nConexión establecida con el usuario " + userServer)
                    except: 
                        print("\nError. Usuario desconectado")

                    print("\nDescargando canción... Por favor espere...")
                    try:
                        if option == 1 or option == 2:
                            # Llamamos la funcion que busca el archivo en la carpeta del cliente de donde se descargara
                            global name_file
                            file_data, name_file = clienteCliente.shareSong(json_song, json_option)
                            # file_data = json.loads(json_file_data)
                            # Guardamos la cancion en el directorio
                            dirDownload = "musica\\cliente2\\descargas\\" + name_file                      
                            file = open(dirDownload, "wb")
                            file.write(file_data.data)
                            print("\nCanción descargada con éxito!\nLa ubicación del archivo es: ", dirDownload)
                            download = 1
                            # Cerramos el archivo 
                            file.close()
                        elif option == 3:
                            # Llamamos la funcion que busca el archivo en la carpeta del cliente de donde se descargara
                            ls_file_data = clienteCliente.shareAlbum(json_lsNewSong, json_option)
                            for file_data in ls_file_data:
                                # Guardamos la cancion en el directorio
                                dirDownload = "musica\\cliente2\\descargas\\" + file_data[0]
                                global name_file_album  
                                name_file_album = file_data[0]              
                                file = open(dirDownload, "wb")
                                file.write(file_data[3].data)
                                print("\nCanción descargada con éxito!\nLa ubicación del archivo es: ", dirDownload)
                                download = 1
                                # Cerramos el archivo 
                                file.close()
                    except:
                        print("\nError al descargar canción. Presiona 1 para volver a intentarlo.")
                        download = 0                                                
                
            elif option2 == "2":
                # llamamos la funcion reproductor de musica
                if download == 1 and option == 3:
                    playMusic(name_file_album)
                if download == 1: 
                    if (option == 1 or option == 2):
                        playMusic(name_file)                    
                else:
                    print("\nLa canción # ", song, " # no esta descargada.\n" )      
                
            elif option2 == "0":
                break

            else:
                print("Digite una opción válida!")

            print("\n_______________________________________________________________________________________________________________________________________________________")             
    else: 
        pass   
        

def menu(client, username):
    # Primer menu: es el menu principal 
    closeMenu = False
    while True:
        print("\n_______________________________________________________________________________________________________________________________________________________")      
        print("\nMENU PRINCIPAL DE NAPSTER  *** ", username, " ***")
        print(" 1. Buscar por canción")
        print(" 2. Buscar por artista")
        print(" 3. Buscar por álbum") 
        print(" 0. Salir") 
        option = input("Opcion >>> ")

        if option == "1":   

            song = input("Escribe el nombre de una canción: ")           
            downloadMenu(client, username, option, song)
            
        elif option == "2":

            artist = input("Escribe el nombre de un artista: ")
            downloadMenu(client, username, option, artist)
                    
        elif option == "3":

            album = input("Escribe el nombre de un álbum: ")
            downloadMenu(client, username, option, album)

        elif option == "0":

            option3 = input("Seguro desea salir de NAPSTER?\n 1. Si / 2. No : ")
            if option3 == "1":
                print("\nCerrando cliente NAPSTER...")
                closeMenu = True
                return closeMenu               
                break  
            elif option3 == "2": 
                pass
            else:
                print("Digite una opción válida!")

        else:
            print("Digite una opción válida!")

    return 0