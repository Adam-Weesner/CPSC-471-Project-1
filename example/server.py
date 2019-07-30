#!/usr/bin/env python3
from socket import *
from subprocess import PIPE
import subprocess
import sys
import threading
import os

from dataConnection import DataConnection
from helpers import sendCommand

START = 0x01 # 0b000001

def parseMessage(buffer, clientSocket):
    # Command format:
    #  0     n-bytes      n+1
    # SoM   Data Length  EoM
    # 0x01 ...........  0x00

    print(buffer)
    if buffer[1] == b'\x05':
        conn = DataConnection(clientSocket, timeout=3)
        try:
            conn.waitClient()
        except:
            print(f"Client didn't connect - aborting transfer.")
            return
        conn.clientSocket.send(str.encode(f"\x01{subprocess.run(['ls', '-l'], stdout=PIPE, stderr=PIPE, universal_newlines=True).stdout}\x00"))
        print(f"sent `ls` to client")

    elif buffer[1] == b'\x04':
        fileName = (b''.join(buffer[2:-1])).decode('utf-8')

        # TODO: Remove this
        print(f"Client wants to upload {fileName}")

        # Setup ephemeral port
        conn = DataConnection(clientSocket, timeout=3)
        try:
            conn.waitClient()
        except:
            print(f"Client didn't connect - aborting transfer.")
            return

        print("Client connected, receiving file...")
        fileSize = 0
        with open(os.path.join('files', fileName), 'wb') as f:
            while True:
                dataIn = conn.clientSocket.recv(1)
                if dataIn:
                    fileSize += 1
                    f.write(dataIn)
                else:
                    break

            f.close()

        print(f"Received {fileSize} bytes from client")

    # Get command
    if buffer[1] == b'\x03':
        fileName = (b''.join(buffer[2:-1])).decode('utf-8')

        # TODO: Remove this
        print(f"Client wants to get {fileName}")

        # Setup ephemeral port
        conn = DataConnection(clientSocket, timeout=3)
        try:
            conn.waitClient()
        except:
            print(f"Client didn't connect - aborting transfer.")
            return

        # Check that the file exists
        if not os.path.exists(fileName):
            print(f"{fileName} does not exist. File must be in same directory as {__file__}")
            return

        print("Client connected, transferring file...")

        # Transfer file
        with open(fileName, 'rb') as f:
            clientSocket.sendall(f.read())

        print(f"Transferred {fileName} to client")

    # Exit command
    if buffer[1] == b'\x02':
        print(f"Client is leaving")


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
            threading.Thread(target=parseMessage, args=(commandBuffer, clientSocket)).start()
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
