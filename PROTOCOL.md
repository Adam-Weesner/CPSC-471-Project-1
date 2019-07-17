# Owl Theory Protocol Design

## Basic message format

`0x42 0xCMD [0xDATA...0xDATA-N] 0x00`

* `0x42` denotes start of message (SoM)
* Minimum message size is 3 bytes (if no data is included)
* `0xCMD` indicates one-byte command code from table in the [quick reference](#quick-reference).
* **All messages are null-terminated.**

## Commands

### Quick Reference

|Sent from|Command Code|Command Name|Command Alias|
|---|---|---|---|
|Server|0x01|[Data port opened](#0x01-data-port-opened)|N/A|
|Client|0x02|[Get](#0x02-get-file-get-path)|`get <path>`|
|Client|0x03|[Put](#0x03-put-file-put-path)|`put <path>`|
|Client|0x04|[List](#0x04-list-ls-path)|`ls [path]`|

### Server-to-client

#### `0x01` Data port opened

Sent to client when server has opened an ephemeral port. Contains one byte of data, indicating offset of port number from `27000`.

Example: server opens port 27023

```
SERVER:
 SoM  CMD PORT  NUL
0x42 0x01 0x17 0x00
```

### Client-to-server

#### `0x02` Get file `get <path>`

Gets a file from the server and sends it to the client.

After receiving this command, the server should open an ephemeral port and send the port number to the client with command `0x01`.

Example for retrieving `helloworld.txt` with server opening ephemeral port at 27000 + 0x32

```
CLIENT:
 SoM  CMD    h    e    l    l    o    w    o    r    l    d    .    t    x    t  NUL
0x42 0x02 0x68 0x65 0x6c 0x6c 0x6f 0x77 0x6f 0x72 0x6c 0x64 0x2e 0x74 0x78 0x74 0x00
 
SERVER:
 SoM  CMD PORT  NUL
0x42 0x01 0x32 0x00
```

#### `0x03` Put file `put <path>`

Puts a file from to server from the client.

After receiving this command, the server should open an ephemeral port and send the port number to the client with command `0x01`.

Example for retrieving `helloworld.txt` with server opening ephemeral port at 27000 + 0x88

```
CLIENT:
SoM  CMD    h    e    l    l    o    w    o    r    l    d    .    t    x    t  NUL
0x42 0x03 0x68 0x65 0x6c 0x6c 0x6f 0x77 0x6f 0x72 0x6c 0x64 0x2e 0x74 0x78 0x74 0x00

SERVER:
 SoM  CMD PORT  NUL
0x42 0x01 0x88 0x00
```

#### `0x04` List `ls [path]`

Lists files in a directory, if given. Otherwise, list files at the servers 'root' directory (TBD; this could be a configuration variable, or we could just assume the root directory to be where `server.py` is executing; might be insecure).

After receiving this command, the server should open an ephemeral port and send the port number to the client with command `0x01`.

Example for listing contents of `joshsfiles/` with server opening ephemeral port at 27000 + 0xFF

```
CLIENT:
 SoM  CMD    j    o    s    h    s    f    i    l    e    s    /  NUL
0x42 0x04 0x6a 0x6f 0x73 0x68 0x73 0x66 0x69 0x6c 0x65 0x73 0x2f 0x00

SERVER:
 SoM  CMD PORT  NUL
0x42 0x01 0xFF 0x00
```
