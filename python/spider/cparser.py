'''
    parser for parsing hyperlink from http response
'''
import re

from clogger import logger
from chelper import Helper
from cprotocol import Protocol


class Parser:
    '''
        parser base class
    '''
    #uri filter for parsing job
    __filter = None

    def __init__(self, filter = None):
        '''
            initialize the parse instance
        :param filter: object, filter object for uri
        '''
        self.__filter = filter

    def filter(self, f = None):
        if f is not None:
            self.__filter = f
        else:
            return self.__filter

    def parse(self, uri, content):
        '''
            parse wrapper for actual @_parse method
        :param uri: object, uri for the @content
        :param content: string, content for the @url
        :return: list, list with @Uri objects
        '''
        links = []
        if self.__filter is None or self.__filter.accept(uri.url()):
            links = self._parse(uri, content)
            if links is None:
                links = []

            logger.info("parser: parsing %s, %d links parsed.", uri.url(), len(links))

            return links
        else:
            logger.info("parser: parsing %s, skipped by filter.", uri.url())

        return links

    def _parse(self, uri, content):
        '''
            method must be implemented by sub classes
        :param uri: object, uri for the @content
        :param content: string, content for the @url
        :return: list, list with @Uri objects
        '''
        logger.warning("parser: unimplemented parser method, nothing will be done.")

        return []


class AParser(Parser):
    '''
        uri parser for tag "a"
    '''
    def __init__(self):
        pass

    def _parse(self, uri, content):

        #regex for parsing "a" tag's links
        regex = re.compile(r'<a.* href="([^"]+)"[^>]*>', re.IGNORECASE)

        #links parsed
        ref, links = uri.ref(), []

        #parse links from content
        urls = regex.findall(content)
        for url in urls:
            url = Helper.combine_path(uri.url(), url)
            links.append(Protocol.Uri(url, ref))

        return links


class ImageParser(Parser):
    '''
        link parser for tag "img"
    '''
    def __init__(self):
        pass

    def _parse(self, uri, content):
        # regex for parsing "img" tag's links
        regex = re.compile(r'<img.* src="([^"]+)"[^>]*>', re.IGNORECASE)

        # links parsed
        ref, links = uri.ref(), []

        # parse links from content
        urls = regex.findall(content)
        for url in urls:
            url = Helper.combine_path(uri.url(), url)
            links.append(Protocol.Uri(url, ref))

        return links


class DefaultParser(Parser):
    '''
        default parser for parse hyperlinks from http response content
    '''
    __parsers = []

    def __init__(self, filter = None):
        Parser.__init__(self, filter)

        self.__parsers.append(AParser())
        self.__parsers.append(ImageParser())

    def _parse(self, uri, content):
        '''
            default parse method for parsing hyperlinks from response @content
        :param uri: string, request uri
        :param content: string, http response content of @uri
        :return: list, links parsed, with @Uri object in the list
        '''
        links = []

        for parser in self.__parsers:
            links += parser.parse(uri, content)

        return links


class ParserMgr:
    '''
        parser manager
    '''
    def __init__(self):
        # parsers in the manager, list of parsers
        self.__parsers = []

    def register(self, parser):
        '''
            load a new @parser with @filter for specified url into manager
        :param filter: object, Filter object for specified url to parse links
        :param parser: object, Parser object for parse links
        :return:
        '''
        self.__parsers.append(parser)

    def parse(self, uri, content):
        '''
            default parse method for parsing hyperlinks from response @content
        :param url: string, request url
        :param content: string, http response content of @url
        :return: list, links parsed, with @Link object in the list
        '''
        links = []

        for parser in self.__parsers:
            links += parser.parse(uri, content)

        return links

if __name__ == "__main__":
    from ccrawler import HttpCrawler

    uri = Protocol.Uri("https://www.caifuqiao.cn/")

    crawler = HttpCrawler()
    response = crawler.crawl(uri)
    content = response.content()

    parsermgr = ParserMgr()
    parsermgr.register(DefaultParser())

    links = parsermgr.parse(uri, content)

    for link in links:
        print link.url()