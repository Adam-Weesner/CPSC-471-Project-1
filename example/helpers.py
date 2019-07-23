def sendCommand(socket, code, data=None):
    out = bytearray(b'\x01')
    out.append(code)
    if type(data) is str:
        out += bytearray(data, "utf-8")
    elif type(data) is bytes:
        out += data
    out += b'\x00'
    
    socket.send(out)

def messageReader(socket):
    buffer = []
    while 1:
        newByte = socket.recv(1)
        buffer.append(newByte)
        if newByte == b"\x01":
            # Got start of message, reset the buffer
            buffer = []
        elif newByte == b"\x00":
            # Got end of message, parse it
            print(b''.join(buffer[0:-1]).decode('utf-8'))
            buffer = []
            return