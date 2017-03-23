'''
    extractor for content extract from crawl response
'''

from clogger import logger
from clauncher import Launcher
from cfilter import DefaultFilter

class Extractor(Launcher):
    '''
        base class for all extractor
    '''
    def __init__(self, workdir, name):
        '''
            initialize extractor instance with @filter
        :param name: string, extractor name, unique identifier for the extractor instance
        '''
        Launcher.__init__(workdir, name)


    def accept(self, *cond):
        self._accept(*cond)

    def match(self, uri):
        return self._match(uri)

    def extract(self, uri, content):
        '''
            extract wrapper for actual @_extract action
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''
        if self.match(uri):
            result = self._extract(uri, content)

            logger.info("extractor: extract data from %s, completed.", uri.url())

            return result
        else:
            logger.info("extractor: extract data form %s, skipped by filter.", uri.url())

        return None

    def _accept(self, *cond):
        pass

    def _match(self, uri):
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
    def __init__(self, workdir, name):
        Extractor.__init__(workdir, name)

        self.__filter = DefaultFilter()

    def _accept(self, *cond):
        self.__filter.accept(*cond)

    def _match(self, uri):
        return not self.__filter.filter(uri.url())

    def _extract(self, uri, content):
        pass


class ImageExtractor(Extractor):
    def __init__(self, workdir, name):
        Extractor.__init__(workdir, name)

        self.__filter = DefaultFilter()

    def _accept(self, *cond):
        self.__filter.accept(*cond)

    def _match(self, uri):
        return not self.__filter.filter(uri.url())

    def _extract(self, uri, content):
        pass

class ExtractorMgr:
    '''
        extractor manager for extractors
    '''
    def __init__(self):
        #array for holding all extractors for response content
        self.__extractors = []

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
        result = []
        for extractor in self.__extractors:
            data = extractor.extract(uri, content)
            if data is not None:
                result.append((extractor.name(), data))

        return result