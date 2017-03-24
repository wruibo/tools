import cexpt

def raise_error():
    raise cexpt.ExpUnsupportedProtocol("heh")

class obj:
    __d = None
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

class obj1:
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

def catch_error():
    try:
        raise_error()
    except Exception, e:
        print e.message
    else:
        print "no error"

if __name__ == "__main__":
    print obj(1, 2, 3)

    print dir(obj)
    print dir(obj(1, 2, 3))
    print dir(obj1(1, 2, 3))