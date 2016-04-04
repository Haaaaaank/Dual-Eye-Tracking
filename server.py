#!/bin/env python

"""
    The server manages the connections to all the clients, receives data from clients
    and sends them to all the other clients
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
import time
from itertools import cycle
import logging
import constants

MAX_CYCLIC_INDEX = 100


def get_msg_index(old, last, new):
    print "server.py/get_msg_index"
    """
    This computes the index value of the message queue from where the reader
    should return messages.  It accounts for having a cyclic counter.
    This code is a little tricky because it has to catch all possible
    combinations.
    old -> index of oldest (first) message in queue
    last -> index of last message read by the client thread
    new -> index of newest (last) message in the queue
    """
    if new >= old:
        # normal case
        if last >= old and last < new:
            return last - old + 1
        else:
            return 0
    else:
        # cyclic roll over (new < old)
        if last >= old:
            return last - old + 1
        elif last < new:
            return MAX_CYCLIC_INDEX - old + last
        else:
            return 0


class MSGQueue(object):
    """
    Manage a queue of messages. the threads will read and write to
    this object.  This is an implementation of the readers - writers problem
    with a bounded buffer.
    """
    def __init__(self):
        print "server.py/MSGQueue.__init__"
        self.msg = []
        self.cyclic_count = cycle(range(MAX_CYCLIC_INDEX))
        self.current = -1
        self.readers = 0
        self.writers = 0
        self.readerCounterLock = threading.Lock()
        self.writerCounterLock = threading.Lock()
        self.readPending = threading.Lock()
        self.writeLock = threading.Lock()
        self.writeLock = threading.Lock()
        self.readLock = threading.Lock()

# The messages are kept in a
# list.  Each list is a tuple containing an index number, a time stamp and
# the message.  Each thread calls the reader on a regular basis to check if
# there are new messages that it has not yet sent to it's client.
# To keep the list from growing without bound, if it is at the MAX_LEN size,
# the oldest item is removed when a new item is added.

    def reader(self, last_read):
        print "server.py/MSGQueue.reader"
        self.readPending.acquire()
        self.readLock.acquire()
        self.readerCounterLock.acquire()
        self.readers += 1
        if self.readers == 1:
            self.writeLock.acquire()
        self.readerCounterLock.release()
        self.readLock.release()
        self.readPending.release()
        # Beginning of critical section
        if last_read == self.current: # or not len(self.msg):
            return_val = None
        else:
            msg_index = get_msg_index(self.msg[0][0], last_read, self.current)
            return_val = self.msg[msg_index:]
        # End of critical section
        self.readerCounterLock.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.writeLock.release()
        self.readerCounterLock.release()
        return return_val

    def writer(self, data):
        print "server.py/MSGQueue.writer"
        self.writerCounterLock.acquire()
        self.writers += 1
        if self.writers == 1:
            self.readLock.acquire()
        self.writerCounterLock.release()
        self.writeLock.acquire()
        # here is the critical section
        self.current = self.cyclic_count.next()
        self.msg.append((self.current, time.localtime(), data))
        # End of critical section
        self.writeLock.release()
        self.writerCounterLock.acquire()
        self.writers -= 1
        if self.writers == 0:
            self.readLock.release()
        self.writerCounterLock.release()


class DataHandler(threading.Thread):
    # Store the data obtained from each client, and send them to all the other clients
    def __init__(self):
        threading.Thread.__init__(self)
        # self.clients is a dict with peer name as the key
        # and a tuple (socket, lock, data_list) as the value
        self.clients = dict()

    def add_client(self, new_sock):
        # called and executed in the main thread
        # if new_sock.getpeername() in self.clients:
        #     raise RuntimeError("Client already exists.")
        self.clients[new_sock.getpeername()] = (new_sock, threading.Lock(), [])
        
    def disconnect_client(self, name, error=None):
        if error:
            msg = name + " has exited -- " + error + "\r\n"
        else:
            msg = name + " has exited\r\n"
        # dataQueue.writer(msg)
        self.write_data(name, msg)
        # close the connection
        sock = self.clients[name][0]
        sock.close()

    def disconnect_all(self):
        for (sock, lock, _) in self.clients.values():
            with lock:
                sock.close()
        self.clients.clear()

    def write_data(self, peer_name, data):
        # add data to storage
        # this function is called and executed in the main thread
        # TODO check data here?
        _, lock, data_list = self.clients[peer_name]
        with lock:  # acquire the lock
            data_list.append(data)
            print "writing!!!!!!!!!!!!!! " + data
            print str(len(data_list)) + "???????????"


    def run(self):
        print "server.py/DataHandler.run"
        while True:
            for name in self.clients.keys():
                sock, lock, data = self.clients[name]
                with lock:
                    # send data if there is any
                    for datum in data:
                        if len(data) > 0:
                            # send to all the clients except for itself
                            for other_name in self.clients.keys():
                                if name is not other_name:
                                    print "sending!!!!!!!!!!!! " + datum
                                    other_sock = self.clients[other_name][0]
                                    other_sock.send(datum)
                            self.clients[name] = (sock, lock, [])  # empty the data list

"""
def send_to_client(sock, last_read):
    print "server.py/MSGQueue.send_to_client"
    # this function just cuts down on some code duplication
    global dataQueue
    reading = dataQueue.reader(last_read)
    if reading is None:
        return last_read
    try:
        for (last, timeStmp, msg) in reading:
            sock.send("At %s -- %s" % (time.asctime(timeStmp), msg))
    except:
        print "Error"  # TODO add err msg
    return last


def client_exit(sock, peer, error=None):
    print "server.py/MSGQueue.client_exit"
    global dataQueue
    print "A disconnect by " + peer
    if error:
        msg = peer + " has exited -- " + error + "\r\n"
    else:
        msg = peer + " has exited\r\n"
    dataQueue.writer(msg)
"""

def handle_client(client_sock):
    global dataHandler
    print "server.py/MSGQueue.handle_client"
    # a server thread that receives data from each client_sock
    # last_reads of -1 gets all available messages on first read, even
    # if message index cycled back to zero.
    last_read = -1
    # the identity of each user is called peer - they are the peer on the other
    # end of the socket connection.
    peer_name = client_sock.getpeername()
    print "Got connection from ", peer_name
    msg = str(peer_name) + " has joined\r\n"
    # dataQueue.writer(msg)
    dataHandler.write_data(peer_name, msg)

    while True:
        # check for and send any new messages
        # last_read = send_to_client(client_sock, last_read)
        try:
            data = client_sock.recv(constants.BUFFER_SIZE)  # TODO recvall?
        except socket.timeout:
            continue
        except socket.error, (value, message):
            # caused by main thread doing a socket.close on this socket
            # It is a race condition if this exception is raised or not.
            print "Error: " + message
            return
        except:  # some error or connection reset by peer
            dataHandler.disconnect_client(peer_name)  # TODO add error msg
            break
        if not len(data):  # a disconnect (socket.close() by client)
            dataHandler.disconnect_client(peer_name)  # TODO add error msg
            break

        # Process the data received from the client
        # Check if it is a command
        if data.startswith('/name'):
            old_name = peer_name
            peer = data.replace('/name', '', 1).strname()
            if len(peer):
                # dataQueue.writer("%s now goes by %s\r\n" % (str(old_name), str(peer)))
                dataHandler.write_data(peer_name, "%s now goes by %s\r\n" % (str(old_name), str(peer_name)))
            else:
                peer_name = old_name

        elif data.startswith('/quit'):
            bye = data.replace('/quit', '', 1).strname()
            if len(bye):
                msg = "%s is leaving now -- %s\r\n" % (str(peer_name), bye)
            else:
                msg = "%s is leaving now\r\n" % (str(peer_name))
            # dataQueue.writer(msg)
            dataHandler.write_data(peer_name, msg)  # TODO unnecessary?
            dataHandler.disconnect_client(peer_name)
            break

        else:  # received actual data
            # dataQueue.writer("Message from %s:\r\n\t%s\r\n" % (str(peer), data))
            dataHandler.write_data(peer_name, "Message from %s:\r\n\t%s\r\n" % (str(peer_name), data))


if __name__ == '__main__':
    print "server.py/__main__"

    # TODO
    import sys
    old_stdout = sys.stdout
    # sys.stdout = open("serverout.txt", "w")
    # - TODO -

    # dataQueue = MSGQueue()  # a global data queue

    # Set up the socket.
    connection_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_sock.bind((constants.host, constants.PORT))
    connection_sock.listen(constants.SOCKET_BACKLOG)

    dataHandler = DataHandler()
    dataHandler.start()

    while True:
        print "Waiting for Connections"
        try:
            clientSock, clientAddr = connection_sock.accept()
            print "client accepted"
            # set a timeout so it won't block forever on socket.recv().
            # Clients that are not doing anything check for new messages 
            # after each timeout.
            clientSock.settimeout(constants.SERVER_SOCKET_TIMEOUT)
        except KeyboardInterrupt:
            # shutdown - force the threads to close by closing their socket
            connection_sock.close()
            dataHandler.disconnect_all()
            break
        #except:
        #    traceback.print_exc()
        #    continue

        # clients.append(clientSock)
        dataHandler.add_client(clientSock)
        clientHandler = threading.Thread(target=handle_client, args=(clientSock,))
        clientHandler.setDaemon(True)
        clientHandler.start()

    sys.stdout = old_stdout