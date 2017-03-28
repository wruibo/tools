import cexpt

from chelper import Helper

def raise_error(msg):
    raise cexpt.ExpUnsupportedProtocol(msg)

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

def catch_error(msg, tt):
    try:
        raise_error(msg+tt)
    except Exception, e:
        print e.message
    else:
        print "no error"

if __name__ == "__main__":
    print Helper.timerun(catch_error, "dddd", "aa")