'''
    crawl security data from different source
'''
import time, threading

from ccrawler import *
from cparser import *
from clinker import *
from cstorage import *
from cextractor import *
from clauncher import *


class Spider(threading.Thread, Launcher):
    '''
        spider class
    '''

    def __init__(self, name, workdir):
        Launcher.__init__(name, workdir)
        threading.Thread.__init__(self)

        self.__name = name

        self.__crawler_manager = CrawlerMgr()
        self.__parser_manager = ParserMgr()
        self.__linker_manager = LinkerMgr()
        self.__storage_manager = StorageMgr()
        self.__extractor_manager = ExtractorMgr()

    def launch(self):
        pass

    def shutdown(self):
        pass

    def run(self):

        #get next link may be need crawling
        link = self.__link_manager.next()
        while link is not None:
            #base information of current link
            uri = link.uri()
            config = link.config()
            context = link.last_context()

            #check if current link need crawling
            if self.need_crawl(config, context):
                self.__crawler_manager.crawl(uri)

            #process next link
            link = self.__link_manager.next()


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