"""
A server controls the experimental process and handles
multiple clients using threads
"""
import logging
import threading
import utilities
import constants


class Server:
    def __init__(self):
        logging.basicConfig(filename='serverLog.log', level=logging.DEBUG)

        self.host = ''    # TODO input as parameter?  # '' means connecting to all hosts
        self.port = 13000    # TODO input as parameter?
        self.sock = None
        # self.num_clients = num_clients
        self.connections = []
        self.lock = threading.Lock()

    def connect(self):
        utilities.open_socket(self.sock, self.host, self.port)
        while True:  # TODO while len(self.connections) < num_clients ?
            conn, addr = self.sock.accept()
            conn.settimeout(constants.TIMEOUT)
            self.connections += [(conn, addr)]
            logging.info("Connected to " + addr + ".")
            threading.Thread(target=self.run, args=(conn, addr)).start()

    def send(self):
        # TODO should send data from all clients to all the other clients
        while True:
            self.sock.sendall(utilities.pack_data())

    def run(self, client, addr):
        while True:
            try:
                data = utilities.recv_data(client)
                if data:
                    self.handle_data(data)
                else:
                    logging.error("Client " + addr + " disconnected")
            except:
                client.close()
                logging.error("Unexpected exception. Connection to " + addr + " closed")

    def handle_data(self, data):
        print data
        # TODO will need the lock here
