"""
A client
"""
import logging
import threading
import utilities
import constants


class Client:
    def __init__(self, port, hostname=""):
        logging.basicConfig(filename='clientLog.log', level=logging.DEBUG)

        self.host = hostname
        self.port = port
        self.sock = None
        self.sending_thread = None
        self.sending = False
        self.receiving_thread = None
        self.receiving = False

    def run(self):
        logging.info("Client started.")
        self.sock = utilities.open_socket(self.host, self.port)
        self.connect()

    def connect(self):
        conn, addr = self.sock.accept()
        conn.settimeout(constants.CONNECTION_TIMEOUT)
        logging.info("Connected to " + addr + ".")

        # send
        self.sending = True
        self.sending_thread = threading.Thread(target=self.send, args=(conn, addr))
        self.sending_thread.start()

        # receive
        self.receiving = True
        self.receiving_thread = threading.Thread(target=self.receive, args=(conn, addr))
        self.receiving_thread.start()


    def send(self, client, addr):
        logging.info("Start sending data.")
        while self.sending:
            client.sendall(utilities.pack_data())

    def receive(self, client, addr):
        while self.receiving:
            try:
                data = utilities.recv_data(client)
                if data:
                    self.handle_data(addr, data)
                else:
                    logging.error("Client " + addr + " disconnected")
            except:
                client.close()
                logging.error("Unexpected exception. Client connection to " + addr + " closed.")
                # TODO remove from connections
                # TODO should try reconnecting?
        client.close()

    def exit(self):
        self.receiving = False
        self.sending = False
        self.sending_thread.join()
        self.receiving_thread.join()

    def handle_data(self, addr, data):
        print "Client received data:", addr, data
        # will need a lock here if manipulating shared resources


if __name__ == "__main__":
    client = Client(constants.PORT, "")
    client.run()
