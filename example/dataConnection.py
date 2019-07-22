from socket import *

class DataConnection:
    def __init__(self, timeout=60):
        """Initializes a client-to-server data connection
        by serving an ephemeral socket, and waiting for
        data from the client. Optionally, a timeout can
        be provided; if no data is received within this
        time frame, the server will close the connection.
        """
        self._listen()
        

    def __init__(self, data, timeout=60):
        """Initializes a server-to-client data connection by serving
        an ephemeral socket.
        
        Arguments:
            data {list} -- A list of bytes to write to the client
        """
        self.__init__(timeout)
        self.data = data

    def _listen():
        """To be called by the class only. Sets up an ephemeral socket
        to be used for this instance of the class.
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', 0))

    def getPortNumber():
        return self.socket.getsockname()[1]

    def writeData():
        """Waits until client connects and sends all
        data to client, or times out if no connection
        was made.
        """
        # TODO: start a thread that waits for a client
        pass

    def waitData():
        pass
    