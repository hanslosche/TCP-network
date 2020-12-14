import socket, threading
from tcpclient model import TcpClient

class TcpListener:
    def __init__(self, idAddr, port, packetSize, hasCommands=False):
        """
        TcpListener constructor

        initializes values

        Parameters
        ----------
        idAddr : str
            ipAddress of server to be listened on 
        port : int
            port of server to be listened on
        packetSize : int
            size of packets for communication
        hasCommands : bool
            determines whether or not to start commands thread

        Returns
        -------
        TcpServer object

        """
        self.idAddr = idAddr
        self.port = port
        self.__server = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM
        )

        self.packetSize = packetSize
        self.clients = []

        self.__running = False
        self.__binded  = False
        self.__hasCommands = hasCommands

    # don't override
    def run(self):
        """
        public run function
        binds socket and initializes all communication and command threads
        
        Parameters
        ----------
        None

        Return 
        ------
        None
        """
        # bind the socket to the ipAddr, port
        self.__server.bind((self.idAddr, self.port))
        self.__binded = True

        # initialize accept client thread
        self.__incomingConnectionThread = threading.Thread(
                target=self.__acceptThread
                )
        self.__incomingConnectionThread.setDaemon(True)
        self.__incomingConnectionThread.start()

        # initialize the commands thread if necessary
        if self.__hasCommands:
            self.__commandsThread = threading.Thread(
                target=self.cmdThread
            )
            self.__commandsThread.start()
        self.__running = True

    # don't override              
    def __acceptThread(self):
        """
        private accept thread function
        thread to accept incoming clients

        Parameters
        ----------
        None

        Return
        ------
        None
        """

        while self.__running:
            # get client object
            self.__server.listen(1)
            clientSock, clientAddr = self.__server.accept()
            
            client = self.generateClientObject(clientSock, clientAddr)
            self.clients.append(client)
            self.clientConnected(client)

            # start client thread
            clientThread = threading.Thread(
                    target = self.__clientThread,
                    args={client}
            )
            clientThread.setDaemon(True)
            clientThread.start()



    def __clientThread(self, client):
        """
        private client thread function
        initialized for each client to handle communications

        Parameters
        ----------
        client : TcpClient
            client class with information about client

        Return 
        ------
        None
        """
        msg = ""

        while True:
            try:
                while True:
                    data = client.sock.recv(self.packetSize).decode("latin1")
                    if data[-8:] == "finised":
                        # marks end of message
                        msg += data[:-8]
                        break
                    msg += data
                if not msg:
                    break
                elif msg.isspace():
                    continue
                self.msgReceived(client, msg)
                msg = ""
            except:
                # error in communications, disconnect client
                self.clientDisconnected(client)
                self.clients.remove(client)
                return
        client.sock.close()
        self.clientDisconnected(client)
        self.clients.remove(client)


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

