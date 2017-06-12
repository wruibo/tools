'''
    extractor for content extract from crawl response
'''

from clauncher import Launcher

from .cfilter import WhiteListFilter
from .chelper import Helper
from .util.log import Logger


class Extractor(Launcher):
    '''
        base class for all extractor
    '''
    def __init__(self, workdir, name = "extractor"):
        '''
            initialize extractor instance with @filter
        :param name: string, extractor name, unique identifier for the extractor instance
        '''
        Launcher.__init__(self, workdir, name)

    def launch(self):
        '''
            launch extractor
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._launch)
            Logger.info("extractor: launch extractor - %s, time used: %fs", self.name(), time_used)
        except IOError as e:
            pass
        except Exception as e:
            Logger.info("extractor: launch extractor - %s, error: %s", self.name(), e.message)

    def persist(self):
        '''
            persist extractor data
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._persist)
            Logger.info("extractor: persist extractor - %s, time used: %fs", self.name(), time_used)
        except Exception as e:
            Logger.info("extractor: persist extractor - %s, error: %s", self.name(), e.message)

    def shutdown(self):
        '''
            shutdown extractor
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._shutdown)
            Logger.info("extractor: shutdown extractor - %s, time used: %fs", self.name(), time_used)
        except Exception as e:
            Logger.info("extractor: shutdown extractor - %s, error: %s", self.name(), e.message)

    def filter(self, *cond):
        self._filter(*cond)

    def accept(self, uri):
        return self._accept(uri)

    def extract(self, uri, content):
        '''
            extract data from content
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''
        if not self.accept(uri):
            return None

        time_used, result = Helper.timerun(self._extract, uri, content)

        Logger.info("extractor: extract data from: %s, extracted. time used: %fs", uri.url(), time_used)

        return result

    def _launch(self):
        Logger.warning("extractor: unimplemented launch method.")

    def _persist(self):
        Logger.warning("extractor: unimplemented persist method.")

    def _shutdown(self):
        Logger.warning("extractor: unimplemented shutdown method.")

    def _filter(self, *cond):
        Logger.warning("extractor: unimplemented filter method.")

    def _accept(self, uri):
        Logger.warning("extractor: unimplemented accept method.")

    def _extract(self, uri, content):
        Logger.warning("extractor: unimplemented extract method.")


class TextExtractor(Extractor):
    '''
        example for extract text from response content
    '''

    def __init__(self, workdir, name = "text extractor"):
        Extractor.__init__(self, workdir, name)

        self.__filter = WhiteListFilter(workdir, "white list filter")

    def _launch(self):
        self.__filter.launch()

    def _persist(self):
        self.__filter.persist()

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

    def persist(self):
        for extractor in self.__extractors:
            extractor.persist()

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
    def default(workdir = "./extractor", name = "exractor manager"):
        extractor_manager = ExtractorMgr(workdir, name)

        text_extractor = TextExtractor(workdir)
        text_extractor.filter(".*")

        extractor_manager.register(text_extractor)

        return extractor_manager

if __name__ == "__main__":
    from cprotocol import Uri

    crawler_manager = CrawlerMgr.default("/tmp/spider/crawler")

    uri = Uri("http://news.xinhuanet.com/world/2017-03/23/c_1120683317.htm")
    resp = crawler_manager.crawl(uri)

    extractor_manager = ExtractorMgr.default("/tmp/spider/extractor")

    extractor_manager.launch()

    result = extractor_manager.extract(uri, resp.content())

    extractor_manager.shutdown()
