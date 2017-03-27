'''
    parser for parsing hyperlink from http response
'''
import re, time

from clogger import logger
from chelper import Helper
from cprotocol import Uri
from clauncher import Launcher
from cfilter import WhiteListFilter


class Parser(Launcher):
    '''
        parser base class
    '''
    def __init__(self, workdir, name):
        '''
            initialize the parse instance
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

    def parse(self, uri, content):
        '''
            parse wrapper for actual @_parse method
        :param uri: object, uri for the @content
        :param content: string, content for the @url
        :return: list, list with @Uri objects
        '''
        links = []
        if self.accept(uri):
            stime = time.time()
            links = self._parse(uri, content)
            etime = time.time()

            logger.info("%s: parsing %s completed. links: %d, time used: %fs", self.name(), uri.url(), len(links), etime-stime)
        else:
            logger.info("%s: parsing %s, skipped by filter.", self.name(), uri.url())

        return links

    def _launch(self):
        logger.warning("parser: unimplemented launch method, nothing will be done.")

    def _shutdown(self):
        logger.warning("parser: unimplemented shutdown method, nothing will be done.")

    def _filter(self, *cond):
        logger.warning("parser: unimplemented filter method, nothing will be done.")

    def _accept(self, uri):
        logger.warning("parser: unimplemented accept method, default not accepted.")
        return False

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
    def __init__(self, workdir, name = "a_parser"):
        Parser.__init__(self, workdir, name)

        self.__filter = WhiteListFilter(workdir, "filter")

    def _launch(self):
        self.__filter.launch()

    def _shutdown(self):
        self.__filter.shutdown()

    def _filter(self, *cond):
        self.__filter.filter(*cond)

    def _accept(self, uri):
        return self.__filter.accept(uri.url())

    def _parse(self, uri, content):
        #regex for parsing "a" tag's links
        regex = re.compile(r'<a.* href="([^"]+)"[^>]*>', re.IGNORECASE)

        #links parsed
        links = []

        #parse links from content
        urls = regex.findall(content)
        for url in urls:
            url = Helper.combine_path(uri.url(), url)
            links.append(Uri(url, uri.url()))

        return links


class ImageParser(Parser):
    '''
        link parser for tag "img"
    '''
    def __init__(self, workdir, name = "image_parser"):
        Parser.__init__(self, workdir, name)

        self.__filter = WhiteListFilter(workdir, "filter")

    def _launch(self):
        self.__filter.launch()

    def _shutdown(self):
        self.__filter.shutdown()

    def _filter(self, *cond):
        self.__filter.filter(*cond)

    def _accept(self, uri):
        return self.__filter.accept(uri.url())

    def _parse(self, uri, content):
        # regex for parsing "img" tag's links
        regex = re.compile(r'<img.* src="([^"]+)"[^>]*>', re.IGNORECASE)

        # links parsed
        links = []

        # parse links from content
        urls = regex.findall(content)
        for url in urls:
            url = Helper.combine_path(uri.url(), url)
            links.append(Uri(url, uri.url()))

        return links


class ParserMgr(Launcher):
    '''
        parser manager
    '''
    def __init__(self, workdir, name = "parser_manager"):
        Launcher.__init__(self, workdir, name)

        # parsers in the manager, list of parsers
        self.__parsers = []

    def launch(self):
        for parser in self.__parsers:
            parser.launch()

    def shutdown(self):
        for parser in self.__parsers:
            parser.shutdown()

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

    @staticmethod
    def default(workdir, name = "parser_manager"):
        parser_manager = ParserMgr(workdir, name)

        a_parser = AParser(workdir)
        a_parser.filter(r".*")
        parser_manager.register(a_parser)

        image_parser = ImageParser(workdir)
        image_parser.filter(r".*")
        parser_manager.register(image_parser)

        return parser_manager

if __name__ == "__main__":
    from ccrawler import *
    from cprotocol import Uri

    crawler_manager = CrawlerMgr.default("/tmp/spider/crawler")

    uri = Uri("http://news.xinhuanet.com/world/2017-03/23/c_1120683317.htm")
    resp = crawler_manager.crawl(uri)

    parser_manager = ParserMgr.default("/tmp/spider/parser")
    links = parser_manager.parse(uri, resp.content())

    for link in links:
        print link.url()