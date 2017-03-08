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

    #vendor name
    __name = None

    #vendor platform
    __platform = None

    #vendor's key for headers dictionary
    __key = None

    #default request header for various browsers under different platform
    __headers = {
        "chrome-pc":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8")
        ],
        "safari-pc":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8")
        ],
        "ie-pc":[
            ("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8")
        ]
    }

    def __init__(self, name = "chrome", platform = "pc"):
        self.__name = name
        self.__platform = platform
        self.__key = self.__name+"-"+self.__platform

        if  not self.__headers.has_key(self.__key):
            raise Exception("unsupport browser vendor %s/%s, must be %s" % (self.__name, self.__platform, "/".join(self.__headers.keys())))

    def getName(self):
        return self.__name

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
       __cookie = cookielib.CookieJar()


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

    class DecompressHandler(urllib2.BaseHandler):
        def http_open(self, req):
            pass

        def http_request(self, req):
            '''

            :param req:
            :return:
            '''
            req.add_header("Accept-Encoding", "gzip, deflate")

            return req

        def http_response(self, req, resp):
            '''

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

        def http_error(self):
            pass

class Browser:
    '''
        browser simulator
    '''

    #browser vendor
    __vendor = None

    #cookie for browser
    __cookie = None

    def __init__(self, name, platform):
        #initialize vendor
        self.__vendor = Vendor(name, platform)
        self.__cookie = Cookie()

        #initialize the urllib2
        opener = urllib2.build_opener()

        opener.add_handler(Handler.DecompressHandler())
        opener.add_handler(urllib2.HTTPCookieProcessor())

        urllib2.install_opener(opener)

    def open(self, url, **kwargs):
        conn = urllib2.urlopen(url)
        return HttpResponse(conn.geturl(), conn.getcode(), conn.msg, conn.info().headers, conn.read())


    @staticmethod
    def create(name = "chrome", platform = "pc"):
        '''
        create a new browser object with specified vendor @name under @platform
        :param name: string, browser vendor's name, "chrome", "ie", "safari", ...
        :return: Browser, browser object
        '''
        return Browser(name, platform)


if __name__ == "__main__":
    browser = Browser.create("chrome", "pc")
    #resp = browser.open("http://www.sse.com.cn/js/common/ssesuggestdataAll.js")
    resp = browser.open("http://www.baidu.com/")

    print resp.getHeader("set-cookie")
    print resp.getContent()