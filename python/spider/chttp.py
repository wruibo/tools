'''
    http request and response data structure
'''


class Http:
    '''
        data structure used for http protocol
    '''

    class Cookie:
        def __init__(self):
            pass


    class Request:
        def __init__(self):
            pass

    class Response:
        '''
            structure for holding the http request's response
        '''
        __url = None #sring, request url
        __code = None #string, response code
        __msg = None #string, response message
        __headers = None #string list, response headers
        __content = None #string, response content

        def __init__(self, url, code, msg, headers, content):
            self.__url, self.__code, self.__msg, self.__headers, self.__content = url, code, msg, headers, content

        def getUrl(self):
            return self.__url

        def getCode(self):
            return self.__code

        def getMsg(self):
            return self.__msg

        def getHeader(self, name):
            if self.__headers is None:
                return None

            values = []
            for item in self.__headers:
                key, value = item.split(":", 1)
                key, value = key.strip(), value.strip()

                if key.lower() == name.lower():
                    values.append(value)

            return values

        def getContent(self):
            return self.__content