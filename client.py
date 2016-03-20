#!/bin/env python

"""
**File:** wxchat.py

The client application (with GUI) to go along with the chat server.
wxchat Requires wxPython.

Copyright 2009, Tim Bower: Apache Open Source License
"""

# History:
# Summer 2008 - just used putty (in Windows) for the client application.
# Focus was on the development of the server.
#
# April 2009 - Developed first graphical client using a modified graphics
#   module from book "Introduction to Programming using Python"
#   by John Zelle, which uses the TK widgets.
#
# June 2009 - For much nicer graphics, ported client to wxPython.

# Copyright 2009 Tim Bower 
# This program was developed for education purposes for the Network
# Programming Class, CMST 355, at Kansas State University at Salina.
#
# This program is licensed as Open Source Software using the Apache License,
# Version 2.0 (the "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# You are free to use, copy, distribute, and display the work, and to make
# derivative works. If you do, you must give the original author credit. The
# author specifically permits (and encourages) teachers to post, reproduce,
# and distribute some or all of this material for use in their classes or by
# their students.

import sys
import time
import random

from networking import Connection, defaulthost


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

    def getText(self):  # TODO GET EYE POSITION
        print "client.py/Client.getText"
        "Read text in from user"
        message = str(self.tempCounter)  # string.strip(self.inputWin.GetValue()) TODO
        self.tempCounter += 1
        # self.inputWin.Clear()
        # self.inputWin.SetInsertionPoint(0)
        if len(message):
            # self.add_writeWin(message + '\n')
            return message
        else:
            return ''

    def connect(self, event):
        print "client.py/Client.connect"
        """
        Button call back, may be either *Connect* or *Disconnect* (same button)
        """
        # wx.BeginBusyCursor()
        if self.isConnected:
            # a disconnect request
            name = self.getText()
            self.network.send("/quit " + name)
            # self.add_writeWin('\n')
        else:
            # a connect request
            # self.add_readWin('\n')
            # A thread to listen to the network and display messages from server
            self.network = Connection(self.host, self.connected, self.display, self.lostConnection)
            self.network.start()
            # Note: finish this up in connected

        # wx.EndBusyCursor()

    def send(self, event):
        print "client.py/Client.send"
        "*Send* button (and return key) event call back"
        if self.isConnected:
            sendData = self.getText()
            print "client_send: ", sendData
            if len(sendData):
                self.network.send(sendData)
            # else:
            #     self.add_writeWin('\n')
        # self.inputWin.SetFocus()

    def nickName(self, event):
        print "client.py/Client.nickName"
        "*Set Nick Name* button call back"
        if self.isConnected:
            name = self.getText()
            if len(name):
                self.network.send("/nick " + name)
                # self.statusBar.SetStatusText("Your Nick Name is " + name, 0)
            # else:
            #     self.add_writeWin('Enter a name to set your Nick Name\n')
        # self.inputWin.SetFocus()

    """
    def brb(self, event):
        print "client.py/Client.brb"
        "*Be Right Back* and *I'm Back* button call back"
        msg = self.getText()
        if self.here:
            # switch from here to away
            self.here = False
            self.brbBtn.SetLabel("I'm Back")
            self.net.send("/brb " + msg)
            self.statusBar.PushStatusText("Click 'I'm Back' to resume chat", 0)
            self.statusBar.PushStatusText("Your status is away", 1)
            self.nick_nameBtn.Disable()
            self.nick_nameBtn.Hide()
            self.sendBtn.Disable()
            self.sendBtn.Hide()
        else:
            # switch from away to here
            self.here = True
            self.brbBtn.SetLabel("Be Right Back")
            self.net.send("/back " + msg)
            self.statusBar.PopStatusText(0)
            self.statusBar.PopStatusText(1)
            self.nick_nameBtn.Enable()
            self.nick_nameBtn.Show()
            self.sendBtn.Enable()
            self.sendBtn.Show()
        #--
        self.inputWin.SetFocus()
    """

    def connected(self):
        print "client.py/Client.connected"
        """
        Now connected to the Chat server
        Invoked via :func:`wx.CallAfter` in :mod:`rendezvous`.
        """
        self.isConnected = True
        """
        self.connectBtn.SetLabel('Disconnect')
        self.nick_nameBtn.Enable()
        self.nick_nameBtn.Show()
        self.brbBtn.Enable()
        self.brbBtn.Show()
        self.sendBtn.Enable()
        self.sendBtn.Show()
        self.sendBtn.SetDefault()
        self.statusBar.SetStatusText(
            'Connected to a chat server', 1)
        self.statusBar.SetStatusText(
            "return or 'send' to send message", 0)
        self.add_readWin('\n\nConnected to a chat server\n\n')
        self.clear_writeWin()
        self.add_writeWin(
            "Enter a name click on 'Set Nick Name' to set your identity.\n"
            "Type a message and press return or 'Send'.\n")
        self.inputWin.SetFocus()
        """

    def display(self, msg):  # TODO DISPLAY EYE POSITION
        print "client.py/Client.display"
        # Message to display from the chat server.
        # Invoked via :func:`wx.CallAfter` in :mod:`rendezvous`.
        # self.add_readWin(msg)
        print self.tempName, msg

    def lostConnection(self, msg):
        print "client.py/Client.lostConnection"
        # We lost our connection to the chat server
        # Invoked via :func:`wx.CallAfter` in :mod:`rendezvous`.
        """
        self.connectBtn.SetLabel('Connect')
        self._not_connected()
        self.add_readWin('\n\n'+ msg)
        """
        self.network.join()

    def quit(self, event):
        print "client.py/Client.quit"
        "*Quit* button call back"
        if self.isConnected:
            self.isConnected = False
            self.network.send("/quit" + self.getText())
            self.network.join()
        # self.Close(True)

    """
    def OnExit(self, event):
        print "client.py/Client.OnExit"
        "Close the application by Destroying the object"
        if self.connected:
            self.net.send("/quit")
            self.net.join()
        self.Destroy()
    """

"""
class App(wx.App):
    def OnInit(self):
        print "client.py/App.OnInit"
        self.frame = Client(parent=None, id=-1, title='Multi-Party Chat Client')
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
"""

if __name__ == "__main__":
    print "client.py/__main__"
    # set host name from command line arguments
    # may also be set from menu selection
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = defaulthost
    # make an App object, set stdout to the console so we can see errors
    # app = App(redirect=False)
    # app.MainLoop()
    chat = Client(1, 2, 3)
    chat.connect(1)
    while True:
        chat.send(1)
        time.sleep(2)
