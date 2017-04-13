'''
    pipe class
'''


class Pipe:
    def __init__(self):
        self.pipes = []

    def join(self, pipe):
        self.pipes.append(pipe)

    def feed(self, obj):
        pass

    def fetch(self):
        pass