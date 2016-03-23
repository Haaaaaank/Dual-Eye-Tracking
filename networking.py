"""
    The networking portion
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
import constants


class Connection(threading.Thread):
    # A separate thread class to make and manage the socket connection to the server.

    def __init__(self, host, connected, display, lost):
        print "networking.py/Connection.__init__"
        threading.Thread.__init__(self)
        self.host = host
        self.socket = None
        self.connected = connected
        self.display = display
        self.lost = lost
        self.msgLock = threading.Lock()
        self.numMsg = 0
        self.msg = []

    def run(self):
        # The new thread starts here to listen for data from the server
        print "networking.py/Connection.run"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        try:
            self.socket.connect((self.host, constants.PORT))
        except:
            self.lost("Unable to connect to %s. Please check the server." % self.host)
            return
        self.connected()
        while True:
            self.__send()
            try:
                data = self.socket.recv(constants.BUFFER_SIZE)
            # Timeout once in a while just to check user input
            except socket.timeout:
                continue
            except:  # server was stopped or had some error
                self.lost("Network Connection closed by the server.")
                break
            if len(data):
                self.display(data)
            else:
                # no data when peer does a socket.close()
                self.lost("Network Connection closed.")
                break
        # End loop of network send / recv data
        self.socket.close()

    def __send(self):
        print "networking.py/Connection.__send"
        """
        Actually send a message, if one is available, to the server.
        Need to acquire lock for the message queue.
        """
        self.msgLock.acquire()
        if self.numMsg > 0:
            self.socket.send(self.msg.pop(0))
            self.numMsg -= 1
        self.msgLock.release()

    def send(self, msg):
        print "networking.py/Connection.send"
        """
        Set up to send a message to the server - called from main thread
        This is the only part of this class that executes in the main tread,
        We use a list to drop off the message for the networking thread to pick
        up and actually send it.  We could use a Queue.Queue object, which
        comes standard with Python and not have to mess with locks.  When the
        graphics were done with Tkinter, I did that to send data back to
        the main thread.  This locking stuff is pretty simple, so it's a good
        place to see how to do the locking ourself.
        """
        self.msgLock.acquire()
        self.msg.append(msg)
        self.numMsg += 1
        self.msgLock.release()
