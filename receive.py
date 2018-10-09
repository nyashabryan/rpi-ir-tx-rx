import pigpio
import time

INPUT = 3
FREQ = 100
OUT = []

pi = pigpio.pi()

def get_values(gpio, level, tick):
	global OUT, c1, pi
	print("Now receiving")
	OUT = []
	c1.cancel()
	for i in range(30):
		OUT.append(pi.read(INPUT))
		time.sleep(1/FREQ)
	print("Finished RX") 
	c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	lst = []
	for i in OUT:
		if i == 1:
			lst.append(0)
		else:
			lst.append(1)
	print(lst)
try:
	pi.set_mode(INPUT, pigpio.INPUT)
	pi.set_pull_up_down(INPUT, pigpio.PUD_UP)

	c1 = pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
	while(True):
		pass
	pi.stop()
except KeyboardInterrupt:
	pi.stop()
