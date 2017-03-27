'''
    extractor for content extract from crawl response
'''
import time

from clogger import logger
from clauncher import Launcher
from cfilter import WhiteListFilter


class Extractor(Launcher):
    '''
        base class for all extractor
    '''
    def __init__(self, workdir, name):
        '''
            initialize extractor instance with @filter
        :param name: string, extractor name, unique identifier for the extractor instance
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

    def extract(self, uri, content):
        '''
            extract wrapper for actual @_extract action
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''

        results = []
        if self.accept(uri):
            stime = time.time()
            results = self._extract(uri, content)
            etime = time.time()

            logger.info("%s: extract data from %s completed. time used: %fs", self.name(), uri.url(), etime-stime)
        else:
            logger.info("%s: extract data form %s, skipped by filter.", self.name(), uri.url())

        return results

    def _launch(self):
        logger.warning("extractor: unimplemented launch method, nothing will be done.")

    def _shutdown(self):
        logger.warning("extractor: unimplemented shutdown method, nothing will be done.")

    def _filter(self, *cond):
        logger.warning("extractor: unimplemented filter method, nothing will be done.")

    def _accept(self, uri):
        logger.warning("extractor: unimplemented accept method, default not accepted.")
        return False

    def _extract(self, uri, content):
        '''
            extract method must be implemented by sub class
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''
        logger.warning("extractor: unimplemented extract method, nothing will be done.")

        return None


class TextExtractor(Extractor):
    '''
        example for extract text from response content
    '''

    def __init__(self, workdir, name = "text_extractor"):
        Extractor.__init__(self, workdir, name)

        self.__filter = WhiteListFilter(workdir, "filter")

    def _launch(self):
        self.__filter.launch()

    def _shutdown(self):
        self.__filter.shutdown()

    def _filter(self, *cond):
        self.__filter.filter(*cond)

    def _accept(self, uri):
        return self.__filter.accept(uri.url())

    def _extract(self, uri, content):
        import re

        text = ""
        pattern = re.compile(r">([^<>]*)<", re.IGNORECASE)
        results = pattern.findall(content)
        for result in results:
            text += result

        return text


class ExtractorMgr(Launcher):
    '''
        extractor manager for extractors
    '''
    def __init__(self, workdir, name = "extractor_manager"):
        Launcher.__init__(self, workdir, name)

        #array for holding all extractors for response content
        self.__extractors = []

    def launch(self):
        for extractor in self.__extractors:
            extractor.launch()

    def shutdown(self):
        for extractor in self.__extractors:
            extractor.shutdown()

    def register(self, extractor):
        '''
            register an @extractor into manager for extracting data from response content
        :param extractor: object, @Extractor object
        :return:
        '''
        self.__extractors.append(extractor)

    def extract(self, uri, content):
        '''
            extract data from content by using extractors
        :param uri: object, @Uri object of content
        :param content: string, response content of @uri
        :return: list, extracted data as tuple(extractor name, data object) or None
        '''
        results = []
        for extractor in self.__extractors:
            result = extractor.extract(uri, content)
            results += result

        return results

    @staticmethod
    def default(workdir = "./extractor", name = "exractor_manager"):
        extractor_manager = ExtractorMgr(workdir, name)

        text_extractor = TextExtractor(workdir)
        text_extractor.filter(".*")

        extractor_manager.register(text_extractor)

        return extractor_manager

if __name__ == "__main__":
    from ccrawler import *
    from cprotocol import Uri

    crawler_manager = CrawlerMgr.default("/tmp/spider/crawler")

    uri = Uri("http://news.xinhuanet.com/world/2017-03/23/c_1120683317.htm")
    resp = crawler_manager.crawl(uri)

    extractor_manager = ExtractorMgr.default("/tmp/spider/extractor")

    extractor_manager.launch()

    result = extractor_manager.extract(uri, resp.content())

    extractor_manager.shutdown()
