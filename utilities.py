import sys
import socket
import logging
import struct
import constants

counter = 0  # TODO this is just for test purpose


def open_socket(host, port):
    """
    Construct the socket and start listening, or terminate the program on error
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(constants.SOCKET_BACKLOG)  # start listening
    except socket.error, (value, message):
        if sock:
            sock.close()
        logging.error("Could not open socket. " + message)
        sys.exit(1)

    logging.info("Socket opened. Waiting for a connection.")
    return sock


def pack_data():
    """
    Get data and prefix them with a 4-byte length (in network byte order)
    """
    global counter
    counter += 1
    data = "test data " + str(counter)  # TODO will get data from the eye tracker

    data = struct.pack('>I', len(data)) + data  # prefix with length
    return data


def recv_data(sock):
    """
    Read message length and unpack it into an integer
    """
    raw_length = recvall(sock, constants.INTEGER_STANDARD_LENGTH)  # get the length of data
    if not raw_length:
        raise RuntimeError("Socket connection broken.")
    length = struct.unpack('>I', raw_length)[0]  # convert the length to an integer
    return recvall(sock, length)  # Read the data


def recvall(sock, length):
    """
    A helper function that receives data of 'size' length or raise error if EOF is hit
    """
    data = ""
    while len(data) <= length:
        packet = sock.recv(length - len(data))
        if not packet:
            raise RuntimeError("Socket connection broken.")
        data += packet
    return data
