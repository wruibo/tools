'''
    browser simulator
'''

import urllib2, cookielib, gzip, zlib

from StringIO import StringIO


class HttpResponse:
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

class Vendor:
    '''
        vendor for various browsers
    '''

    #vendor client
    __client = None

    #vendor platform
    __platform = None

    #vendor's key for headers dictionary
    __key = None

    #default request header for various browsers under different platform
    __headers = {
        "chrome-pc":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ],
        "safari-pc":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ],
        "ie-pc":[
            ("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ]
    }

    def __init__(self, client = "chrome", platform = "pc"):
        self.__client = client
        self.__platform = platform
        self.__key = self.__client+"-"+self.__platform

        if  not self.__headers.has_key(self.__key):
            raise Exception("unsupport browser vendor %s/%s, must be %s" % (self.__client, self.__platform, "/".join(self.__headers.keys())))

    def getName(self):
        return self.__client

    def getPlatform(self):
        return self.__platform

    def getHeaders(self):
       return self.__headers[self.__key]


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
    #domain for session
    __domain = None

    #cookie for domain
    __cookies = {}

    def __init__(self):
        pass


class Handler:
    '''
        handler for urllib2
    '''
    def __init__(self):
        pass

    class AddHeaderHandler(urllib2.BaseHandler):
        '''
            add header handler for each request
        '''
        def __init__(self, headers):
            self.__headers = headers

        def http_request(self, req):
            '''
                add request headers
            :param req:
            :return:
            '''
            for header in self.__headers:
                req.add_header(header[0], header[1])
                req.add_unredirected_header(header[0], header[1])

            return req

        def https_request(self, req):
            return self.http_request(req)


    class DecompressHandler(urllib2.BaseHandler):
        def __init__(self):
            pass

        def http_response(self, req, resp):
            '''
                decompress the compressed response
            :param req:
            :param resp:
            :return:
            '''
            msg = resp.msg

            encoding = resp.headers.get("content-encoding")
            if encoding == "gzip":
                fp = gzip.GzipFile(fileobj=StringIO(resp.read()))
                resp = urllib2.addinfourl(fp, resp.info(), resp.geturl(), resp.getcode())
            elif encoding == "deflate":
                fp = zlib.decompress(resp.read())
                resp = urllib2.addinfourl(fp, resp.info(), resp.geturl(), resp.getcode())
            else:
                pass

            resp.msg = msg

            return resp

        def https_response(self, req, resp):
            return self.http_response(req, resp)


class Browser:
    '''
        browser simulator
    '''
    #browser vendor
    __vendor = None

    #cookie for browser
    __cookie = None

    def __init__(self, client, platform):
        #initialize vendor
        self.__vendor = Vendor(client, platform)
        self.__cookie = Cookie()

        #initialize the urllib2
        opener = urllib2.build_opener()

        #add special handlers
        opener.add_handler(Handler.AddHeaderHandler(self.__vendor.getHeaders()))
        opener.add_handler(Handler.DecompressHandler())
        opener.add_handler(urllib2.HTTPCookieProcessor(self.__cookie.getCookie()))

        urllib2.install_opener(opener)

    def open(self, url, data = None, **kwargs):

        conn = urllib2.urlopen(url, data)
        return HttpResponse(conn.geturl(), conn.getcode(), conn.msg, conn.info().headers, conn.read())

    @staticmethod
    def create(client = "chrome", platform = "pc"):
        '''
        create a new browser object with specified vendor @client under @platform
        :param name: string, browser vendor's name, "chrome", "ie", "safari", ...
        :return: Browser, browser object
        '''
        return Browser(client, platform)

if __name__ == "__main__":
    #url = "https://www.caifuqiao.cn/Product/List/productList?typeId=3&typeName=%E9%98%B3%E5%85%89%E7%A7%81%E5%8B%9F"
    #url = "https://docs.python.org/2/library/random.html?highlight=rand#module-random"
    #url = "http://www.baidu.com/"
    url = "http://www.caifuqiao.cn/"
    browser = Browser.create("chrome", "pc")
    #resp = browser.open("http://www.sse.com.cn/js/common/ssesuggestdataAll.js")
    #resp = browser.open("http://www.baidu.com/")
    resp = browser.get(url)

    print resp.getHeader("set-cookie")
    print resp.getContent()