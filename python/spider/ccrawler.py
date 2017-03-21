'''
    browser simulator
'''

import urllib2, cookielib, gzip, zlib
from StringIO import StringIO

from clogger import logger
from cprotocol import Http
from chelper import Helper


class Crawler:
    '''
        crawler base class
    '''
    #uri filter for crawling job
    __filter = None

    def __init__(self, filter = None):
        '''
            initialize crawler instance with uri filter
        :param filter:
        '''
        self.__filter = filter

    def filter(self, f = None):
        if f is not None:
            self.__filter = f
        else:
            return self.__filter

    def crawl(self, uri):
        '''
            crawl wrapper for @_crawl method
        :param uri: object, @Uri class object
        :return: object, crawl response content
        '''
        if self.__filter is None or self.__filter.accept(uri.url()):
            response = self._crawl(uri)

            logger.info("crawler: crawling %s, response content length: %d bytes.", uri.url(), len(response.content()))

            return response
        else:
            logger.info("crawler: crawling %s, skipped by filter.", uri.url())

        return None

    def _crawl(self, uri):
        '''
            crawl method that subclass must be implemented
        :param uri: object, @Uri class object
        :return:object, crawl response content
        '''
        logger.warning("crawler: unimplemented crawl method, nothing will be done.")

        return None


class HttpCrawler(Crawler):
    class Vendor:
        '''
            vendor for various simulate browsers
        '''

        # vendor client
        __client = None

        # vendor platform
        __platform = None

        # vendor's key for headers dictionary
        __key = None

        # default request header for various simulate browsers under different platform
        __headers = {
            "chrome-pc": [
                ("User-Agent",
                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
                ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
                ("Accept-Encoding", "gzip, deflate")
            ],
            "safari-pc": [
                ("User-Agent",
                 "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"),
                ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
                ("Accept-Encoding", "gzip, deflate")
            ],
            "ie-pc": [
                ("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"),
                ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
                ("Accept-Encoding", "gzip, deflate")
            ]
        }

        def __init__(self, client="chrome", platform="pc"):
            self.__client = client
            self.__platform = platform
            self.__key = self.__client + "-" + self.__platform

            if not self.__headers.has_key(self.__key):
                raise Exception("unsupport browser vendor %s/%s, must be %s" % (
                self.__client, self.__platform, "/".join(self.__headers.keys())))

        def client(self):
            return self.__client

        def platform(self):
            return self.__platform

        def headers(self):
            return self.__headers[self.__key]

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


    '''
        crawler for url, simulate as a browser
    '''
    #browser vendor
    __vendor = None

    #cookie for browser
    __cookie = None

    def __init__(self, client = "chrome", platform = "pc", filter = None):
        Crawler.__init__(self, filter)

        #initialize vendor
        self.__vendor = HttpCrawler.Vendor(client, platform)
        self.__cookie = Http.Cookie()

        #initialize the urllib2
        opener = urllib2.build_opener()

        #add special handlers
        opener.add_handler(HttpCrawler.Handler.AddHeaderHandler(self.__vendor.headers()))
        opener.add_handler(HttpCrawler.Handler.DecompressHandler())
        opener.add_handler(urllib2.HTTPCookieProcessor(self.__cookie.cookie()))

        urllib2.install_opener(opener)

    def _crawl(self, uri):
        protocol = uri.protocol().lower()
        if protocol != "http" and protocol != "https":
            return None

        conn = urllib2.urlopen(uri.url())
        return Http.Response(conn.getcode(), conn.msg, conn.info().headers, conn.read())


class CrawlerMgr:
    '''
        crawler manager for all supported crawlers
    '''

    def __init__(self):
        self.__crawlers = {}

    def load(self, protocol, crawler):
        self.__crawlers[protocol.lower()] = crawler

    def crawl(self, uri):
        protocol = uri.protocol().lower()

        crawler = self.__crawlers.get(protocol, None)
        if not crawler:
           logger.warning("crawler: unsupported protocol: " + protocol + ", url: " + uri.url())

        return crawler.crawl(uri)




if __name__ == "__main__":
    crawler_manager = CrawlerMgr()
    crawler_manager.load("http", HttpCrawler())
    crawler_manager.load("https", HttpCrawler())

    #url = "https://www.caifuqiao.cn/Product/List/productList?typeId=3&typeName=%E9%98%B3%E5%85%89%E7%A7%81%E5%8B%9F"
    #url = "https://docs.python.org/2/library/random.html?highlight=rand#module-random"
    url = "http://www.baidu.com/"
    #url = "http://www.caifuqiao.cn/"
    #resp = crawler.open("http://www.sse.com.cn/js/common/ssesuggestdataAll.js")
    #resp = crawler.open("http://www.baidu.com/")
    resp = crawler_manager.crawl(Http.Uri(url))
