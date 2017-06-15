'''
    facades for wrapping requests
'''
import requests

from .models import Response
from .session import Session


class SessionFromRequestsFacade(Session):
    def __init__(self):
        self.session = requests.session()

    def get(self, url, params=None, **kwargs):
        return self.getx(url, params, **kwargs)

    def getb(self, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        response = self.session.request('get', url, params=params, **kwargs)
        return ResponseDataFromRequestsFacade(response)

    def getx(self, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        response = self.session.request('get', url, params=params, **kwargs)
        return ResponseTextFromRequestsFacade(response)

    def getj(self, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        response = self.session.request('get', url, params=params, **kwargs)
        return ResponseJsonFromRequestsFacade(response)

    def getf(self, url, path, resume=False, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        response = self.session.request('get', url, **kwargs)
        return ResponseFileFromRequestsFacade(response, path, resume)


class ResponseFromRequestFacade(Response):
    def __init__(self, response):
        self.response = response

    @property
    def url(self):
        return self.response.url

    @property
    def status(self):
        return self.response.status_code

    @property
    def reason(self):
        return self.response.reason

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def content_length(self):
        return len(self._content)

    @property
    def elapsed(self):
        return self.response.elapsed


class ResponseDataFromRequestsFacade(ResponseFromRequestFacade):
    def __init__(self, response):
        ResponseFromRequestFacade.__init__(self, response)
        with response as r:
            self.content = r.content


class ResponseTextFromRequestsFacade(ResponseFromRequestFacade):
    def __init__(self, response):
        ResponseFromRequestFacade.__init__(self, response)
        with response as r:
            self.content = r.text


class ResponseJsonFromRequestsFacade(ResponseFromRequestFacade):
    def __init__(self, response):
        ResponseFromRequestFacade.__init__(self, response)
        with response as r:
            self.content = r.json()


class ResponseFileFromRequestsFacade(ResponseFromRequestFacade):
    def __init__(self, response, path=None, resume=None):
        ResponseFromRequestFacade.__init__(self, response)
        with response as r:
            self.content = self.hold_file(r, path, resume)

    def hold_file(self, response, path, resume):
        import os, sys
        if os.path.exists(path) and not os.path.isfile(path):
            pass
        else:
            with open(path, 'wb') as f:
                while True:
                    chunk = response.iter_content(2**16)
                    if chunk:
                        f.write(chunk)
                    else:
                        break