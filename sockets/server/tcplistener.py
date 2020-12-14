import socket, threading
from tcpclient model import TcpClient

class TcpListener:
    def __init__(self, idAddr, port, packetSize, hasCommands=False):
        pass

    def run(self):
        pass

    def __acceptThread(self):
        pass

    def __clientThread(self, client):
        pass

    def cmdThread(self):
        pass

    def getTcpClient(self, sock):
        pass

    def send(self, client, msg, doEncode=True):
        pass

    def generateClientObject(self, clientSock, clientAddr):
        pass

    def serverStarted(self):
        pass

    def clientConnected(self, client):
        pass

    def clientDisconnected(self, client):
        pass

    def msgReceived(self, client, msg):
        pass

