from pygame import mixer

def playMusic(song):
    
    mixer.init()
    newSong = song 
    mixer.music.load("musica\\cliente2\\descargas\\" + newSong)
    mixer.music.set_volume(0.7)
    mixer.music.play()

    while True:
        print("\n_______________________________________________________________________________________________________________________________________________________")  
        print("\n *REPRODUCTOR DE DESCARGAS*")
        print("\n  Nombre de cancion:", newSong)
        print("\n 1. Reproducir")
        print(" 2. Detener")
        print(" 3. Reiniciar")
        print(" 4. Seleccionar otra canción de descargas:")
        print(" 0. <- Atrás")

        opcion = input(">>> ")

        if opcion=="1":
            mixer.music.unpause()
        elif opcion=="2":
            mixer.music.pause()        
        elif opcion=="3":
            mixer.music.play()
        elif opcion=="4":
            mixer.music.stop()
            newSong = str(input("Escribe el nombre de otra cancion: "))
            try:
                mixer.music.load("musica\\cliente2\\descargas\\" + newSong + ".mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play() 
            except: 
                print("La canción no existe en tu carpeta de descargas.")    
        elif opcion=="0":
            mixer.music.stop()
            break
        else:
            print("Digite una opción válida!")
            
        print("\n_______________________________________________________________________________________________________________________________________________________")        