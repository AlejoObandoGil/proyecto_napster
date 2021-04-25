import threading
from client1 import ClientThread, ClientThread2, ClientServerThread

if __name__=="__main__":
    
    clientSend = ClientThread()
    clientSend.start()
    clientSend2 = ClientThread2()
    clientSend2.start()
    clientServer = ClientServerThread()
    clientServer.start()         