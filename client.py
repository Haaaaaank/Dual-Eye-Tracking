"""
A client is a thread, 
"""
import socket
import logging
import threading
import utilities


class Client:
    def __init__(self, hostname):
        logging.basicConfig(filename='clientLog.log', level=logging.DEBUG)

        self.host = hostname
        self.port = 13000    # TODO input as parameter?
        self.sock = None

    def send(self):
        while True:
            self.sock.send(utilities.get_data())

