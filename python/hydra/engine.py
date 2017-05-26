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