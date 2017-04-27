'''
    lock for thread
'''

import threading


class clock:
    def __init__(self, lock):
        print "init"
        self.lock = lock

    def __enter__(self):
        print "accquire"
        self.lock.acquire()


    def __exit__(self, exc_type, exc_val, exc_tb):
        print "release"
        self.lock.release()

if __name__ == "__main__":
    lock = threading.Lock()
    lock = threading.RLock()
    with clock(lock):
        print "hello in lock"