from pygame import mixer

mixer.init()
cancion=str(input("\nBuscador de canciones.\nEscribe el nombre de una cancion o album y pulsa enter: "))
mixer.music.load("musica\\cliente1\\canciones1\\Metallica - Nothing Else Matters - Live.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

while True:
    print("Pulsa p para detener la cancion")
    print("Pulsa r para reanudar la cancion")
    print("Pulsa e para elegir otra cancion")
    print("Pulsa s para salir")

    opcion = input(">>> ")

    if opcion=="p":
        mixer.music.pause()
    elif opcion=="r":
        mixer.music.unpause()        
    elif opcion=="s":
        mixer.music.stop()
    elif opcion=="e":
        mixer.music.stop()
        cancion=str(input("Selecciona una cancion: "))
        mixer.music.load("musica\\cliente1\\canciones1\\Metallica - Nothing Else Matters - Live.mp3")
    mixer.music.set_volume(0.7)
mixer.music.play()               