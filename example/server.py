#!/usr/bin/env python3
from socket import *
from subprocess import PIPE
import subprocess
import sys
import threading

START = 0x01 # 0b000001


# we need to create the port to send to the client
# create a new socket on the server
# send that socket to the client
# have client establish connection
# then send over data
def epheremal():
    epheremalSocket = socket(AF_INET, SOCK_STREAM)
    epheremalSocket.bind(('', 0))
    return epheremalSocket.getsockname()[1]

# Commands
# get the epheremal port then sends it over to the client.
def cmdList(clientSocket):
    # universal_newlines=PIPE -- for newlines on output
    port = epheremal()
    print("epheremal port: ", port)
    message = f'\x01\x02{port}\x00'
    print("message, ", str.encode(message))
    clientSocket.send(str.encode(message))
    # result = subprocess.run(['ls', '-l'], stdout=PIPE, stderr=PIPE)
    # print(result.stdout)


def parseMessage(buffer, clientSocket):
    # Command format:
    #  0     n-bytes      n+1 
    # SoM   Data Length  EoM
    # 0x01 ...........  0x00

    print(buffer)
    if buffer[1] == b'\x04':
        print("before cmd list")
        cmdList(clientSocket)

def clientHandler(clientSocket, clientAddress):
    print(f"Client connected from {clientAddress}")

    commandBuffer = []
    while 1:
        newByte = clientSocket.recv(1)
        commandBuffer.append(newByte)
        if newByte == b"\x01":
            # Got start of message, reset the buffer
            print("Byte came in")
            commandBuffer = [newByte]
        elif newByte == b"\x00":
            # Got end of message, parse it
            parseMessage(commandBuffer, clientSocket)
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
