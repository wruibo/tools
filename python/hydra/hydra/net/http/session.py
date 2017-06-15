'''
    session for http client
'''


class Session:
    def __init__(self):
        pass

    def get(self, url, params=None, **kwargs):
        pass

    def getb(self, url, params=None, **kwargs):
        pass

    def getx(self, url, params=None, **kwargs):
        pass

    def getj(self, url, params=None, **kwargs):
        pass

    def getf(self, url, path, resume=False, **kwargs):
        pass


def session():
    from .facade import SessionFromRequestsFacade
    return SessionFromRequestsFacade()