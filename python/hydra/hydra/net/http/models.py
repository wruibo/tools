'''
    models for session request&response
'''
class Header:
    def __init__(self):
        pass

class Cookies:
    def __init__(self):
        pass

class Request:
    def __init__(self):
        pass

class Response:
    def __init__(self):
        pass

    @property
    def url(self):
        pass

    @property
    def status(self):
        pass

    @property
    def reason(self):
        pass

    @property
    def content(self):
        pass

    @content.setter
    def content(self, value):
        pass

    @property
    def content_length(self):
        pass

    @property
    def elapsed(self):
        pass

    def __str__(self):
        return "query: %s\nlength:%d, time used: %s\n%d %s\n%s" % (self.url, self.content_length, self.elapsed, self.status, self.reason, self.content)

    def __repr__(self):
        return self.__str__()
