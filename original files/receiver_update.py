from openexp.canvas import canvas

while True:
	(data, addr) = UDPSock.recvfrom(buf)
	data = data.split()
	x = data[0]
	y = data[1]
	fixpoint = canvas(exp)  #create a canvas and draw the fixation point
	fixpoint.circle(float(x),float(y),30)
	fixpoint.show()
