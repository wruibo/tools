'''
    browser simulator
'''

import urllib2, gzip, zlib, time
from StringIO import StringIO

from clogger import logger
from clauncher import Launcher
from cfilter import WhiteListFilter
from cprotocol import Uri, Cookie, HttpResponse


class Crawler(Launcher):
    '''
        crawler base class
    '''
    def __init__(self, workdir, name):
        '''
            initialize crawler instance
        '''
        Launcher.__init__(self, workdir, name)

    def launch(self):
        self._launch()

    def shutdown(self):
        self._shutdown()

    def filter(self, *cond):
        self._filter(*cond)

    def accept(self, uri):
        return self._accept(uri)

    def crawl(self, uri):
        '''
            crawl wrapper for @_crawl method
        :param uri: object, @Uri class object
        :return: object, crawl response content
        '''
        if self.accept(uri):

            stime = time.time()
            response = self._crawl(uri)
            etime = time.time()

            logger.info("%s: crawling %s, length: %d bytes. time used: %fs", self.name(), uri.url(), len(response.content()), etime-stime)

            return response
        else:
            logger.info("%s: crawling %s, skipped by filter.", self.name(), uri.url())

        return None

    def _launch(self):
        logger.warning("crawler: unimplemented launch method, nothing will be done.")

    def _shutdown(self):
        logger.warning("crawler: unimplemented shutdown method, nothing will be done.")

    def _filter(self, *cond):
        logger.warning("crawler: unimplemented filter method, nothing will be done.")

    def _accept(self, uri):
        logger.warning("crawler: unimplemented accept method, default not accepted.")
        return False

    def _crawl(self, uri):
        '''
            crawl method that subclass must be implemented
        :param uri: object, @Uri class object
        :return:object, crawl response content
        '''
        logger.warning("crawler: unimplemented crawl method, nothing will be done.")

        return None


class HttpCrawler(Crawler):
    '''
        crawler for url, simulate as a browser
    '''
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

    def __init__(self, workdir, name = "http_crawler", client = "chrome", platform = "pc"):
        Crawler.__init__(self, workdir, name)
        #use white list filter
        self.__filter = WhiteListFilter(workdir)

        #initialize vendor, cookie
        self.__vendor = HttpCrawler.Vendor(client, platform)
        self.__cookie = Cookie()

        #initialize the urllib2
        opener = urllib2.build_opener()

        #add special handlers
        opener.add_handler(HttpCrawler.Handler.AddHeaderHandler(self.__vendor.headers()))
        opener.add_handler(HttpCrawler.Handler.DecompressHandler())
        opener.add_handler(urllib2.HTTPCookieProcessor(self.__cookie.cookie()))

        urllib2.install_opener(opener)

    def _launch(self):
        self.__filter.launch()

    def _shutdown(self):
        self.__filter.shutdown()

    def _filter(self, *cond):
        self.__filter.filter(*cond)

    def _accept(self, uri):
        return self.__filter.accept(uri.url())

    def _crawl(self, uri):
        protocol = uri.protocol().lower()
        if protocol != "http" and protocol != "https":
            return None

        resp = HttpResponse()

        try:
            conn = urllib2.urlopen(uri.url())
        except Exception, e:
            pass
        else:
            resp = HttpResponse(conn.getcode(), conn.msg, conn.info().headers, conn.read())

        return resp


class CrawlerMgr(Launcher):
    '''
        crawler manager for all supported crawlers
    '''

    def __init__(self, workdir, name="crawler_manager"):
        Launcher.__init__(self, workdir, name)

        self.__crawlers = []

    def launch(self):
        for crawler in self.__crawlers:
            crawler.launch()

    def shutdown(self):
        for crawler in self.__crawlers:
            crawler.shutdown()

    def register(self, crawler):
        self.__crawlers.append(crawler)

    def crawl(self, uri):

        for crawler in self.__crawlers:
            resp = crawler.crawl(uri)
            if resp is not None:
                return resp

        logger.warning("crawler: there is no satisfied crawler for url: " + uri.url())
        return None

    @staticmethod
    def default(workdir = "./crawler", name = "crawler_manager"):
        crawler_manager = CrawlerMgr(workdir, name)

        http_crawler = HttpCrawler(workdir, "http_crawler")
        http_crawler.filter("^http://.*")
        crawler_manager.register(http_crawler)

        https_crawler = HttpCrawler(workdir, "https_crawler")
        https_crawler.filter("^https://.*")
        crawler_manager.register(https_crawler)

        return crawler_manager


if __name__ == "__main__":
    crawler_manager = CrawlerMgr.default("/tmp/spider/crawler")

    #url = "https://www.caifuqiao.cn/Product/List/productList?typeId=3&typeName=%E9%98%B3%E5%85%89%E7%A7%81%E5%8B%9F"
    #url = "https://docs.python.org/2/library/random.html?highlight=rand#module-random"
    url = "http://www.sse.com.cn/js/common/ssesuggestdataAll.js"
    #url = "http://www.baidu.com/"
    #url = "http://www.caifuqiao.cn/"
    #resp = crawler.open("http://www.sse.com.cn/js/common/ssesuggestdataAll.js")
    #resp = crawler.open("http://www.baidu.com/")
    resp = crawler_manager.crawl(Uri(url))

    print resp.content()
