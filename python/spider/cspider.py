'''
    crawl security data from different source
'''
import time, threading

from ccrawler import *
from cparser import *
from clinkdb import *
from cstorage import *
from cextractor import *


class Spider(threading.Thread):
    '''
        spider class
    '''

    def __init__(self, name):
        threading.Thread.__init__(self)

        self.__name = name

        self.__crawler_manager = CrawlerMgr()
        self.__parser_manager = ParserMgr()
        self.__link_manager = LinkMgr()
        self.__storage_manager = StorageMgr()
        self.__extractor_manager = ExtractorMgr()

    def run(self):
        while True:
            print "run"
            import thread
            import time
            time.sleep()




class SpiderMgr:
    pass

if __name__ == "__main__":

    spider = Spider.create("abc")

    browser = Browser.default()
    parser = Parser.default()

    response = browser.open("http://www.baidu.com/")

    url = response.getUrl()
    content = response.getContent()

    links = parser.parse(url, content)

    print links