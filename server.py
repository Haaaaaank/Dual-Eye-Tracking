#!/bin/env python

"""
    The server manages the connections to all the clients, receives data from clients
    and sends them to all the other clients
"""
"""
    Copyright 2016 Meng Du

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
"""

import socket
import threading
import logging
import net_constants
import commands


class DataHandler(threading.Thread):
    # A DataHandler maintains the data obtained from each client as a shared resource
    # and continuously checks and sends the new data to all the other clients
    def __init__(self):
        threading.Thread.__init__(self)
        # self.clients is a dict with peer name as the key
        # and a tuple (socket, lock, data_list) as the value
        self.clients = dict()

    def add_client(self, new_sock):
        # called and executed in the server main thread
        # if new_sock.getpeername() in self.clients:
        #     raise RuntimeError("Client already exists.")
        self.clients[new_sock.getpeername()] = (new_sock, threading.Lock(), [])
        
    def disconnect_client(self, name, error=None):
        if error:
            msg = str(name) + " has exited -- " + error + "\r\n"
        else:
            msg = str(name) + " has exited\r\n"
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
        # this function is called and executed in the handle_client thread
        # TODO check data here?
        _, lock, data_list = self.clients[peer_name]
        with lock:  # acquire the lock
            data_list.append(data)

    def run(self):
        # send data continuously
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
                                    other_sock = self.clients[other_name][0]
                                    other_sock.send(datum)
                            self.clients[name] = (sock, lock, [])  # empty the data list


def handle_client(client_sock):
    # a server thread that receives data from each client_sock
    global dataHandler
    print "server.py/handle_client"
    peer_name = client_sock.getpeername()
    print "Got connection from ", peer_name
    msg = str(peer_name) + " has joined\r\n"
    dataHandler.write_data(peer_name, msg)

    while True:
        # check for and send any new messages
        try:
            data = client_sock.recv(net_constants.BUFFER_SIZE)  # TODO recvall?
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
        is_command = False
        client_stays = True
        for command in commands.commands:
            if data.startswith(command):
                # calling the corresponding command function
                client_stays = commands.commands[command](dataHandler, peer_name)
                is_command = True
                break

        if not client_stays:  # client exits, end the thread
            break

        if not is_command:  # received actual data
            dataHandler.write_data(peer_name, data)  # TODO add info about sender of data

        """
        if data.startswith('/name'):
            # TODO
            old_name = peer_name
            peer = data.replace('/name', '', 1).strname()
            if len(peer):
                dataHandler.write_data(peer_name, "%s now goes by %s\r\n" % (str(old_name), str(peer_name)))
            else:
                peer_name = old_name

        elif data.startswith('/quit'):
            bye = data.replace('/quit', '', 1).strname()
            if len(bye):
                msg = "%s is leaving now -- %s\r\n" % (str(peer_name), bye)
            else:
                msg = "%s is leaving now\r\n" % (str(peer_name))
            dataHandler.write_data(peer_name, msg)  # TODO unnecessary?
            dataHandler.disconnect_client(peer_name)
            break

        else:  # received actual data
            dataHandler.write_data(peer_name, "Message from %s:\r\n\t%s\r\n" % (str(peer_name), data))
        """


if __name__ == '__main__':
    print "server.py/__main__"

    # Set up the socket.
    connection_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection_sock.bind((net_constants.host, net_constants.PORT))
    connection_sock.listen(net_constants.SOCKET_BACKLOG)

    # Start the dataHandler
    dataHandler = DataHandler()  # global
    dataHandler.start()

    while True:
        print "Waiting for Connections"
        try:
            clientSock, clientAddr = connection_sock.accept()
            print "client accepted"
            # set a timeout so it won't block forever on socket.recv().
            # Clients that are not doing anything check for new messages 
            # after each timeout.
            clientSock.settimeout(net_constants.SERVER_SOCKET_TIMEOUT)
        except KeyboardInterrupt:
            # shutdown - force the threads to close by closing their socket
            connection_sock.close()
            dataHandler.disconnect_all()
            break
        #except:
        #    traceback.print_exc()
        #    continue

        dataHandler.add_client(clientSock)
        # start a handle_client thread for each client
        clientHandler = threading.Thread(target=handle_client, args=(clientSock,))
        clientHandler.setDaemon(True)
        clientHandler.start()
