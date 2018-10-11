import pigpio
import time
import queue

INPUT = 3
FREQ = 10
OUT = []

pi = pigpio.pi()
MAIN_QUEUE = queue.Queue()
LAST_DATA = 0

TRANSMITTING = False
DATA = False
LAST_TICK = 0
ZERO_T = 0

def get_values(gpio, level, tick):
	global TRANSMITTING, ZERO_T, LAST_TICK, DATA
	if not TRANSMITTING:
		TRANSMITTING = True
	else:
		if DATA:
			if pigpio.tickDiff(LAST_TICK, tick) < ZERO_T * 0.8:
				OUT.append(1)
			else:
				OUT.append(0)
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
	if bitstream[0] != 0 or bitstream[1] != 1:
		print("Header corrupt. Data discarded.")
	if bitstream[27] != 0 or bitstream[28] != 1:
		print("Tail corrupt. Data discarded.")
	if parity_check(bitstream):
		LAST_DATA = bitstream
		return decode(bitstream)
	else:
		print("Data corrupt.")
	return LAST_DATA

try:
	pi.set_mode(INPUT, pigpio.INPUT)
	pi.set_pull_up_down(INPUT, pigpio.PUD_UP)
	c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	while(True):
		if(len(OUT) < 29):
			pass
		else:
			c1.cancel()
			print("Receiving", OUT)
			#MAIN_QUEUE.join(process(OUT))
			TRANSMITTING = False
			DATA = False
			c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
			OUT = []
	pi.stop()
except KeyboardInterrupt:
	while (not MAIN_QUEUE.empty()):
		print(MAIN_QUEUE.get())
	pi.stop()
exit()
