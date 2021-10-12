from threading import Thread, Lock, Condition
from random import randint
import time

MAX_CAPACITY = 5
MAX_COUNT = 20
count = 0
queue = []
qlock = Lock()
has_space = Condition(qlock)
has_item = Condition(qlock)

class Producer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    
    def run(self):
        global queue
        global count
        while count <= MAX_COUNT:
            qlock.acquire()
            while len(queue) >= MAX_CAPACITY:
                print("space of queue if full! not produce new item {}".format(self.name))
                has_space.wait()
                if len(queue) >= MAX_CAPACITY:
                    print("someone has filled the queue before me! {}".format(self.name))
            
            item = chr(ord('A') + randint(0, 25))
            count += 1
            if count > MAX_COUNT:
                print("exceed max_count!")
                if len(queue) > 0:
                    has_item.notify()
                qlock.release()
                break

            print("{} produced #{} item {}".format(self.name, count, item))
            queue.append(item)
            has_item.notify()
            qlock.release()
            time.sleep(1.0)

class Consumer(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        global queue
        global count
        while count <= MAX_COUNT:
            qlock.acquire()
            while not queue and count < MAX_COUNT:
                print("{} there is no item in queue".format(self.name))
                has_item.wait()
                if not queue:
                    print("{} someone has consumed the item before me".format(self.name))

            if len(queue) > 0:
                item = queue.pop()
                print("{} consumed item {}".format(self.name, item))

            has_space.notify()
            qlock.release()
            time.sleep(1.0)

if __name__ == "__main__":
    p1 = Producer("p1")
    p2 = Producer("p2")
    p3 = Producer("p3")

    c1 = Consumer("c1")
    c2 = Consumer("c2")
    c3 = Consumer("c3")

    threads = [p1, p2, p3, c1, c2, c3]
    for th in threads:
        th.start()
        
    for th in threads:
        th.join()
