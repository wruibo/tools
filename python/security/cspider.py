'''
    crawl security data from different source
'''
import urllib, urllib2, httplib, cutil



class Spider:
    #default client
    client = "chrome"

    #default headers of client
    headers = {
        "chrome":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ],
        "safari":[
            ("User-Agent", "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ],
        "ie":[
            ("User-Agent", "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0"),
            ("Accept", "text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8"),
            ("Accept-Encoding", "gzip, deflate")
        ]
    }

    def __init__(self, **kwargs):
        self.client = kwargs["client"] if kwargs.has_key("client") else self.client

        opener = urllib2.build_opener()

        opener.addheaders = self.headers[self.client]

        urllib2.install_opener(opener)

    def get(self, url):
        conn = urllib2.urlopen(url)
        encoding = conn.info().get("Content-Encoding")
        content = cutil.Decompress(conn.fp, encoding)

        response = HttpResponse(conn.geturl(), conn.getcode(), conn.getmsg(), conn.info(), content)
        return response

    def post(self, url):
        pass

class SSE(Spider):
    urls = {
        "getAllStocks":"http://www.sse.com.cn/js/common/ssesuggestdataAll.js"
    }

    def getAllStocks(self):
        self.get(self.urls["getAllStocks"])


if __name__ == "__main__":

    spiderSSE = SSE(a="1")

    spiderSSE.getAllStocks()