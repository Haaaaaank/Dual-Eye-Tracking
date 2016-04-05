"""
    A list of available commands and corresponding server functions
    All command functions take two parameters: a dataHandler and a peer name,
    and returns false if the client exits (true otherwise)
"""
"""
    Copyright 2016 Meng Du

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
"""

import net_constants


def client_quit(data_handler, peer_name):
    msg = "%s is leaving now\r\n" % (str(peer_name))
    data_handler.write_data(peer_name, msg)  # TODO unnecessary?
    data_handler.disconnect_client(peer_name)
    return True


def start(data_handler, peer_name):
    return False


def rename(data_handler, peer_name):
    return False


commands = {net_constants.CMD_RENAME: rename, net_constants.CMD_QUIT: client_quit, net_constants.CMD_START: start}
