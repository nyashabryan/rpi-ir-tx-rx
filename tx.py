import pigpio


PWM = 18

DATA_OUT = 0

# receive from socket.and put into a queue

# once queue is set, send the queue

# start pwm

pi = pigpio.pi() #  Make a pigpio object

pi.set_mode(PWM, pigpio.OUTPUT) #  Set the mode of PWM to output

pi.hardware_PWM(PWM, 38000, 500000) #  Start the hardware PWM at 38000Hz and 50% duty cycle

pi.set_mode(DATA_OUT, pigpio.OUTPUT)



