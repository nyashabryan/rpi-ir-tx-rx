import pigpio
import time
import queue
import threading

INPUT = 3
FREQ = 10
OUT = []

pi = pigpio.pi()
BIT_QUEUE = queue.Queue()
RX_QUEUE = queue.Queue()
PX_QUEUE = queue.Queue()
LAST_DATA = 0

TRANSMITTING = False
DATA = False
LAST_TICK = 0
ZERO_T = 0

def get_values(gpio, level, tick):
	global TRANSMITTING, ZERO_T, LAST_TICK, DATA, BIT_QUEUE
	if not TRANSMITTING:
		TRANSMITTING = True
	else:
		if DATA:
			if pigpio.tickDiff(LAST_TICK, tick) < ZERO_T * 0.73:
				BIT_QUEUE.put(1)
			else:
				BIT_QUEUE.put(0)
		if not DATA:
			ZERO_T = pigpio.tickDiff(LAST_TICK, tick)
			DATA = True
	LAST_TICK = tick

class Note:

	def __init__(self, note, volume, duration):
		self.note = note
		self.volume = volume
		self.duration = duration
	def __str__(self):
		return str(self.note) + " " + str(self.volume) + " " + str(self.duration)


def decode(bitstream):
	note = chr(int(
		str(bitstream[2])+
		str(bitstream[3])+
		str(bitstream[4])+
		str(bitstream[5])+
		str(bitstream[6])+
		str(bitstream[7])+
		str(bitstream[8])+
		str(bitstream[9]), 2
		))
	volume = int(
		str(bitstream[10])+
		str(bitstream[11])+
		str(bitstream[12])+
		str(bitstream[13])+
		str(bitstream[14])+
		str(bitstream[15])+
		str(bitstream[16])+
		str(bitstream[17]), 2
	)
	duration = int(
		str(bitstream[18])+
		str(bitstream[19])+
		str(bitstream[20])+
		str(bitstream[21])+
		str(bitstream[22])+
		str(bitstream[23])+
		str(bitstream[24])+
		str(bitstream[25]), 2
	)
	return Note(note, volume, duration)

def parity_check(bitstream):
	count = 0
	for bit in bitstream:
		if bit == 1:
			count = count + 1
	return bitstream[26] == count % 2


def process(bitstream):
	global LAST_DATA
	if bitstream[0] != 1:
		print("Header corrupt. Data discarded.")
	if bitstream[27] != 0 or bitstream[28] != 1:
		print("Tail corrupt. Data discarded.")
	if parity_check(bitstream):
		LAST_DATA = bitstream
		return decode(bitstream)
	else:
		print("Data corrupt.")
	return LAST_DATA

def IR_RX(BIT_QUEUE):
	global OUT, DATA, TRANSMITTING
	try:
		pi.set_mode(INPUT, pigpio.INPUT)
		pi.set_pull_up_down(INPUT, pigpio.PUD_UP)
		c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
		while(True):
			pass
		pi.stop()
	except KeyboardInterrupt:
		while (not RX_QUEUE.empty()):
			print(RX_QUEUE.get())
		pi.stop()

def RX_BITS(BIT_QUEUE, RX_QUEUE):
	OUT = [0]
	while True:
		while len(OUT) < 30:
			OUT.append(BIT_QUEUE.get())
		RX_QUEUE.put(OUT)
		OUT = []

def PX(RX_QUEUE, PX_QUEUE):
	while (True):
		if(not RX_QUEUE.empty()):
			bitstream = RX_QUEUE.get()
			#PX_QUEUE.put(process(bitstream))


def printing(RX_QUEUE, PX_QUEUE):
	while(True):
		if (not RX_QUEUE.empty()):
			#print("Received", RX_QUEUE.get())
			pass


if __name__ == "__main__":
	
	try:
		threads = [
			threading.Thread(target=IR_RX, args=(BIT_QUEUE,)),
			threading.Thread(target=RX_BITS, args=(BIT_QUEUE, RX_QUEUE)),
			threading.Thread(target=PX, args=(RX_QUEUE, PX_QUEUE)),
			threading.Thread(target=printing, args=(RX_QUEUE, PX_QUEUE)),
		]
		for thread in threads:
			thread.start()
		
	except KeyboardInterrupt:
		print("Quiting")
		exit()
