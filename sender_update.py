while True:
	pos_tuple = eyetracker.wait_for_fixation_start()[1]	#get the fixation pos
	data = str(pos_tuple[0])+' '+str(pos_tuple[1])
	UDPSock.sendto(data, addr)
#	key, end_time = key_press.get_key()
#	self.experiment.set('goforward', key)
#	if self.experiment.get('goforward') == 'space':
#		continue
#	if self.experiment.get('goforward') == 'q':
#		data = "-999 -999"
#		UDPSock.sendto(data, addr)
#		break
