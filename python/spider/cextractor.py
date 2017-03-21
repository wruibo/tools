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

    def __init__(self, filter = None):
        '''
            initialize extractor instance with @filter
        :param filter: object, @Filter for uri
        '''
        self.__filter = filter

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

class ExtractorMgr(Extractor):

    def load(self, extractor):
        pass

    def extract(self, content):
        pass