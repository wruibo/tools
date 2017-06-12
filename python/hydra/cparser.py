'''
    parser for parsing hyperlink from http response
'''

from clauncher import Launcher

from .cfilter import WhiteListFilter
from .chelper import Helper
from .util.log import Logger


class Parser(Launcher):
    '''
        parser base class
    '''
    def __init__(self, workdir, name = "parser"):
        '''
            initialize the parse instance
        '''
        Launcher.__init__(self, workdir, name)

    def launch(self):
        '''
            launch parser
        :return:
        '''
        self._launch()

    def persist(self):
        '''
            persist parser data
        :return:
        '''
        self._persist()

    def shutdown(self):
        '''
            shutdown parser
        :return:
        '''
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
        if not self.accept(uri):
            return None

        time_used, links = Helper.timerun(self._parse, uri, content)
        Logger.info("parser: parse links: %s, parsed. links: %d, time used: %fs", uri.url(), len(links), time_used)

        return links

    def _launch(self):
        Logger.warning("parser: unimplemented launch method.")

    def _persist(self):
        Logger.warning("parser: unimplemented persist method.")

    def _shutdown(self):
        Logger.warning("parser: unimplemented shutdown method.")

    def _filter(self, *cond):
        Logger.warning("parser: unimplemented filter method.")

    def _accept(self, uri):
        Logger.warning("parser: unimplemented accept method.")

    def _parse(self, uri, content):
        Logger.warning("parser: unimplemented parser method.")


class AParser(Parser):
    '''
        uri parser for tag "a"
    '''
    def __init__(self, workdir, name = "href parser"):
        Parser.__init__(self, workdir, name)

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
    def __init__(self, workdir, name = "image parser"):
        Parser.__init__(self, workdir, name)

        self.__filter = WhiteListFilter(workdir, "filter")

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
    def __init__(self, workdir, name = "parser manager"):
        Launcher.__init__(self, workdir, name)

        # parsers in the manager, list of parsers
        self.__parsers = []

    def launch(self):
        for parser in self.__parsers:
            parser.launch()

    def persist(self):
        for parser in self.__parsers:
            parser.persist()

    def shutdown(self):
        for parser in self.__parsers:
            parser.shutdown()

    def register(self, parser):
        self.__parsers.append(parser)

    def parse(self, uri, content):
        links = []
        for parser in self.__parsers:
            links += parser.parse(uri, content)
        return links

    @staticmethod
    def default(workdir, name = "parser manager"):
        parser_manager = ParserMgr(workdir, name)

        a_parser = AParser(workdir, "href parser")
        a_parser.filter(r".*")
        parser_manager.register(a_parser)

        image_parser = ImageParser(workdir, "image parser")
        image_parser.filter(r".*")
        parser_manager.register(image_parser)

        return parser_manager

if __name__ == "__main__":
    from .ccrawler import *
    from cprotocol import Uri

    crawler_manager = CrawlerMgr.default("/tmp/spider/crawler")

    uri = Uri("http://news.xinhuanet.com/world/2017-03/23/c_1120683317.htm")
    resp = crawler_manager.crawl(uri)

    parser_manager = ParserMgr.default("/tmp/spider/parser")
    links = parser_manager.parse(uri, resp.content())

    for link in links:
        print(link.url())