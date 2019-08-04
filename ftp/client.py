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
                if len(argument) != 1:
                    print(f"ERROR - ls command does not accept additional arguments\n")
                else:
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
                if len(argument) != 2:
                    print(f"ERROR - Please write commands in the format of: 'put <fileName>'\n")
                else:
                    # Puts a file to the server
                    fileName = argument[1]

                    # Check that the file exists
                    if not os.path.exists(fileName):
                        print(f"{fileName} does not exist. File must be in same directory as {__file__}\n")
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

                    print(f"Done! Transferred {os.path.getsize(fileName)} bytes\n")

            elif argument[0] == "get":
                if len(argument) != 2:
                    print(f"ERROR - Please write commands in the format of: 'get <fileName>'\n")
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
                    isFile = True

                    #check if empty file/file not found
                    dataIn = ephSocket.recv(1)
                    if dataIn == b"":
                        print(f"No data returned. File does not exist at server\n")
                    else: #transfer the file
                        with open(fileName, 'wb') as f:
                            fileSize += 1
                            f.write(dataIn)
                            while True:
                                dataIn = ephSocket.recv(1)
                                if dataIn:
                                    fileSize += 1
                                    f.write(dataIn)
                                else:
                                    break
                        f.close()
                        print(f"Done! Transferred {fileSize} bytes\n")


                    # Close connection
                    ephSocket.close()

            elif argument[0] == "exit":

                if len(argument) != 1:
                    print(f"ERROR - exit command does not accept additional arguments\n")
                else:
                    # Send `ls` command to server
                    sendCommand(clientSocket, 2)

                    clientSocket.close()

                    print(f"Exiting...")
                    sys.exit(0)

            else:
                print(f"ERROR - not a valid command. Enter one of the following commands: ls, get, put, exit\n")


if __name__ == '__main__':
    main()
