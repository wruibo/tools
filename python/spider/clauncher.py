'''
    base launcher class
'''

class Launcher:
    '''
        launcher class has a working directory, and some launcher methods
    '''
    def __init__(self, workdir, name):
        self.__workdir = workdir
        self.__name = name

    def workdir(self, w=None):
        if w is not None:
            self.__workdir = w
        else:
            return self.__workdir

    def name(self, n = None):
        if n is not None:
            self.__name = n
        else:
            return self.__name

    def launch(self):
        pass

    def shutdown(self):
        pass
