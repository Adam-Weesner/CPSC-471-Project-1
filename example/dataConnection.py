from socket import *
from helpers import sendCommand

class DataConnection:
    def __init__(self, clientSocket, data=None, timeout=60):
        self.clientSocket = clientSocket
        self.timeout = timeout
        self.data = data

        self._listen()

    def _listen(self):
        """To be called by the class only. Sets up an ephemeral socket
        to be used for this instance of the class.
        """
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(('', 0))
        self.socket.listen(1)

    def getPortNumber(self):
        return self.socket.getsockname()[1]

    def writeData(self):
        """Waits until client connects and sends all
        data to client, or times out if no connection
        was made.
        """
        # TODO: start a thread that waits for a client
        pass

    def waitData(self):
        print(f"Waiting for client on {self.getPortNumber()}")
        sendCommand(self.clientSocket, 2, self.getPortNumber().to_bytes(2, byteorder="big"))
        (clientSocket, addr) = self.socket.accept()
        self.clientSocket = clientSocket
            
    