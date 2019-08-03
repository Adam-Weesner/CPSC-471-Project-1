# CPSC 471 - Assignment 1
## Group Members
1. Adam Weesner - aweesner@csu.fullerton.edu
2. Melissa Riddle
3. Joshua Ferrara - joshferrara@csu.fullerton.edu
4. Hector Medina - hecmed@csu.fullerton.edu

## Language

**Python 3.6 or greater**

## Protocol Design

Please see [PROTOCOL.md](./PROTOCOL.md)

## How To Execute Program

**Note:** `server.py` must be ran in the context of the `ftp` directory or a directory that contains a `files` directory. Uploads will be placed in the `files` directory.

#### Starting the Server

```
cd ftp && python3 ./server.py <port>
ex: cd ftp && python3 ./server.py 12000
```

#### Starting the Client

```
cd ftp && python3 ./client.py <hostname> <port>
ex: cd ftp && python3 ./client.py 127.0.0.1 12000
```

#### Client commands:

##### ls

```
Please input a command >> ls
```

Lists the files present in the `files` directory on the server.

##### put

```
Please input a command >> put <filename>
```

Sends a file from the client to the server. The file will be placed in the server's `files` directory.

##### get

```
Please input a command >> get <filename>
```

Gets a file from the server's `files` directory and downloads it to the client.

##### exit

```
Please input a command >> exit
```

Provides a method for cleanly closing the control connection between the client and server.

## Notes

**Requires Python 3.6 or greater**
