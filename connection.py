"""
    The Connection class handles all the socket networking stuff of a client
"""
"""
    Copyright 2016 Meng Du

    Adopted from Tim Bower's Multi-threaded Chat Server
    Original work Copyright 2009 Tim Bower

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
"""

import socket
import threading
import net_constants


class Connection(threading.Thread):
    # A separate thread class to make and manage the socket connection to the server.

    def __init__(self, host, connected, display, lost):
        print "networking.py/Connection.__init__"
        threading.Thread.__init__(self)
        self.host = host
        self.socket = None
        self.socketLock = threading.Lock()
        self.connected = connected
        self.display = display
        self.lost = lost

    def run(self):
        # The new thread starts here to listen for data from the server
        print "networking.py/Connection.run"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect
        try:
            self.socket.connect((self.host, net_constants.PORT))
        except Exception as e:
            print "Unable to connect to the server. Error: " + str(e)
            self.lost("")
            return

        self.socket.settimeout(net_constants.CLIENT_SOCKET_TIMEOUT)  # TODO Is there a better way than timeout?
        self.connected()

        # Receive data
        while True:
            # print "networking.py/Connection.run/while_loop"
            try:
                with self.socketLock:
                    data = self.socket.recv(net_constants.BUFFER_SIZE)
            except socket.timeout:
                # print "timeout"
                continue
            except Exception as e:  # server was stopped or had some error
                print "Network Connection closed by the server. " + str(e)
                self.lost("")
                break

            if len(data):
                self.display(data)
            else:
                # no data when peer does a socket.close()
                self.lost("Network Connection closed.")
                break

        # End of receiving loop
        self.socket.close()

    def send_to_server(self, msg):
        print "networking.py/Connection.send"
        # Send a message to the server - called from and executes in the main thread
        try:
            with self.socketLock:
                self.socket.send(msg)
        except Exception as e:
            print "Error:", e
