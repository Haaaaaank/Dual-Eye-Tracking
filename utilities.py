import sys
import socket
import logging
import struct
import constants

counter = 0


def open_socket(sock, host, port):
    """
    Construct the socket and start listening
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(constants.BACKLOG)
    except socket.error, (value, message):
        if sock:
            sock.close()
        logging.error("Could not open socket. " + message)
        sys.exit(1)

    logging.info("Socket opened. Waiting for a connection.")


def pack_data():
    """
    Get data and prefix them with a 4-byte length (in network byte order)
    """
    global counter
    counter += 1
    data = "test data " + str(counter)

    data = struct.pack('>I', len(data)) + data
    return data


def recv_data(sock):
    """
    Read message length and unpack it into an integer
    """
    raw_size = recvall(sock, 4)
    if not raw_size:
        return None
    size = struct.unpack('>I', raw_size)[0]
    # Read the data
    return recvall(sock, size)


def recvall(sock, size):
    """
    A helper function that receives data of 'size' length or returns None if EOF is hit
    """
    data = ''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data
