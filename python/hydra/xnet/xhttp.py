'''
    http module
'''
import os, re, gzip, zlib
import urllib.request, urllib.error, urllib.parse
from http.cookiejar import Cookie
from http.cookiejar import http2time
from http.cookiejar import MozillaCookieJar
from io import StringIO


class HttpClient:
    class ClientCookie:
        def __init__(self):
            pass

        def make(self, cookie_string):
            # split "Set-Cookie:x=y; domain=...; expires=...;..."
            set_string, tuple_string = cookie_string.split(":", 1)
            # parse version from set string
            version = self._version(set_string)

            # parse name, value from tuple string
            nv = self._name_value(tuple_string)
            # change tuple string to dict
            dict = self._dict(tuple_string)

            if nv is None or dict is None:
                return None

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
                expires = http2time(expires)

            discard = dict.get("discard", False)
            comment = dict.get("comment", None)
            comment_url = None
            rest = {}

            # create cookielib.Cookie object
            cookie = Cookie(
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

        def _version(self, set_string):
            result = re.search(r"set-cookie(\d)*", set_string, re.IGNORECASE)
            if result is not None:
                return result.group(1)
            return None

        def _name_value(self, tuple_string):
            result = re.search(r"([^=;]+)=([^=;]*)", tuple_string, re.IGNORECASE)
            if result is not None:
                return result.group(1), result.group(2)

            return None

        def _dict(self, tuple_string):
            results = re.findall(r"([^=;]+)=([^=;]*)", tuple_string, re.IGNORECASE)
            if results is not None:
                dict = {}
                for result in results:
                    dict[result[0].strip()] = result[1].strip()
                return dict

            return None

    class ClientHandler(urllib.request.BaseHandler):
        DEFAULT_HEADERS = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Accept": "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8",
            "Accept-Encoding": "gzip, deflate"
        }

        def __init__(self):
            self.headers = self.DEFAULT_HEADERS
            self.cookies = MozillaCookieJar()

        def load_cookie(self, fpath):
            self.cookies.load(fpath)

        def save_cookie(self, fpath):
            self.cookies.save(fpath)

        def set_header(self, name, value):
            self.headers[name] = value

        def set_cookie(self, cookie_string):
            cookie = self._make_cookie(cookie_string)
            if cookie:
                self.cookies.set_cookie(cookie)

        def _make_cookie(self, cookie_string):
            return HttpClient.ClientCookie().make(cookie_string)

        def _request_add_headers(self, request):
            for name, value in list(self.headers.items()):
                request.add_header(name, value)
                request.add_unredirected_header(name, value)
            return self

        def _request_add_cookies(self, request):
            self.cookies.add_cookie_header(request)

        def _response_extract_cookies(self, request, response):
            self.cookies.extract_cookies(response, request)
            return self

        def _response_decompress_content(self, request, response):
            encoding = response.headers.get("content-encoding", "")
            if encoding == "gzip":
                response.fp = gzip.GzipFile(fileobj=StringIO(response.read()))
            elif encoding == "deflate":
                response.fp = zlib.decompress(response.read())
            else:
                pass
            return self

        def http_request(self, request):
            self._request_add_headers(request)
            self._request_add_cookies(request)
            return request

        def http_response(self, request, response):
            self._response_extract_cookies(request, response)._response_decompress_content(request, response)
            return response

        https_request = http_request
        https_response = http_response


    def __init__(self):
        #working directory for http client
        self.workdir = os.getenv('HOME', "~") + "/hydra"
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        #client handler for urllib2 opener
        self.client_handler = HttpClient.ClientHandler()

        #cookie file path for http client cookies
        self.cookie_file_path = self.workdir+"/cookies"
        if os.path.exists(self.cookie_file_path):
            self.client_handler.load_cookie(self.cookie_file_path)

        #urllib2 opener as http client
        self.client = urllib.request.build_opener(self.client_handler)

    def set_cookie(self, cookie_string):
        return self.client_handler.set_cookie(cookie_string)

    def set_header(self, name, value):
        return self.client_handler.set_header(name, value)

    def get(self, url, headers=None):
        try:
            response = self.client.open(url)
            return response.getcode(), response.msg, response.headers.dict, response.read()
        except Exception as e:
            return -1, str(e.__class__.__name__)+":"+str(e), None, None

    def post(self, url, data=None, headers=None):
        try:
            response = self.client.open(url, data)
            return response.getcode(), response.msg, response.headers, response.read()
        except Exception as e:
            return -1, str(e.__class__.__name__)+":"+str(e), None, None

    def download(self, url, fpath):
        file = None
        try:
            response = self.client.open(url)
            with open(fpath, "wb") as f:
                RDSZ = 16*1024
                content = response.read(RDSZ)
                while content:
                    f.write(content)
                    content = response.read(RDSZ)
            return response.getcode(), response.msg, response.headers, fpath
        except Exception as e:
            return -1, str(e.__class__.__name__) + ":" + str(e), None, None

    def close(self):
        # create working directory
        if not os.path.exists(self.workdir):
            os.makedirs(self.workdir)

        # save cookie data of cookie handler
        self.client_handler.save_cookie(self.cookie_file_path)

#http instance for http request
client = HttpClient()

if __name__ == "__main__":
    client.set_cookie("Set-Cookie: userId=68131; expires=Tue, 04-Apr-2017 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")
    client.set_cookie("Set-Cookie: token=b5b0d334273a82053a8c50775a675690; expires=Tue, 04-Apr-2018 09:16:00 GMT; Max-Age=432000; domain=www.caifuqiao.cn; path=/")

    resp = client.download("https://ss2.baidu.com/-vo3dSag_xI4khGko9WTAnF6hhy/image/h%3D200/sign=b4d9c7399582d158a4825eb1b00819d5/aa18972bd40735fa831d0f6e97510fb30e240873.jpg", "/Users/polly/Temp/baidu.jpg")
    print(resp)

    resp = client.download("https://www.baidu.com/", "/Users/polly/Temp/baidu.html")
    print(resp)

    resp = client.download("https://www.caifuqiao.cn/Product/Detail/attachmentDownload?attachmentId=799720", "/Users/polly/Temp/caifuqiao.pdf")
    print(resp)

    client.close()