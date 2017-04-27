'''
    file tools
'''
import os


class cfile:
    def __init__(self):
        pass

    @staticmethod
    def create(path):
        pass

    @staticmethod
    def write(path, str, mode="w"):
        f = open(path, mode)
        f.write(str)
        f.close()


    @staticmethod
    def read(path, mode="r"):
        if not os.path.isfile(path):
            return ""

        f = open(path, mode)
        str = f.read()
        f.close()

        return str


class TFFile:
    '''
        thread safe file
    '''
    def __init__(self, name, mode=None, buffering=None):
        self
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
