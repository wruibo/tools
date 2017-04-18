class TestProperty:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value


def log(func):
    def aa(*args, **kwargs):
        print "log"
        func(*args, **kwargs)
    return aa

@log
def now():
    import time
    print time.time()

def fn(self, name="ena"):
    print "abc"

Hello = type('Hello', (object,), dict(hello=fn, hello1=fn))


class QueIter:
    def __init__(self, count):
        self.count = count

    def next(self):
        self.count -= 1
        if self.count == 0:
            raise StopIteration
        return self.count

class Que:
    def __init__(self):
        pass

    def __iter__(self):
        return QueIter(10)



if __name__ == "__main__":
    q = Que()
    for i in q:
        print i