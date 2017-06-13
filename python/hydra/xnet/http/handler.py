'''
    implement handlers for urllib opener
'''
import gzip, zlib
import urllib.request

class DecompressHandler(urllib.request.BaseHandler):
    '''
        handler for decompress response content
    '''
    def __init__(self):
        pass

    def http_response(self, request, response):
        '''
            call-back after http response returned
        :param request:
        :param response: @http.client.HTTPResponse
        :return: response
        '''
        encoding = response.getheader("content-encoding")
        if encoding == "gzip":
            response.fp = gzip.GzipFile(fileobj=response.fp)
        elif encoding == "deflate":
            response.fp = zlib.decompress(response.read())
        else:
            pass

        return response

    https_response = http_response


class CookieHandler(urllib.request.BaseHandler):
    '''
        handler for process cookie
    '''
    def __init__(self):
        pass

    def http_request(self, request):
        return request

    def http_response(self, request, response):
        return response

    https_request = http_request
    https_response = http_response

defaults = (DecompressHandler(), CookieHandler())
