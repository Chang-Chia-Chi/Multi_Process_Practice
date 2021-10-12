from threading import Semaphore, Thread, Lock
from random import randint
import time

MAX_CAPACITY = 10
queue = [0] * MAX_CAPACITY
MAX_COUNT = 30

count = 0
qlock = Lock()
full = Semaphore(0)
empty = Semaphore(MAX_CAPACITY)

class Producer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        global queue, count
        for i in range(MAX_COUNT):
            empty.acquire()
            qlock.acquire()

            item = randint(0, 25)
            queue[(i + 1) % MAX_CAPACITY] = item
            print("{} produced No.{} item {}".format(self.name, i + 1, item))

            qlock.release()
            full.release()
            time.sleep(0.5)
        

class Consumer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        global queue, count
        for i in range(MAX_COUNT):
            full.acquire()
            qlock.acquire()

            item = queue[(i + 1) % MAX_CAPACITY]
            print("{} consumed No.{} item {}".format(self.name, i + 1, item))

            qlock.release()
            empty.release()
            time.sleep(0.5)

if __name__ == "__main__":
    threads = [Producer("p1"), Consumer("c1")]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
