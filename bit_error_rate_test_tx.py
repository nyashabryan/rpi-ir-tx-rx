import pigpio
import tx
import queue
pi = pigpio.pi()

PWM = 18
OUTPUT = 14
MAIN_QUEUE = queue.Queue() 

tx.IR_TX(MAIN_QUEUE)
bits = []
# make 10000 bits to be transmitted
for i in range(5000):
    bits.append(0)
    bits.append(1)

tx.tx(bits)

# Finshed transmitting
