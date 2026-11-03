import threading
import time


def rubbingTummy(value):
    while True:
        print("Rubbing...")
        time.sleep(value)

def pattingHead(value):
    while True:
        print("Patting...")
        time.sleep(value)

x = threading.Thread(target=rubbingTummy, args=(1,))
y = threading.Thread(target=pattingHead, args=(0.5,))

x.start()
y.start()

