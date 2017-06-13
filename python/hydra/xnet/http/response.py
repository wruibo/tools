'''
    extension for  http.client.HTTPResponse
'''


class Response:
    def __init__(self, http_response):
        self.url = None

        self.pro = None
        self.ver = None

        self.status = None
        self.reason = None

        self.headers = {}
        self.content = None

    def get_url(self):
        return self.url

    def get_protocol(self):
        return self.pro

    def get_version(self):
        return self.ver

    def get_status(self):
        return self.status

    def get_reason(self):
        self.reason

    def get_header(self, name):
        return None

    def get_content(self):
        return self.content


class HtmlResponse(Response):
    def __init__(self, http_response):
        self.url = http_response.geturl()
        self.status = http_response.getcode()
        self.headers = http_response.headers
        self.content = http_response.read()

    def __str__(self):
        pass


class FileResponse(Response):
    def __init__(self):
        pass


class ErrorResponse(Response):
    def __init__(self, exception, url):
        self.url = url
        self.status = -1
        self.reason = str(exception)

    def __str__(self):
        return self.reason