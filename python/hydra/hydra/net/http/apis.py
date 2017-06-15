'''
    global api methds for http request
'''

from .client import client


def get(url, params=None, **kwargs):
    return client().get(url, params, **kwargs)


def getb(url, params=None, **kwargs):
    return client().getb(url, params, **kwargs)


def getx(url, params=None, **kwargs):
    return client().getx(url, params, **kwargs)


def getj(url, params=None, **kwargs):
    return client().getj(url, params, **kwargs)


def getf(url, path, resume=False, **kwargs):
    return client().getf(url, path, resume, **kwargs)
