"""
A client
"""
import socket
import logging
import threading
import utilities


class Client:
    def __init__(self, hostname, port):
        logging.basicConfig(filename='clientLog.log', level=logging.DEBUG)

        self.host = hostname
        self.port = port
        self.sock = None

    def send(self):
        while True:
            self.sock.send(utilities.pack_data())

