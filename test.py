import os


contenido = os.listdir("musica\\cliente1\\canciones1")
print(contenido)

lsfichero = []
with os.scandir("musica\\cliente1\\canciones1") as ficheros:
    for fichero in ficheros:
        print(fichero.name)
        lsfichero.append(fichero)

print (lsfichero)        