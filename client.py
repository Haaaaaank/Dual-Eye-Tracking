"""
A client is a thread, 
"""
import socket
import threading

class Client:
    def __init__(self, hostname):
        self.host = hostname
        self.PORT = 13000    # TODO input as parameter?
        self.BUFFSIZE = 1024
        self.BACKLOG = 5
        self.TIMEOUT = 60