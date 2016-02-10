'''
Server controls the experimental process
'''
import os
import socket
import threading
from openexp.keyboard import keyboard

#setting experiment variables
my_canvas = canvas()
my_canvas.text('<b>Hit the space bar to start simultaneous recording...</b>')
my_canvas.show()

key_press = keyboard(exp, keylist=['space'])
key, end_time = key_press.get_key()
self.experiment.set('response', key)


# Sending a trigger
HOST = "35.2.2.134" # set to IP address of target computer
PORT = 13000
addr = (HOST, PORT)
TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
	if self.experiment.get('response') == 'space':
		data = "1"
		TCPSock.send(data)
		break


