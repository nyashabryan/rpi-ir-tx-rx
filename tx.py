import pigpio
import queue

PWM = 18

DATA_OUT = 0

# receive from socket.and put into a queue

# once queue is set, send the queue

# start pwm

def main():
    try:
        pi = pigpio.pi() #  Make a pigpio object

        pi.set_mode(PWM, pigpio.OUTPUT) #  Set the mode of PWM to output

        pi.hardware_PWM(PWM, 38000, 500000) #  Start the hardware PWM at 38000Hz and 50% duty cycle

        pi.set_mode(DATA_OUT, pigpio.OUTPUT)

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