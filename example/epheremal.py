from socket import *

# we need to create the port to send to the client
# create a new socket on the server
# send that socket to the client
# have client establish connection
# then send over data
def epheremal():
    epheremalSocket = socket(AF_INET, SOCK_STREAM)
    epheremalSocket.bind(('', 0))
    return epheremalSocket.getsockname()