#!/usr/bin/env python3
from socket import *
import sys
import threading

START = 0x2A # 0b101010 = 42

def parseMessage(buffer):
    # Command format:
    #  0     n-bytes      n+1 
    # SoM   Data Length  EoM
    # 0x42  ...........  0x43

    print(buffer)

def clientHandler(clientSocket, clientAddress):
    print(f"Client connected from {clientAddress}")

    commandBuffer = []
    while 1:
        newByte = clientSocket.recv(1)
        commandBuffer.append(newByte)
        if newByte == b"\x42":
            # Got start of message, reset the buffer
            commandBuffer = [newByte]
        elif newByte == b"\x43":
            # Got end of message, parse it
            parseMessage(commandBuffer)
            commandBuffer = []


def main():
    if len(sys.argv) <= 1:
        print(f"{sys.argv[0]} [portNum]")
        return

    serverPort = int(sys.argv[1])
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)

    print(f"Server started on port {serverPort}") 

    while 1:
        (clientSocket, addr) = serverSocket.accept()
        threading.Thread(target=clientHandler, args=(clientSocket, addr)).start()

if __name__ == '__main__':
    main()
