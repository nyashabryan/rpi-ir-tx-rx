#!usr/bin/python

from socket import *
import pigpio
import queue
import time
import threading

PWM = 18
OUTPUT = 14
DATA_OUT = 0

FREQ = 2900  # In bits/sec

serTCPsock = socket(AF_INET, SOCK_STREAM)
HOST = ''
PORT = 5005
BUFSIZE = 1024
ADDR = (HOST,PORT)

# Start the pi object
pi = pigpio.pi()

# receive from socket.and put into a queue
MAIN_QUEUE =  queue.Queue()
# once queue is set, send the queue

# start pwm
def calculate_parity(HEADER, TAIL, bitstream):
	"""
		Calculates the value of the even parity
	"""
	all_bits = HEADER + bitstream + TAIL
	count = 0
	for bit in all_bits:
		if bit == 1:
			count = count + 1
	return count % 2


def make_message(bitstream):
	HEADER = [0, 1]
	TAIL = [0, 1]
	bitstream = bitstream
	parity = calculate_parity(HEADER, TAIL, bitstream)
	bitstream.append(parity)
	return HEADER + bitstream + TAIL


def tx(bitstream):
	for bit in bitstream:
		if bit == 0:
			tick = time.monotonic()
			pi.write(OUTPUT, 1)
			while(time.monotonic()-tick < 1/FREQ):
				pass
			tick = time.monotonic()
			pi.write(OUTPUT, 0)
			while(time.monotonic()-tick < 1/FREQ * 2):
				pass
		else:
			tick = time.monotonic()
			pi.write(OUTPUT, 1)
			while(time.monotonic() - tick < 1/FREQ):
				pass
			tick = time.monotonic()
			pi.write(OUTPUT, 0)
			while(time.monotonic() - tick < 1/FREQ):
				pass

def encode(value):
	lst = []
	value = value[3:-2]
	value = value.split(",")
	a = str(bin(ord(value[0])))
	a = "0"+ a[2:]
	for ch in a:
		lst.append(eval(ch))
	b = str(bin(eval(value[1])))
	b = b[2:]
	while len(b) < 8:
		b = "0" + b
	for ch in b:
		lst.append(eval(ch))
	c = str(bin(eval(value[2])))
	c = c[2:]
	while len(c) < 8:
		c = "0" + c
	for ch in c:
		lst.append(eval(ch))
	return lst


def transmit(value):
	bitstream = encode(value)
	bitstream = make_message(bitstream)
	print("Sending", bitstream)
	tx(bitstream)


def IR_TX(MAIN_QUEUE):
	global pi
	try:
		time.sleep(5)
		pi = pigpio.pi() #  Make a pigpio object

		pi.set_mode(PWM, pigpio.OUTPUT) #  Set the mode of PWM to output

		pi.hardware_PWM(PWM, 38000, 500000) #  Start the hardware PWM at 38000Hz and 50% duty cycle

		pi.set_mode(OUTPUT, pigpio.OUTPUT)
		time.sleep(2)
		print("IR TX set up")
		while(True):
			if MAIN_QUEUE.not_empty:
				transmit(MAIN_QUEUE.get())
				time.sleep(0.3)
			
		pi.stop()
	except KeyboardInterrupt:
		pi.stop()
		exit()


def WIFI_RX(MAIN_QUEUE):
	try:
		serTCPsock.bind(ADDR)
		serTCPsock.listen(5)
		cliTCPsock,addr =serTCPsock.accept()
		print("WIFI set up at ", addr)
		while(True):
			data = ''
			data = cliTCPsock.recv(11)
			if not data:
				continue
			elif data != 'quit':
				MAIN_QUEUE.put(str(data))
			elif data=='quit':
				serTCPsock.close()
				exit()

	except KeyboardInterrupt:
		serTCPsock.close()
		exit()


def main():
	threads = [
		threading.Thread(target=IR_TX, args=(MAIN_QUEUE,)),
		threading.Thread(target=WIFI_RX, args=(MAIN_QUEUE,)),
	]
	for thread in threads:
		thread.start()

if __name__ == "__main__":
	main()
	pi.stop()
