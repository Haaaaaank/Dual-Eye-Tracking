import os
import socket

#showing the waiting message
my_canvas = canvas()
my_canvas.text('<b>Waiting for the main computer...</b>')
my_canvas.show()

# Waiting for message from main computer
HOST = ""
PORT = 13000
BUFF = 1024
addr = (HOST, PORT)
TCPSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPSock.bind(addr)

while True:
	data = TCPSock.recv(BUFF)
	if data == "1": 
		break
