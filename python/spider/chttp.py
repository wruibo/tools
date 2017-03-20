'''
    http request and response data structure
'''
import cookielib

from chelper import Helper

class Http:
    '''
        data structure used for http protocol
    '''

    class Uri:
        '''
            uri class
        '''

        def __init__(self, url, ref):
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

    class Cookie:
        '''
            cookie for a session
        '''
        __cookie = None

        def __init__(self):
            self.__cookie = cookielib.CookieJar()

        def getCookie(self):
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

    class Request:
        '''
            structure for holding the http request messages
        '''
        __url = None #string, request url

        def __init__(self):
            pass

    class Response:
        '''
            structure for holding the http request's response
        '''
        __url = None #sring, request url
        __code = None #string, response code
        __msg = None #string, response message
        __headers = [] #string list, response headers
        __content = None #string, response content

        def __init__(self, url, code, msg, headers, content):
            self.__url, self.__code, self.__msg, self.__headers, self.__content = url, code, msg, headers, content

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

        def content(self, c = None):
            if c is not None:
                self.__content = c
            else:
                return self.__content