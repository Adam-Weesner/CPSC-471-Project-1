#!/usr/bin/env python3
from socket import *
import sys
import threading

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
    clientSocket.send(b'\x01\x04\x00')
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

def main():
    clientPort = int(sys.argv[1])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('', clientPort))
    print("made connection to ", clientPort)
    clientSocket.send(b'\x01Greetings\x00')
    
    while 1:
            #threading.Thread(target=serverHandler, args=(clientSocket, clientPort)).start()
            argument = input("Please input a command >> ")
            if argument == "ls":
                cmdList(clientSocket)
            serverHandler(clientSocket, clientPort)
        
    
            

if __name__ == '__main__':
    main()