#!/bin/env python

"""
    A client represents a user with an eye tracker. It sends its eye tracking data
    to the server, and receives data of all the other clients from the server.
"""
"""
    Copyright 2016 Meng Du

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
"""

import time
import random
import datetime
import threading
import net_constants
import commands
import utilities
from connection import Connection


class Client(threading.Thread):
    """
    The main class containing the wxPython graphical interface.
    """
    def __init__(self):
        print "client.py/Client.__init__"
        threading.Thread.__init__(self)
        self.isConnected = False
        self.connection = None
        # self.tempCounter = 0
        self.tempName = random.randint(1, 100)
        self.current_data = None

    def get_data(self):
        # print "client.py/Client.get_data"
        # data = str(self.tempName) + ": " + str(self.tempCounter)
        # self.tempCounter += 1
        data = utilities.get_data()
        if len(data):
            if data is not self.current_data:
                self.current_data = data
                return data
            else:  # ignore duplicates
                return None
        else:
            return None

    def connect(self):
        # Connect to server
        print "client.py/Client.connect"
        # Start another thread for the connection
        self.connection = Connection(net_constants.host, self.connected, self.display, self.lost_connection)
        self.connection.start()

    def disconnect(self):
        # Disconnect from server
        name = self.get_data()  # TODO whut
        self.connection.send_to_server(net_constants.CMD_QUIT + name)

    def send(self):
        # Send the data to server. Data is obtained by get_data().
        # print "client.py/Client.send"
        if self.isConnected:
            data = self.get_data()
            if data is not None:
                print "client_send: ", data
                self.connection.send_to_server(data)

    def set_name(self):
        print "client.py/Client.set_name"
        # Set an alternative name
        if self.isConnected:
            name = self.get_data()  # TODO change this, name does not come from get_data()
            if len(name):
                self.connection.send_to_server(net_constants.CMD_RENAME + name)

    def connected(self):
        # This function is invoked in networking.Connection.run()
        print "client.py/Client.connected"
        self.isConnected = True

    def display(self, data):
        print "client.py/Client.display"
        # Display the eye positions
        utilities.display(data)

    def lost_connection(self, msg):  # TODO
        # This function is invoked in networking.Connection.run() when connection is lost
        print "client.py/Client.lostConnection"
        self.connection.join()

    def quit(self):
        # Quit connection
        print "client.py/Client.quit"
        if self.isConnected:
            self.isConnected = False
            self.connection.send_to_server(net_constants.CMD_QUIT + self.get_data())  # TODO ?
            self.connection.join()

    def run(self):
        # TODO
        import sys
        old_stdout = sys.stdout
        sys.stdout = open("clientout" + str(self.tempName) + ".txt", "w")
        # - TODO -

        self.connect()
        time.sleep(0.05)
        while True:
            self.send()
            time.sleep(0.001)

        sys.stdout = old_stdout


if __name__ == "__main__":
    # if len(sys.argv) > 1:
    #     net_constants.host = sys.argv[1]
    client_thread = Client()
    client_thread.start()
