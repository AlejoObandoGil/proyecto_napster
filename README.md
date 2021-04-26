# proyecto_napster

Proyecto Napster: Este proyecto es un simulador de el programa P2P de descargas de musica NAPSTER.
Desarrollado con el lenguaje de Programacion Python, bajo una arquitectura CLiente/Servidor P2P, envia informacion con JSON a traves de RPC 
e implementa hilos en servidor y cliente.
Los clientes se conectan y envia sus archivos de musica a el Servidor Principal y se crea una copia en un servidor Secundario(Servidor Espejo), 
luego cada cliente busca musica en el servidor, y se conecta con el cliente que tiene la cancion buscada para luego descargarla.
