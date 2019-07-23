def sendCommand(socket, code, data=None):
    out = bytearray(b'\x01')
    out.append(code)
    if type(data) is str:
        out += bytearray(data, "utf-8")
    elif type(data) is bytes:
        out += data
    out += b'\x00'
    
    socket.send(out)

