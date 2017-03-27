'''
    http request and response data structure
'''
import cookielib

from chelper import Helper


class Uri:
    '''
        uri class
    '''
    def __init__(self, url = "", ref = ""):
        self.__url = url
        self.__ref = ref
        self.__protocol = Helper.protocol(self.__url)

    def url(self, u=None):
        if u is not None:
            self.__url = u
        else:
            return self.__url

    def ref(self, r=None):
        if r is not None:
            self.__ref = r
        else:
            return self.__ref

    def protocol(self, p=None):
        if p is not None:
            self.__protocol = p
        else:
            return self.__protocol

    def encode(self):
        return {"url":self.__url, "ref":self.__ref, "protocol":self.__protocol}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__url = obj.get("url", self.__url)
            self.__ref = obj.get("ref", self.__ref)
            self.__protocol = obj.get("protocol", self.__protocol)
        return self


class Cookie:
    '''
        cookie for a session
    '''
    __cookie = None

    def __init__(self):
        self.__cookie = cookielib.CookieJar()

    def cookie(self):
        return self.__cookie

class Session:
    '''
        session for http
    '''
    # domain for session
    __domain = None

    # cookie for domain
    __cookies = {}

    def __init__(self):
        pass


class Response:
    '''
        base class for all sub response class
    '''
    def __init__(self, content = ""):
        '''
            initialize response instance
        :param content: string, content
        '''
        self.__content = content

    def success(self):
        return False

    def extras(self):
        return {}

    def content(self, c = None):
        if c is not None:
            self.__content = c
        else:
            return self.__content

class HttpResponse(Response):
    '''
        structure for holding the http request's response
    '''
    __headers = [] #string list, response headers

    def __init__(self, code = None, msg = "", headers = [], content = ""):
        Response.__init__(self, content)

        self.__code = code
        self.__msg = msg
        self.__headers = headers

    def success(self):
        if self.__code is not None and self.__code == "200":
            return True

        return False

    def extras(self):
        return {"code":self.__code, "msg":self.__msg, "headers":self.__headers}

    def url(self, u = None):
        if u is not None:
            self.__url = u
        else:
            return self.__url

    def code(self, c = None):
        if c is not None:
            self.__code = c
        else:
            return self.__code

    def message(self, m = None):
        if m is not None:
            self.__message = m
        else:
            return self.__message

    def header(self, name, value = None):
        if value is not None:
            if self.__headers is None:
                self.__headers = []

            self.__headers.append(name+":"+value)
        else:
            if self.__headers is None:
                return None

            values = []
            for item in self.__headers:
                key, value = item.split(":", 1)
                key, value = key.strip(), value.strip()

                if key.lower() == name.lower():
                    values.append(value)

            return values
