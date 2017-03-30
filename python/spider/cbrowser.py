import os, re, gzip, zlib
import urllib2, cookielib
from StringIO import StringIO


class Browser:
    def __init__(self, workdir = "./browser"):
        #create working directory
        self.__workdir = workdir
        self.__cookie_file_path = workdir+"/cookies"

        #initialize handlers
        self.__header_handler = HeaderHandler()
        self.__cookie_handler = CookieHandler()
        self.__decompress_handler = DecompressHandler()

        #initialize urllib2 opener
        self.__opener = urllib2.build_opener()

    def create(self):
        #load cookie data for cookie handler
        if os.path.exists(self.__cookie_file_path):
            self.__cookie_handler.load(self.__cookie_file_path)

        #add special handlers
        self.__opener.add_handler(self.__header_handler)
        self.__opener.add_handler(self.__cookie_handler)
        self.__opener.add_handler(self.__decompress_handler)

    def open(self, url):
        try:
            response = self.__opener.open(url)
            content = response.read()
        except Exception, e:
            return Response(url, "exception", str(e.__class__.__name__)+":"+str(e))
        else:
            return Response(url, response.getcode(), response.msg, response.headers, content)

    def destroy(self):
        #create working directory
        if not os.path.exists(self.__workdir):
            os.makedirs(self.__workdir)

        #save cookie data of cookie handler
        self.__cookie_handler.save(self.__cookie_file_path)

    def set_cookie(self, cookie_string):
        return self.__cookie_handler.set(cookie_string)

    def set_header(self, name, value):
        return self.__header_handler.set(name, value)


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
        self.charset = self._charset(headers, content)

    def __str__(self):
        str = "%s\n%s %s %s\n" % (self.url, self.code, self.message, self.charset)
        for name, value in self.headers.items():
            str += "%s:%s\n" % (name, value)
        str += "\n"+self.content

        return str

    __repr__ = __str__

    def _charset(self, headers, content):
        #first find charset from response headers
        content_type = headers.get("content-type", None)
        if content_type is not None:
            result = re.search(r'charset=([\w-]*)', content_type, re.IGNORECASE)
            if result is not None:
                return result.group(1).strip().lower()

        #if charset not set in header, then find charset from response content
        if content is not None:
            result = re.search(r'<meta[^>]*charset=[\'\"\s]*([\w-]*)[\'\"\s]*[^>]*>', content, re.IGNORECASE)
            if result is not None:
                return result.group(1).strip().lower()

        #can not detect charset
        return None


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


if __name__ == "__main__":
    browser = Browser()
    browser.create()

    browser.set_cookie("Set-Cookie: userId=68131; expires=Tue, 04-Apr-2017 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")
    browser.set_cookie("Set-Cookie: token=615347353461caaf28eb4023230faa80; expires=Tue, 04-Apr-2017 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")
    resp = browser.open("https://www.caifuqiao.cn/")
    print resp

    if resp.code == "200":
        result = re.search(r'<meta[^>]*charset=[\'\"\s]*([\w-]*)[\'\"\s]*[^>]*>', resp.content, re.IGNORECASE)
        print result.group(1).strip().lower()

    browser.destroy()