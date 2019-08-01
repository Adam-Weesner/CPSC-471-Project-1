#!/usr/bin/env python3
from socket import *
from helpers import sendCommand, messageReader
import sys
import threading
import os

START = 0x01
END = 0x00

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
                # Send `ls` command to server
                sendCommand(clientSocket, 5)

                # Get response from the server
                ephPortNumber = getPortNumber(clientSocket.recv(5))

                print(f"Attempting to connect to socket at {clientHost}:{ephPortNumber}")

                # Connecting to ephemeral port
                ephSocket = socket(AF_INET, SOCK_STREAM)
                ephSocket.connect((clientHost, ephPortNumber))

                # Printing out `ls` content
                messageReader(ephSocket)

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

                print(f"Done! Transferred {os.path.getsize(fileName)} bytes.")

            if argument[0] == "get":
                if len(argument) != 2:
                    print(f"ERROR - Please write commands in the format of: 'get <fileName>'")
                else:
                    # Puts a file to the server
                    fileName = argument[1]

                    # Send `get` command and filename to server
                    sendCommand(clientSocket, 3, fileName)

                    # Get response from the server
                    ephPortNumber = getPortNumber(clientSocket.recv(5))

                    print(f"Attempting to connect to socket at {clientHost}:{ephPortNumber}")

                    # Connect to ephemeral socket
                    ephSocket = socket(AF_INET, SOCK_STREAM)
                    ephSocket.connect((clientHost, ephPortNumber))

                    print(f"Connected, transferring {fileName}")

                    # Transfer file
                    fileSize = 0
                    with open(fileName, 'wb') as f:
                        while True:
                            dataIn = ephSocket.recv(1)
                            if dataIn:
                                fileSize += 1
                                f.write(dataIn)
                            else:
                                break
                        f.close()

                    # Close connection
                    ephSocket.close()

                    print(f"Done! Transferred {fileSize} bytes")

            if argument[0] == "exit":
                # Send `ls` command to server
                sendCommand(clientSocket, 2)

                clientSocket.close()

                print(f"Exiting...")
                sys.exit(0)


if __name__ == '__main__':
    main()
