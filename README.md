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

#### Starting the Server

```
python3 ftp/server.py <port>
ex: python3 ftp/server.py 12000
```

#### Starting the Client

```
python3 ftp/client.py <hostname> <port>
ex: python3 ftp/client.py 127.0.0.1 12000
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

Gets a file from the server and downloads it to the client.

##### exit

```
Please input a command >> exit
```

## Notes

**Requires Python 3.6 or greater**
