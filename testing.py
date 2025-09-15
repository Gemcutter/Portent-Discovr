import threading
import time

def test_threading():
    time.sleep(1)
    print("Thread finished")

t = threading.Thread(target=test_threading, args=())
t.start()
t.join()