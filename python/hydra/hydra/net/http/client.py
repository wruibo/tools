'''
    client for http request
'''
from .session import session


class Client:
    def __init__(self):
       self.session = session()

    def get(self, url, params=None, **kwargs):
        return self.session.get(url, params, **kwargs)

    def getb(self, url, params=None, **kwargs):
        return self.session.getb(url, params, **kwargs)

    def getx(self, url, params=None, **kwargs):
        return self.session.getx(url, params, **kwargs)

    def getj(self, url, params=None, **kwargs):
        return self.session.getj(url, params, **kwargs)

    def getf(self, url, path, resume=False, **kwargs):
        return self.session.getf(url, path, resume, **kwargs)


#default global client
_global_default_client = Client()


def client():
    return _global_default_client
