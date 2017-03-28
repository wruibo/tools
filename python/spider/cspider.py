'''
    crawl security data from different source
'''
import time, json, threading

from ccrawler import *
from cparser import *
from clinker import *
from cstorage import *
from cextractor import *
from clauncher import *


class Spider(threading.Thread, Launcher):
    '''
        spider class, schedule the linker manager, crawler manager, parser manager, extractor manager
    '''

    def __init__(self, workdir, name = "spider"):
        threading.Thread.__init__(self)
        Launcher.__init__(self, workdir, name)

        module_workdir = workdir+"/"+name

        self.__linker_manager = LinkerMgr(module_workdir, "linker")
        self.__crawler_manager = CrawlerMgr(module_workdir, "crawler")
        self.__parser_manager = ParserMgr(module_workdir, "parser")
        self.__extractor_manager = ExtractorMgr(module_workdir, "extractor")

        self.__stop = True
        self.__stopped = True

        self.__last_persist_time = time.time()

        self.config()

    def config(self, **kwargs):
        self.__crawl_interval = kwargs.get("crawl_interval", 3)
        self.__idle_time = kwargs.get("idle_time", 5)

    def register(self, obj):
        if isinstance(obj, Linker):
            self.__linker_manager.register(obj)
        elif isinstance(obj, Crawler):
            self.__crawler_manager.register(obj)
        elif isinstance(obj, Parser):
            self.__parser_manager.register(obj)
        elif isinstance(obj, Extractor):
            self.__extractor_manager.register(obj)
        else:
            pass

    def push(self, uri):
        self.__linker_manager.push(uri)

    def launch(self):
        self.__linker_manager.launch()
        self.__crawler_manager.launch()
        self.__parser_manager.launch()
        self.__extractor_manager.launch()

        self.__stop = False
        self.start()

        self.__last_persist_time = time.time()

    def persist(self):
        if self.__last_persist_time + 10 < time.time():
            self.__linker_manager.persist()
            self.__crawler_manager.persist()
            self.__parser_manager.persist()
            self.__extractor_manager.persist()

    def shutdown(self):
        self.__extractor_manager.shutdown()
        self.__parser_manager.shutdown()
        self.__crawler_manager.shutdown()
        self.__linker_manager.shutdown()

        self.__stop = True
        self.join()

    def stopped(self):
        return self.__stopped

    def run(self):
        #set the stopped flag to false
        self.__stopped = False

        #get next link need crawling
        uri = self.__linker_manager.pull()
        while not self.__stop:
            #check if has more link
            if uri is not None:
                #crawl the link
                resp = self.__crawler_manager.crawl(uri)

                # update link context
                self.__linker_manager.update(uri, resp.extras())

                #parse new links
                links = self.__parser_manager.parse(uri, resp.content())

                #add new links to linker
                for link in links:
                    self.__linker_manager.push(link)

                #extract content
                data = self.__extractor_manager.extract(uri, resp.content())

                time.sleep(self.__crawl_interval)
            else:
                time.sleep(self.__idle_time)

            #persist spider data
            self.persist()

            #process next link
            uri = self.__linker_manager.pull()


        #set the stopped flag to true
        self.__stopped = True


class SpiderMgr(threading.Thread, Launcher):
    '''
        spider manager
    '''
    __SPIDERS_FILE_NAME = "spiders"

    def __init__(self, workdir, name = "spiders"):
        threading.Thread.__init__(self)
        Launcher.__init__(self, workdir, name)

        self.__spiders = []

        self.__stop = True
        self.__stopped = True

    def register(self, spider):
        self.__spiders.append(spider)

    def spider(self, name):
        for spider in self.__spiders:
            if spider.name() == name:
                return spider

        return None

    def spiders(self):
        return self.__spiders

    def launch(self):
        #load all spiders
        try:
            if Helper.exists(self.workdir(), self.__SPIDERS_FILE_NAME):
                fspiders = Helper.open(self.workdir(), self.__SPIDERS_FILE_NAME, "r")

                spiders = json.load(fspiders)

                if isinstance(spiders, list):
                    for spider in spiders:
                        if isinstance(spider, dict):
                            workdir = spider.get("workdir", None)
                            name = spider.get("name", None)

                            if workdir is not None and name is not None:
                                spider = Spider(workdir, name)
                                self.__spiders.append(spider)

                fspiders.close()
        except Exception, e:
            logger.error("spider manager: launch error: %s", e.message)
        else:
            logger.info("spider manager: load spiders, %d spiders launched.", len(self.__spiders))
        finally:
            pass

        #start all spiders
        for spider in self.__spiders:
            spider.launch()

        #start spider manager thread
        self.__stop = False
        self.start()

    def persist(self):
        pass

    def shutdown(self):
        #shutdown all spiders
        try:
            fspiders = Helper.open(self.workdir(), self.__SPIDERS_FILE_NAME, "w")

            spiders = []
            for spider in self.__spiders:
                spiders.append({"workdir":spider.workdir(), "name":spider.name()})

            json.dump(spiders, fspiders)

            fspiders.close()

        except Exception, e:
            logger.error("spider manager: shutdown error: %s", e.message)
        else:
            logger.info("spider manager: shutdown finished, %d spiders shutdown.", len(self.__spiders))
        finally:
            pass

        #shutdown all spiders
        for spider in self.__spiders:
            spider.shutdown()

        #stop spider manager thread
        self.__stop = True
        self.join()

    def run(self):
        self.__stopped = False

        while not self.__stop:
            time.sleep(10)

        self.__stopped = True

if __name__ == "__main__":
    spider = Spider("/tmp/spiders/caifuqiao")

    linker = DefaultLinker(spider.workdir(), "linker")
    linker.filter(".*")

    crawler = HttpCrawler(spider.workdir(), "crawler")
    crawler.filter(".*")

    parser = AParser(spider.workdir(), "parser")
    parser.filter(".*")

    extractor = TextExtractor(spider.workdir(), "extractor")
    extractor.filter(".*")

    spider.register(linker)
    spider.register(crawler)
    spider.register(parser)
    spider.register(extractor)

    spider.push(Uri("https://www.caifuqiao.cn/"))


    spider_manager = SpiderMgr("/tmp/spiders")
    spider_manager.register(spider)
    spider_manager.launch()


    while True:
        time.sleep(10)

    spider_manager.shutdown()
