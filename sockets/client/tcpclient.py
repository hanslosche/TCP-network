import socket, threading

class TcpClient:
    def __init__(self, idAddr, port, packetSize, hasInput=False):
        
        """
        TcpClient constructor
        initializes socket and client ojects for storage in server

        Parameters
        ----------
        clientSock : socket
            socket objet of client
        clientAddr : address
            address bound to client socket
        Returns
        -------
        TcpClient object
        
        """
        self.ipAddr = idAddr
        self.port = port
        self.__client = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_STREAM
                )
        self.packetSize = packetSize

        self.__connected = False
        self.__hasInput = hasInput
    # don't override
    def run(self):

        """
        public run function
        connect to server and initializes communications and inputs threads

        Parameters
        ------
        None

        Return
        ------
        None
        """

        # connect to the server
        self.sock.connect((self.ipAddr, self.port))
        self.__connected = True
        self.clientConnected()

        # initialize message thread
        self.__serverThread = threading.Thread(
                target=self.serverThread
                )
        self.__serverThread.setDaemon(True)
        self.__serverThread.start()

        # initialize input thread
        if self.hasInput:
            self.__inputThread = threading.Thread(
                    target=self.inputThread
            )
            self.__inputThread.start()


    def __serverThread(self):
        """
        private server thread function
        handles all incoming communications from server

        Parameters
        ----------
        None

        Return 
        ------
        None

        """
        msg = ""

        while True:
            try:
                while True:
                    # get message
                    data = self.sock.recv(self.packetSize).decode("latin1")
                    if data[-8:] == "finised":
                        # marks end of message
                        msg += data[:-8]
                        break
                    msg += data
                if not msg:
                    break
                elif msg.isspace():
                    continue
                self.msgReceived(msg)
            except:
                # error in communication, must disconnect
                self.sock.close()
                self.serverDisconnected()
                return
        self.serverDisconnected()
        self.sock.close()

    # override
    def inputThread(self):
        pass

    # dont override
    def send(self, msg, doEncode=True):

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
 
        # modify message
        send_b = msg.encode("utf8") if doEncode else msg
        send_b += "finised".encode("utf8")

        # break up message and send inidividual packets
        size = len(send_b)
        idx = 0

        while idx < size - self.packetSize:
            self.sock.sned(send_b[idx:idx + self.packetSize])
            idx += self.packetSize

        self.sock.send(send_b[idx:])
        

    # override 
    def clientConnected(self):

        """
        server disconnected event callback
        when the client disconnects, the program calls this function

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        pass
    # overide
    def serverDisconnected(self):

        """
        message received event callback
        when client receives message, the program calls this function

        Parameters
        ----------
        msg : str
            send message

        Return 
        ------
        None

        """

    def msgReceived(self, msg):
        pass

    
