'''
    model class
'''


class MetaModel(type):
    def __new__(cls, name, bases, attrs):
        return type.__new__(cls, name, bases, attrs)

    def __init__(self, *args, **kargs):
        pass


class Model(dict):
    __metaclass__ = MetaModel

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            self[key] = kwargs.get(key)

    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
