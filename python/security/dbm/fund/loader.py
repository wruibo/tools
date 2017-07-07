"""
    loader base class
"""


class Context:
    def __init__(self):
        pass

    def headers(self):
        pass

    def url(self, what):
        pass


class Loader:
    def __init__(self, context):
        self._context = context

    def headers(self):
        return self._context.headers()

    def url(self, url):
        return self._context.url(url)

    def all(self, code):
        pass

    def navs(self, code):
        pass