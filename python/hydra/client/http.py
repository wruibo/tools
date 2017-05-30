import os, re, gzip, zlib
import urllib2, cookielib
from StringIO import StringIO

class HttpHandler:
    def __init__(self):
        pass

    def handle_request(self):
        pass

    def handle_response(self):
        pass

    def handle_error(self):
        pass


class HttpClients:
    def __init__(self):
        pass


class HttpClient:
    def __init__(self):
        #working directory for http client
        self.workdir = os.getenv('HOME', "~") + "/hydra"
        #cookie file path for http client cookies
        self.cookie_file_path = self.workdir+"/cookies"

        #initialize handlers
        self.header_handler = HeaderHandler()
        self.cookie_handler = CookieHandler()
        self.decompress_handler = DecompressHandler()

        #urllib2 opener as http client
        self.opener = None

        import threading
        threading.Thread

    def create(self):
        '''
            create a http client instance using urllib2
        :return: http client instance
        '''
        #create the workdir if not exist
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

        #load cookie data for cookie handler
        if os.path.exists(self.cookie_file_path):
            self.cookie_handler.load(self.cookie_file_path)

        #build the opener with urllib2
        self.opener = urllib2.build_opener(self.header_handler, self.cookie_handler, self.decompress_handler)

        #return self
        return self

    def open(self, url):
        try:
            response = self.opener.open(url)
            content = response.read()
        except Exception, e:
            return Response(url, "exception", str(e.__class__.__name__)+":"+str(e))
        else:
            return Response(url, response.getcode(), response.msg, response.headers, content)

    def get(self, url, headers=None, handler=None):
        '''
            get url
        :param url:
        :param headers:
        :param handler:
        :return:
        '''
        try:
            if handler is None:
                client = self.opener.open(url,)
        except Exception, e:
            pass
        else:
            pass

    def post(self, url, data=None, headers=None, handler=None):
        pass

    def download(self, url, fpath):
        file = None
        try:
            file = open(fpath, "wb")
            response = self.opener.open(url)
            content = response.read(16*1024)
            while content:
                file.write(content)
                content = response.read(16*1024)
        except Exception, e:
            return Response(url, "exception", str(e.__class__.__name__) + ":" + str(e))
        else:
            return Response(url, response.getcode(), response.msg, response.headers, fpath)
        finally:
            if file is not None:
                file.close()

    def set_cookie(self, cookie_string):
        return self.cookie_handler.set(cookie_string)

    def set_header(self, name, value):
        return self.header_handler.set(name, value)

    def destroy(self):
        #create working directory
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        #save cookie data of cookie handler
        self.cookie_handler.save(self.cookie_file_path)

class Cookie:
    def __init__(self):
        pass

    @staticmethod
    def create(cookie_string):
        try:
            #split "Set-Cookie:x=y; domain=...; expires=...;..."
            set_string, tuple_string = cookie_string.split(":", 1)
            #parse version from set string
            version = Cookie._version(set_string)

            #parse name, value from tuple string
            nv = Cookie._name_value(tuple_string)
            #change tuple string to dict
            dict = Cookie._dict(tuple_string)

            if nv is None or dict is None:
                raise Exception("invalid cookie string: " + cookie_string)

            name, value = nv
            port = dict.get("port", None)
            port_specified = port is not None

            domain = dict.get("domain", None)
            domain_specified = domain is not None
            domain_initial_dot = False
            if domain is not None:
                domain_initial_dot = domain.startswith(".")

            path = dict.get("path", None)
            path_specified = path is not None

            secure = dict.get("secure", False)
            expires = dict.get("expires", None)
            if expires is not None:
                expires = cookielib.http2time(expires)

            discard = dict.get("discard", False)
            comment = dict.get("comment", None)
            comment_url = None
            rest = {}

            #create cookielib.Cookie object
            cookie = cookielib.Cookie(
                version, name, value,
                port, port_specified,
                domain, domain_specified, domain_initial_dot,
                path, path_specified,
                secure,
                expires,
                discard,
                comment,
                comment_url,
                rest
            )

            return cookie
        except Exception, e:
            return None

    @staticmethod
    def _version(set_string):
        result = re.search(r"set-cookie(\d)*", set_string, re.IGNORECASE)
        if result is not None:
            return result.group(1)
        return None

    @staticmethod
    def _name_value(tuple_string):
        result = re.search(r"([^=;]+)=([^=;]*)", tuple_string, re.IGNORECASE)
        if result is not None:
            return result.group(1), result.group(2)

        return None

    @staticmethod
    def _dict(tuple_string):
        results = re.findall(r"([^=;]+)=([^=;]*)", tuple_string, re.IGNORECASE)
        if results is not None:
            dict = {}
            for result in results:
                dict[result[0].strip()] = result[1].strip()
            return dict

        return None


class Response:
    '''
        response of opened url by browser
    '''
    def __init__(self, url, code = "-1", message = "", headers = {}, content = ""):
        self.url = url
        self.code = code
        self.message = message
        self.headers = headers
        self.content = content

    def __str__(self):
        str = "%s\n%s %s\n" % (self.url, self.code, self.message)
        for name, value in self.headers.items():
            str += "%s:%s\n" % (name, value)
        str += "\n"+self.content

        return str

    __repr__ = __str__

    def ctype(self):
        ctype = None
        content_type = self.headers.get("content-type", None)
        # parse content type from header
        if content_type is not None:
            result = re.search(r'(\w+)/\w+;?', content_type, re.IGNORECASE)
            if result is not None:
                ctype = result.group(1).strip().lower()

        return ctype

    def ftype(self):
        ftype = None
        content_type = self.headers.get("content-type", None)
        # parse content type from header
        if content_type is not None:
            result = re.search(r'\w+/(\w+);?', content_type, re.IGNORECASE)
            if result is not None:
                ftype = result.group(1).strip().lower()

        return ftype

    def fname(self):
        fname = None
        content_disposition = self.headers.get("content-disposition", None)
        # parse content type from header
        if content_disposition is not None:
            result = re.search(r'filename=(.+);?', content_disposition, re.IGNORECASE)
            if result is not None:
                fname = result.group(1).strip().lower()

        return fname

    def charset(self):
        charset = None
        content_type = self.headers.get("content-type", None)
        # parse charset from header
        if content_type is not None:
            result = re.search(r'charset=([\w-]*)', content_type, re.IGNORECASE)
            if result is not None:
                charset = result.group(1).strip().lower()

        # parse charset from content
        if charset is None and self.content is not None:
            result = re.search(r'<meta[^>]*charset=[\'\"\s]*([\w-]*)[\'\"\s]*[^>]*>', self.content, re.IGNORECASE)
            if result is not None:
                charset = result.group(1).strip().lower()

        return charset


class HeaderHandler(urllib2.BaseHandler):
    '''
        add header for each request
    '''
    __DEFAULT_HEADERS ={
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Accept":"text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8",
        "Accept-Encoding":"gzip, deflate"
    }

    def __init__(self):
        self.headers = self.__DEFAULT_HEADERS

    def set(self, name, value):
        self.headers[name] = value
        return True

    def http_request(self, req):
        for name, value in self.headers.items():
            req.add_header(name, value)
            req.add_unredirected_header(name, value)

        return req

    https_request = http_request


class CookieHandler(urllib2.BaseHandler):
    '''
        manage cookie of browser
    '''
    def __init__(self):
        self.__cookiejar = cookielib.MozillaCookieJar()

    def load(self, filename):
        self.__cookiejar.load(filename)

    def set(self, cookie_string):
        cookie = Cookie.create(cookie_string)
        if cookie is not None:
            self.__cookiejar.set_cookie(cookie)
            return True
        else:
            return False

    def save(self, filename):
        self.__cookiejar.save(filename)

    def http_request(self, request):
        self.__cookiejar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self.__cookiejar.extract_cookies(response, request)
        return response

    https_request = http_request
    https_response = http_response


class DecompressHandler(urllib2.BaseHandler):
    '''
        decompress response content
    '''
    def __init__(self):
        pass

    def http_response(self, req, resp):
        encoding = resp.headers.get("content-encoding", "")
        if encoding == "gzip":
            fp = gzip.GzipFile(fileobj=StringIO(resp.read()))

            response = urllib2.addinfourl(fp, resp.info(), resp.geturl(), resp.getcode())
            response.msg = resp.msg

            return response
        elif encoding == "deflate":
            fp = zlib.decompress(resp.read())

            response = urllib2.addinfourl(fp, resp.info(), resp.geturl(), resp.getcode())
            response.msg = resp.msg

            return response
        else:
            return resp

    https_response = http_response

#http instance for http request
http = Http().init()

if __name__ == "__main__":
    crawler = Crawler()
    crawler.init()

    crawler.set_cookie("Set-Cookie: userId=68131; expires=Tue, 04-Apr-2017 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")
    crawler.set_cookie("Set-Cookie: token=615347353461caaf28eb4023230faa80; expires=Tue, 04-Apr-2017 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")

    resp = crawler.download("https://ss2.baidu.com/-vo3dSag_xI4khGko9WTAnF6hhy/image/h%3D200/sign=b4d9c7399582d158a4825eb1b00819d5/aa18972bd40735fa831d0f6e97510fb30e240873.jpg", "/tmp/baidu.jpg")
    print resp

    resp = crawler.download("http://www.baidu.com/", "/tmp/baidu.html")
    print resp

    resp = crawler.download("https://www.caifuqiao.cn/Product/Detail/attachmentDownload?attachmentId=799720", "/tmp/caifuqiao.pdf")
    print resp
    print resp.ctype(), resp.ftype(), resp.fname()

    crawler.destroy()