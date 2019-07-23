#!/usr/bin/env python3
from socket import *
from helpers import sendCommand
import sys
import threading
import os

START = 0x01
END = 0x00


def connectEpheremal(dataPort):
   
   dataSocket = socket(AF_INET, SOCK_STREAM)
   dataSocket.connect(('', dataPort))
   conn = True
   while conn:
           conn = serverHandler(dataSocket, dataPort)

   return

def cmdList(clientSocket):
    clientSocket.send(b'\x01\x05\x00')
    return

def parseMessage(buffer):
    # Command format:
    #  0     n-bytes      n+1 
    # SoM   Data Length  EoM
    # 0x01 ...........  0x00

    print(buffer)
    if buffer[1] == b'\x02':
        #once port is open acknowledge connection?
        print("Data port opened")
        return

def serverHandler(serverSocket, serverAddress):
    print(f"Client connected from {serverAddress}")
    
    buffer = []
    while 1:
            newByte = serverSocket.recv(1)
            buffer.append(newByte)
            if newByte == b"\x01":
                # Got start of message, reset the buffer
                print("Byte came in")
                buffer = [newByte]
            elif newByte == b"\x00":
                # Got end of message, parse it
                parseMessage(buffer)
                buffer = []
                return False

def getPortNumber(data):
    """
    Given a 0x05 packet in the data argument
    returns an integer with the port number
    encoded via the 2 data bytes in the packet
    """
    return int.from_bytes(data[2:4], byteorder="big")

def main():
    clientHost = sys.argv[1]
    clientPort = int(sys.argv[2])

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((clientHost, clientPort))
    print(f"made connection to {clientHost}:{clientPort}")
    
    while 1:
            #threading.Thread(target=serverHandler, args=(clientSocket, clientPort)).start()
            argument = input("Please input a command >> ").split()
            if argument[0] == "ls":
                cmdList(clientSocket)
                serverHandler(clientSocket, clientPort)
            elif argument[0] == "put":
                # Puts a file to the server
                fileName = argument[1]

                # Check that the file exists
                if not os.path.exists(fileName):
                    print(f"{fileName} does not exist. File must be in same directory as {__file__}")
                    continue

                # Send `put` command to server with fileName
                sendCommand(clientSocket, 4, fileName)

                # Get response from server
                ephPortNumber = getPortNumber(clientSocket.recv(5))

                print(f"Attempting to connect to socket at {clientHost}:{ephPortNumber}")

                # Connect to ephemeral socket
                ephSocket = socket(AF_INET, SOCK_STREAM)
                ephSocket.connect((clientHost, ephPortNumber))

                print(f"Connected, transferring {fileName}")

                # Transfer file
                with open(fileName, 'rb') as f:
                    ephSocket.sendall(f.read())

                # Close connection
                ephSocket.close()

                print("Done!")
                

        
    
            

if __name__ == '__main__':
    main()