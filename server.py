"""
A server controls the experimental process and handles
multiple clients using threads
"""
import socket
import logging
import sys
import threading


class Server:
    def __init__(self):
        logging.basicConfig(filename='serverLog.log', level=logging.DEBUG)

        self.host = ''    # TODO input as parameter?  # '' means connecting to all hosts
        self.port = 13000    # TODO input as parameter?
        self.BUFFSIZE = 1024
        self.BACKLOG = 5
        self.TIMEOUT = 60

        self.sock = None
        # self.num_clients = num_clients
        self.connections = []
        # self.lock = threading.Lock()

    def open_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.HOST, self.PORT))
            self.sock.listen(self.BACKLOG)
        except socket.error, (value, message):
            if self.sock:
                self.sock.close()
            logging.error("Could not open socket. " + message)
            sys.exit(1)

        logging.info("Socket opened. Waiting for a connection.")

    def connect(self):
        self.open_socket()
        while True:  # TODO while len(self.connections) < num_clients ?
            conn, addr = self.sock.accept()
            conn.settimeout(self.TIMEOUT)
            self.connections += [(conn, addr)]
            logging.info("Connected to " + addr + ".")
            threading.Thread(target=self.run, args=(conn, addr)).start()

    def run(self, client, addr):
        while True:
            try:
                data = client.recv(self.BUFFSIZE)
                if data:
                    response = data
                    self.handle_data(response)
                else:
                    logging.error("Client " + addr + " disconnected")
            except:
                client.close()
                logging.error("Unexpected exception. Connection to " + addr + " closed")

    def handle_data(self, data):
        print data
