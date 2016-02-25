"""
A server controls the experimental process and handles multiple clients using threads
"""
import logging
import threading
import utilities
import constants


class Server:
    def __init__(self, port, hostname):
        logging.basicConfig(filename='serverLog.log', level=logging.DEBUG)

        self.host = hostname    # '' means connecting to all hosts
        self.port = port
        # self.num_clients = num_clients
        self.sock = None
        self.sending_thread = None
        self.sending = False
        self.receiving_thread = None
        self.receiving = False
        self.clients = []
        self.container_lock = threading.Lock()

    def run(self):
        self.sock = utilities.open_socket(self.host, self.port)
        self.sending = True
        self.sending_thread = threading.Thread(target=self.send, args=())
        self.sending_thread.start()
        self.connect()

    def connect(self):
        # if self.sock is None:
        #     utilities.open_socket(self.sock, self.host, self.port)

        while True:  # TODO while len(self.connections) < num_clients ?
            conn, addr = self.sock.accept()
            conn.settimeout(constants.CONNECTION_TIMEOUT)
            self.container_lock.acquire()
            self.clients += [(conn, addr)]
            self.container_lock.release()
            logging.info("Connected to " + addr + ".")
            self.receiving = True
            self.receiving_thread = threading.Thread(target=self.receive, args=(conn, addr))
            self.receiving_thread.start()

    def send(self):
        # TODO should send data from all clients to all the other clients
        # TODO Use try catch; remove from connections if error
        # Assuming there's only one server and one client right now
        while True:
            self.sock.sendall(utilities.pack_data())

    def receive(self, client, addr):
        while self.receiving:
            try:
                data = utilities.recv_data(client)
                if data:
                    self.handle_data(addr, data)
                else:
                    logging.error("Client " + addr + " disconnected")
            except RuntimeError:
                client.close()
                logging.error("Server socket connection to " + addr + " broken.")
                # TODO remove from connections
                # TODO should try reconnecting?
            except:
                client.close()
                logging.error("Unexpected exception. Server connection to " + addr + " closed.")
                # TODO remove from connections
                # TODO should try reconnecting?
        client.close()

    def exit(self):
        self.receiving = False
        self.sending = False
        self.sending_thread.join()
        self.receiving_thread.join()

    def handle_data(self, addr, data):
        print "Server received data:", addr, data
        # will need a lock here if manipulating shared resources


if __name__ == "__main__":
    server = Server(constants.PORT, constants.LOCAL_HOST)
    server.run()
