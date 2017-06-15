'''
    hydra engine module for running the spiders
'''
import threading


class Engine(threading.Thread):
    def __init__(self):
        self.spiders = []

    def start(self):
        pass

    def stop(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    from hydra.net.http import get, getx, getb, getj
    r = getx("http://www.baidu.com/")

    print(r)
