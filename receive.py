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
			print(pigpio.tickDiff(LAST_TICK, tick))
			if pigpio.tickDiff(LAST_TICK, tick) < ZERO_T * 0.8:
				OUT.append(1)
			else:
				OUT.append(0)
		if not DATA:
			ZERO_T = pigpio.tickDiff(LAST_TICK, tick)
			DATA = True
			print(ZERO_T)
	LAST_TICK = tick


def parity_check(bitstream):
	count = 0
	for bit in bitstream:
		if bit == 1:
			count = count + 1
	return bitstream[26] == count % 2


def process(bitstream):
	if bitstream[0] != 0 or bitstream[1] != 1:
		print("Header corrupt. Data discarded.")
	if bitstream[27] != 0 or bitstream[28] != 1:
		print("Tail corrupt. Data discarded.")
	if parity_check(bitstream):
		LAST_DATA = bitstream
		return bitstream
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
			MAIN_QUEUE.join(process(OUT))
			TRANSMITTING = False
			DATA = False
			c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	pi.stop()
except KeyboardInterrupt:
	pi.stop()
exit()
