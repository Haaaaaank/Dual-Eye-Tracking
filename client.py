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

import sys
import time
import random
import datetime
import threading
import constants
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
        self.tempCounter = 0
        self.tempName = random.randint(1, 100)

    def get_data(self):
        # TODO Return the eye position
        print "client.py/Client.get_data"
        data = str(self.tempName) + ": " + str(self.tempCounter)
        self.tempCounter += 1
        if len(data):
            return data
        else:
            return ''

    def connect(self):
        # Connect to server
        print "client.py/Client.connect"
        # Start another thread for the connection
        self.connection = Connection(constants.host, self.connected, self.display, self.lost_connection)
        self.connection.start()

    def disconnect(self):
        # Disconnect from server
        name = self.get_data()  # TODO whut
        self.connection.send_to_server("/quit " + name)

    def send(self):
        # Send the data to server. Data is obtained by get_data().
        print "client.py/Client.send"
        if self.isConnected:
            sendData = self.get_data()
            print "client_send: ", sendData
            if len(sendData):
                self.connection.send_to_server(sendData)

    def set_name(self):
        print "client.py/Client.set_name"
        # Set an alternative name
        if self.isConnected:
            name = self.get_data()  # TODO change this, name does not come from get_data()
            if len(name):
                self.connection.send_to_server("/name " + name)

    def connected(self):
        # This function is invoked in networking.Connection.run()
        print "client.py/Client.connected"
        self.isConnected = True

    def display(self, data):  # TODO DISPLAY EYE POSITION
        print "client.py/Client.display"
        # Display the eye positions
        print datetime.datetime.now()
        print data

    def lost_connection(self, msg):  # TODO
        # This function is invoked in networking.Connection.run() when connection is lost
        print "client.py/Client.lostConnection"
        self.connection.join()

    def quit(self):
        # Quit connection
        print "client.py/Client.quit"
        if self.isConnected:
            self.isConnected = False
            self.connection.send_to_server("/quit" + self.get_data())  # TODO ?
            self.connection.join()

    def run(self):
        self.connect()
        time.sleep(0.2)
        for i in range(50):
            self.send()
            time.sleep(1)

        time.sleep(0.2)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        constants.host = sys.argv[1]
    else:
        constants.host = constants.DEFAULT_HOST
    client_thread = Client()
    client_thread.start()
