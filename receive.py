import pigpio
import time

INPUT = 3
FREQ = 10
OUT = []

pi = pigpio.pi()

TRANSMITTING = False
DATA = False
LAST_TICK = 0
ZERO_T = 0
ONE_T = 0

def get_values(gpio, level, tick):
	print("Detected")
	tic = time.monotonic()
	global TRANSMITTING, ZERO_T, LAST_TICK, DATA
	if not TRANSMITTING:
		TRANSMITTING = True
	else:
		if DATA:
			if pigpio.tickDiff(LAST_TICK, tick) < ZERO_T * 1.2:
				OUT.append(0)
			else:
				OUT.append(1)
		else:
			ZERO_T = pigpio.tickDiff(LAST_TICK, tick)
			DATA = True
	LAST_TICK = tick

try:
	print("In the try block")
	pi.set_mode(INPUT, pigpio.INPUT)
	pi.set_pull_up_down(INPUT, pigpio.PUD_UP)
	print("Try")
	c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	print("waiting")
	while(len(OUT)< 28):
		print(pi.read(INPUT))
		time.sleep(0.5)
	print(OUT)
	pi.stop()
except KeyboardInterrupt:
	pi.stop()
