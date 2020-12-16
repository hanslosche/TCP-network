"""
Tcp Client model class

Used to store data about client for server
"""
class TcpClient:
    def __init(self, clientSock, clientAddr):

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
        
        self.sock = clientSock
        self.addr = clientAddr
    # don't override   
    def send(self, packetSize, msg, doEncode=True):

        """
        public send message function
        sends message to client socket
        
        Parameters
        ----------
        bufSize : int
            packet size to send message
        msg : str or b
            message to send
        deEncode : bool
            if message must be encoded to bytes

        Return
        ------

        None
        """
    
        # modify message
        send_b = msg.encode("utf8") if doEncode else msg # true_result if condition esle false_result
        send_b += "finised".encode("utf8")

        # break up and send inidividual packets
        size = len(send_b)
        idx = 0

        while idx < size - packetSize:
            self.sock.send(send_b[idx:idx + packetSize])
            idx += packetSize
        self.sock.send(send_b[idx:])


        # break up and sned individual packets
