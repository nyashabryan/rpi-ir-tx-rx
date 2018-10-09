import pigpio
import queue
import time

PWM = 18
OUTPUT = 4
DATA_OUT = 0

FREQ = 4000  # In Kbits/sec

# receive from socket.and put into a queue
main_queue =  queue.Queue()
main_queue.put("1010101")
# once queue is set, send the queue

# start pwm

def make_message(value):
	bits = []
	bits.append("1")
	bits.append(value.split())
	bits.append("1")
	return bits


def transmit(value):
	bits = make_message(value)
	for bit in bits:
		if bit == "0":
			pi.write(OUTPUT, 0)
		else:
			pi.write(OUTPUT, 1)
		time.sleep(1/FREQ)
	print("Done Transmitting")



def main():
	global pi
	try:
		pi = pigpio.pi() #  Make a pigpio object

		pi.set_mode(PWM, pigpio.OUTPUT) #  Set the mode of PWM to output

		pi.hardware_PWM(PWM, 38000, 500000) #  Start the hardware PWM at 38000Hz and 50% duty cycle

		pi.set_mode(OUTPUT, pigpio.OUTPUT)
		value = "1010101"
		transmit(value)
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
