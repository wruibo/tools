'''
    extractor for content extract from crawl response
'''

from clogger import logger

class Extractor:
    '''
        base class for all extractor
    '''
    #filter for extract job
    __filter = None

    def __init__(self, name, filter = None):
        '''
            initialize extractor instance with @filter
        :param name: string, extractor name, unique identifier for the extractor instance
        :param filter: object, @Filter for uri
        '''
        self.__name = name
        self.__filter = filter

    def name(self, n = None):
        if n is not None:
            self.__name = n
        else:
            return self.__name

    def extract(self, uri, content):
        '''
            extract wrapper for actual @_extract action
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''
        if self.__filter is None or self.__filter.accept(uri.url()):
            result = self._extract(uri, content)

            logger.info("extractor: extract data from %s, completed.", uri.url())

            return result
        else:
            logger.info("extractor: extract data form %s, skipped by filter.", uri.url())

        return None

    def _extract(self, uri, content):
        '''
            extract method must be implemented by sub class
        :param uri: object, @Uri object of content
        :param content: string, content of @uri
        :return: object, extract result object or None
        '''
        logger.warning("extractor: unimplemented extract method, nothing will be done.")

        return None


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