"""
A server controls the experimental process and handles multiple clients using threads
"""
import logging
import threading
import utilities
import constants


class Server:
    def __init__(self, hostname, port):
        logging.basicConfig(filename='serverLog.log', level=logging.DEBUG)

        self.host = hostname    # '' means connecting to all hosts
        self.port = port
        # self.num_clients = num_clients
        self.sock = None
        self.connections = []
        # self.lock = threading.Lock()

    def connect(self):
        if self.sock is None:
            utilities.open_socket(self.sock, self.host, self.port)

        while True:  # TODO while len(self.connections) < num_clients ?
            conn, addr = self.sock.accept()
            conn.settimeout(constants.CONNECTION_TIMEOUT)
            self.connections += [(conn, addr)]
            logging.info("Connected to " + addr + ".")
            threading.Thread(target=self.receive, args=(conn, addr)).start()

    def send(self):
        # TODO should send data from all clients to all the other clients
        while True:
            self.sock.sendall(utilities.pack_data())

    def receive(self, client, addr):
        while True:
            try:
                data = utilities.recv_data(client)
                if data:
                    self.handle_data(addr, data)
                else:
                    logging.error("Client " + addr + " disconnected")
            except:
                client.close()
                logging.error("Unexpected exception. Connection to " + addr + " closed.")

    def handle_data(self, addr, data):
        print addr, data
        # will need a lock here if manipulating shared resources
