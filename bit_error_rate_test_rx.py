import pigpio
import receive
import queue
import threading 

receive.IR_RX()

def getData():
    while len(receive.OUT) < 10000:
        pass
    with open("results.txt", "a+") as f:
        for bit in receive.OUT:
            f.write(str(OUT))


if __name__ == "__main__":
    threads = [
        threading.Thread(target=receive.IR_RX),
        threading.Thread(target=getData)
    ]
    threads[0].start()
    threads[1].run()