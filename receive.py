import pigpio
import time

INPUT = 4
FREQ = 4000
OUT = []

pi = pigpio.pi()

def get_values():
    for i in range(12):
        OUT.append(pi.read(INPUT))
        time.sleep(1/FREQ)
try:
    pi.setmode(INPUT, pigpio.INPUT)
    pi.set_pull_up_down(INPUT, pigpio.PUD_UP)

    pi.callback(INPUT, pigpio.FALLING_EDGE, get_values)
    print(OUT)
    pi.stop()
except KeyboardInterrupt:
    pi.stop()