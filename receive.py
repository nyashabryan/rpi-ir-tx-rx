import pigpio
import time

INPUT = 3
FREQ = 100
OUT = []

pi = pigpio.pi()

TRANSMITTING = False
DATA = False
LAST_TICK = 0
ZERO_T = 0
ONE_T = 0

def get_values(gpio, level, tick):
	global TRANSMITTING, ZERO_T, LAST_TICK
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
	LAST_TICK = tick

try:
	pi.set_mode(INPUT, pigpio.INPUT)
	pi.set_pull_up_down(INPUT, pigpio.PUD_UP)

	c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	while(len(OUT)< 28):
		pass
	print(OUT)
	pi.stop()
except KeyboardInterrupt:
	pi.stop()
