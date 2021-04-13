from pygame import mixer

def playMusic(song):
    
    mixer.init()
    newSong = song 
    print("\nBuscador de canciones")
    mixer.music.load("musica\\cliente1\\descargas\\Metallica - Nothing Else Matters - Live.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play()

    while True:
        print("2. Reproducir")
        print("3. Detener")
        print("4. Seleccionar otra cancion")
        print("5. Salir")

        opcion = input(">>> ")

        if opcion=="2":
            mixer.music.unpause()
        elif opcion=="3":
            mixer.music.pause()        
        elif opcion=="4":
            mixer.music.stop()
            newSong=str(input("Selecciona una cancion: "))
            mixer.music.load("musica\\cliente1\\canciones1\\Metallica - Nothing Else Matters - Live.mp3")
        elif opcion=="5":
            mixer.music.stop()
        mixer.music.set_volume(0.7)
    mixer.music.play()               