# Owl Theory Protocol Design

## Message format

`0x01 0xCMD [0xDATA...0xDATA-N] 0x00`

* `0x01` denotes start of message (SoM)
* Minimum message size is 3 bytes (if no data is included); there is theoretically no maximum message size.
* In the examples, `0xCMD` indicates one-byte command code from table in the [quick reference](#quick-reference).
* **All messages are null-terminated to signify the end of the command.**
* The client will typically expect a response from the server immediately after processing a command from the client.

## Commands

A swimlane sequence diagram can be found and edited here: https://swimlanes.io/d/UhF7Bk5NL

The sequence diagram is also embedded at the bottom of this document.

### Quick Reference

|Sent from|Command Code|Command Name|Command Alias|
|---|---|---|---|
|Server|0x02|[Data port opened](#0x02-data-port-opened)|N/A|
|Client|0x02|Client Quitting|N/A|
|Client|0x03|[Get](#0x03-get-file-get-path)|`get <filename>`|
|Client|0x04|[Put](#0x04-put-file-put-path)|`put <filename>`|
|Client|0x05|[List](#0x05-list-ls-path)|`ls`|

### Server-to-client

#### `0x02` Data port opened

Sent to client when server has opened an ephemeral port. Contains two bytes of data indicating the port which was opened.

Example: server opens port 32768 = 0x80 0x00

```
SERVER:
 SoM  CMD PORTH PORTL  NUL
0x01 0x02  0x80  0x00 0x00
```

### Client-to-server

#### `0x03` Get file `get <filename>`

Gets a file from the server and sends it to the client.

After receiving this command, the server should open an ephemeral port and send the port number to the client with command `0x02`.

Example for retrieving `helloworld.txt` with server opening ephemeral port at 32768

```
CLIENT:
 SoM  CMD    h    e    l    l    o    w    o    r    l    d    .    t    x    t  NUL
0x01 0x03 0x68 0x65 0x6c 0x6c 0x6f 0x77 0x6f 0x72 0x6c 0x64 0x2e 0x74 0x78 0x74 0x00
 
SERVER:
 SoM  CMD PORTH PORTL  NUL
0x01 0x02  0x80  0x00 0x00
```

#### `0x04` Put file `put <filename>`

Puts a file from to server from the client.

After receiving this command, the server should open an ephemeral port and send the port number to the client with command `0x02`.

Example for retrieving `helloworld.txt` with server opening ephemeral port at 32768

```
CLIENT:
 SoM  CMD    h    e    l    l    o    w    o    r    l    d    .    t    x    t  NUL
0x01 0x04 0x68 0x65 0x6c 0x6c 0x6f 0x77 0x6f 0x72 0x6c 0x64 0x2e 0x74 0x78 0x74 0x00

SERVER:
 SoM  CMD PORTH PORTL  NUL
0x01 0x02  0x80  0x00 0x00
```

#### `0x05` List `ls`

Lists files in the server's `files` directory.

After receiving this command, the server will respond with a file listing.

```
CLIENT:
 SoM  CMD  NUL
0x01 0x05 0x00

SERVER:
 SoM  CMD  [Variable length file listing]  NUL
0x01 0x05  .............................. 0x00
```

## Sequence Diagram

![Sequence diagram](sequence.png)
