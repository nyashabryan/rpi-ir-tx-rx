import pigpio
import queue
import time

PWM = 18
OUTPUT = 14
DATA_OUT = 0

FREQ = 10  # In Kbits/sec

# receive from socket.and put into a queue
main_queue =  queue.Queue()
main_queue.put("101001110110010000")
# once queue is set, send the queue

# start pwm

def make_message(value):
	bits = [0,1,1,0,1,0,0,1,1,1,0,1,1,0,0,1,0,0,0,0,1,0,1,0,1,0,1,0]
	return bits


def transmit(value):
	global pi
	bits = make_message(value)
	print("Starting TX")
	print(bits)
	for bit in bits:
		if bit == 0:
			pi.write(OUTPUT, 1)
			time.sleep(1)
		else:
			pi.write(OUTPUT, 0)
			time.sleep(1)
	pi.write(OUTPUT, 1)
	print("Done Transmitting")



def main():
	global pi
	try:
		time.sleep(5)
		pi = pigpio.pi() #  Make a pigpio object

		pi.set_mode(PWM, pigpio.OUTPUT) #  Set the mode of PWM to output

		pi.hardware_PWM(PWM, 38000, 500000) #  Start the hardware PWM at 38000Hz and 50% duty cycle

		pi.set_mode(OUTPUT, pigpio.OUTPUT)
		pi.write(OUTPUT, 0)
		time.sleep(2)
		print("Output going HIGH")
		value = "101010111110000111"
		#transmit(value)
		while(True):
			pass
		pi.stop()



	except KeyboardInterrupt:
		pi.stop()

main()
pi.stop()
"""
#!usr/bin/python

#Communicating with Android App
#Michael Granelli
#5 September 2018

from socket import *
import time

HOST = ''
PORT = 5005
BUFSIZE = 1024
ADDR = (HOST,PORT)

serTCPsock = socket(AF_INET, SOCK_STREAM)
serTCPsock.bind(ADDR)
serTCPsock.listen(5)
cont=1

while 1:
	print 'Waiting to be connected'
	cliTCPsock,addr =serTCPsock.accept()
	print 'Connected to:',addr
	try:
		while 1:
			data = ''
			data = cliTCPsock.recv(BUFSIZE)
			if not data:
				break
			if data!='quit':
				print data
			elif data=='quit':
				serTCPsock.close()
				exit()
				break
	except KeyboardInterrupt:
		break
serTCPsock.close()



"""
