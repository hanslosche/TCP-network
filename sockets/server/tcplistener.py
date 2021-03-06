import socket, threading
from .tcpclientmodel import TcpClient

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
        self.serverStarted()

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
                    # get message
                    data = client.sock.recv(self.packetSize).decode("latin1")
                    if data[-8:] == "finished":
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
        """
        command thread
        if hasCommands, server starts this thread to accept commands as input

        Parameters
        ----------
        None
        Return
        ------
        None
        """
        pass

    # dont override
    def getTcpClient(self, sock):
        '''
        function to retrieve client object
        compares socket to each socket in list of clients

        Parameters
        ----------
        sock : socket
            desired socket object
        Return 
        ------
        client object with matching socket, None if no match
        '''

        for client in self.clients:
            if client.sock == sock:
                return client
        return None

    def send(self, client, msg, doEncode=True):
        """
        public send message function
        calls send function for client parameter

        Parameters
        ----------
        client : TCP-client
            recipient client
        msg : str or b
            message to send
        doEncode : bool
            specity whether or not to encode message into bytes

        Return
        ------
        None
        """
        client.send(self.packetSize, msg, doEncode)

    # recommended to override
    def generateClientObject(self, clientSock, clientAddr):
        """
        function to generate client object
        should be overriden to generate object of tpye that inherits from tcp-client

        Parameters
        ----------
        clientsock : socket
            socket of client
        clientAddr : address
            address of client

        Return
        ------
        client object inherited from tcpclient with clientsock, clientAddr
        """
        return TcpClient(clientSock, clientAddr)

    # override this
    def serverStarted(self):
        """
        server started event callback
        when server is fully started, the program calls this function

        Parameters
        ----------
        None
        Return
        ------
        None
        """
        pass

    # override this
    def clientConnected(self, client):
        pass
    # override this
    def clientDisconnected(self, client):
        """
        client disconnected event callbacl
        when a client disconnects, the program calls this function

        Parameters
        ----------
        client : TcpClient
            client that disconnected

        Return 
        ------
        None
        """
        pass 
    # override this
    def msgReceived(self, client, msg):
        """
        message received event callback
        when server receives message, then program calls this function

        Parameters
        ----------
        client : TcpClient
            sending client
        msg : str
            sent message

        Return 
        ------
        None
        """
        pass

