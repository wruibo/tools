'''
    parser for parsing hyperlink from http response
'''
import re

from chelper import Helper
from clink import Link

class Parser:
    '''
        parser base class
    '''

    def __init__(self):
        pass

    def parse(self, url, content):
        '''
        method must be implemented by sub classes
        :param url: string, url for the @content
        :param content: string, content for the @url
        :return: list, list with @Link objects
        '''
        pass


class AParser(Parser):
    '''
        link parser for tag "a"
    '''
    def __init__(self):
        pass

    def parse(self, url, content):

        #regex for parsing "a" tag's links
        regex = re.compile(r'<a.* href="([^"]+)"[^>]*>', re.IGNORECASE)

        #links parsed
        ref, links = url, []

        #parse links from content
        urls = regex.findall(content)
        for url in urls:
            links.append(Link("a", url, ref))

        return links


class ImageParser(Parser):
    '''
        link parser for tag "img"
    '''
    def __init__(self):
        pass

    def parse(self, url, content):
        # regex for parsing "img" tag's links
        regex = re.compile(r'<img.* src="([^"]+)"[^>]*>', re.IGNORECASE)

        # links parsed
        ref, links = url, []

        # parse links from content
        urls = regex.findall(content)
        for url in urls:
            links.append(Link("img", url, ref))

        return links


class DefaultParser(Parser):
    '''
        default parser for parse hyperlinks from http response content
    '''
    __parsers = []

    def __init__(self):
        self.__parsers.append(AParser())
        self.__parsers.append(ImageParser())

    def parse(self, url, content):
        '''
            default parse method for parsing hyperlinks from response @content
        :param url: string, request url
        :param content: string, http response content of @url
        :return: list, links parsed, with @Link object in the list
        '''
        links = []

        for parser in self.__parsers:
            links += parser.parse(url, content)

        return links


class ParserMgr(Parser):
    #parsers in the manager, list of (filter, parser)
    __parsers = []

    def __init__(self):
        pass

    def load(self, parser = DefaultParser(), filter = None):
        '''
            load a new @parser with @filter for specified url into manager
        :param filter: object, Filter object for specified url to parse links
        :param parser: object, Parser object for parse links
        :return:
        '''
        self.__parsers.append((parser, filter))

    def parse(self, url, content):
        '''
            default parse method for parsing hyperlinks from response @content
        :param url: string, request url
        :param content: string, http response content of @url
        :return: list, links parsed, with @Link object in the list
        '''
        links = []

        for parser, filter in self.__parsers:
            if filter is None or filter.accept(url):
                links += parser.parse(url, content)

        return links

if __name__ == "__main__":
    from ccrawler import Browser

    url = "https://www.caifuqiao.cn/"

    browser = Browser.create()

    response = browser.open(url)

    content = response.getContent()

    parsermgr = ParserMgr()
    parsermgr.load()

    links = parsermgr.parse(url, content)

    for link in links:
        print link.tag()+":"+link.url()