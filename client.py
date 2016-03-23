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
import constants
from networking import Connection


class Client(object):
    """
    The main class containing the wxPython graphical interface.
    """
    def __init__(self):
        print "client.py/Client.__init__"
        self.isConnected = False
        self.network = None
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
        # A thread to listen to the network and display messages from server
        self.network = Connection(constants.host, self.connected, self.display, self.lost_connection)
        self.network.start()

    def disconnect(self):
        # Disconnect from server
        name = self.get_data()
        self.network.send("/quit " + name)

    def send(self):
        # Send the data to server. Data is obtained by get_data().
        print "client.py/Client.send"
        if self.isConnected:
            sendData = self.get_data()
            print "client_send: ", sendData
            if len(sendData):
                self.network.send(sendData)

    def set_name(self):
        print "client.py/Client.set_name"
        """
            Set an alternative name
            TODO: name does not come from get_data(), but?
        """
        if self.isConnected:
            name = self.get_data()
            if len(name):
                self.network.send("/name " + name)

    """
    def brb(self, event):
        print "client.py/Client.brb"
        "*Be Right Back* and *I'm Back* button call back"
        msg = self.get_data()
        if self.here:
            # switch from here to away
            self.here = False
            self.net.send("/brb " + msg)
        else:
            # switch from away to here
            self.here = True
            self.net.send("/back " + msg)
    """

    def connected(self):
        # This function is invoked in networking.Connection.run()
        print "client.py/Client.connected"
        self.isConnected = True

    def display(self, msg):  # TODO DISPLAY EYE POSITION
        print "client.py/Client.display"
        # Message to display from the chat server.
        # Invoked via :func:`wx.CallAfter` in :mod:`rendezvous`.
        print msg

    def lost_connection(self, msg):  # TODO
        # This function is invoked in networking.Connection.run() when connection is lost
        print "client.py/Client.lostConnection"
        self.network.join()

    def quit(self):
        # Quit connection
        print "client.py/Client.quit"
        if self.isConnected:
            self.isConnected = False
            self.network.send("/quit" + self.get_data())  # TODO ?
            self.network.join()


if __name__ == "__main__":
    print "client.py/__main__"
    # set host name from command line arguments, if any
    if len(sys.argv) > 1:
        constants.host = sys.argv[1]
    else:
        constants.host = constants.DEFAULT_HOST
    chat = Client()
    chat.connect()
    while True:
        chat.send()
        time.sleep(3)
