'''
    parser for parsing hyperlink from http response
'''
import re


class Link:
    '''
        link for url in the http response content
    '''
    def __init__(self, type, url, title = None):
        self.__type = type
        self.__url = url
        self.__title = title

    def type(self):
        return self.__type

    def url(self):
        return self.__url

    def title(self):
        return self.__title


class Parser:
    '''
        default parser for parse hyperlinks from http response content
    '''
    #url type of the parser to parse
    __type = None
    #url filter regex pattern for filter
    __filter = None
    #link parse regex pattern for parsing the url with @__type
    __pattern = None

    # dictionary, parsers index by the url regex pattern, like:
    # {pattern1:[parser1, parser2, ...], pattern1:[parser1, parser2, ...]}
    __parsers = []

    def __init__(self, type = None, pattern = None, filter = None):
        self.__type = type

        if pattern is not None:
            self.__pattern = re.compile(pattern, re.IGNORECASE)

        if filter is not None:
            self.__filter = re.compile(pattern, re.IGNORECASE)

    @staticmethod
    def default():
        '''
            generate a default parser object for links parser
        :return:
        '''
        parser = Parser()

        parser.addParser(Parser("href", ur'<a.* href="([^"]+)"[^>]*>'))
        parser.addParser(Parser("img", ur'<img.* src="([^"]+)"[^>]*>'))

        return parser

    def addPattern(self, type, pattern, filter = None):
        '''
            add link parse @pattern for @type content link, url match @filter will be ignored
        :param pattern: string, link parsing regex pattern
        :param filter: string,  ignored url pattern
        :return:
        '''
        self.__parsers.append(Parser(type, pattern, filter))

    def addParser(self, parser):
        '''
          add a @parser for url @pattern
        :param parser: object, parser object
        :return:
        '''
        self.__parsers.append(parser)

    def parse(self, url, content):
        '''
            default parse method for parsing hyperlinks from response @content
        :param url: string, request url
        :param content: string, http response content of @url
        :param charset: string, http response content charset, if None charset parsed from content will be used
        :return: list, links parsed, with @Link object in the list
        '''

        baseurl = self.baseurl(url)

        links = []

        if self.__pattern is not None:
            #parse links use self parse pattern
            result = self.__pattern.findall(content)
            for link in result:
                if link.startwith(u'/'):
                    link = baseurl + link
                links.append(Link(self.__type, link))

        for parser in self.__parsers:
            links = links + parser.parse(url, content)

        return links

    @staticmethod
    def baseurl(url):
        '''
            parse base url from @url
        :param url: string, base url will be parsed from
        :return: string, base url of @url
        '''
        regex = re.compile(ur'(^[^/]+//[^/]+/?)', re.IGNORECASE)
        result = regex.search(url)
        if (result):
            url = result.group(1)
            if (url[-1] != u'/'):
                url += u'/'
            return url
        return None

