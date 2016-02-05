import os
from socket import *
from openexp.keyboard import keyboard

#setting experiment variables
my_canvas = canvas()
my_canvas.text('<b>Hit the space bar to start simultaneous recording...</b>')
my_canvas.show()

key_press = keyboard(exp, keylist=['space'])
key, end_time = key_press.get_key()
self.experiment.set('response', key)


# Sending a trigger

host = "35.2.15.136" # set to IP address of target computer
port = 13000
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
while True:
	if self.experiment.get('response') == 'space':
		data = "1"
		UDPSock.sendto(data, addr)
		break
