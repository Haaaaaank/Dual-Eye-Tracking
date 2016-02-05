#showing the waiting message
my_canvas = canvas()
my_canvas.text('<b>Waiting for the main computer...</b>')
my_canvas.show()

# Waiting for message from main computer
import os
from socket import *
host = ""
port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)


while True:
	(data, addr) = UDPSock.recvfrom(buf)
	if data == "1": 
		break