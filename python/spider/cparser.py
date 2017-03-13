'''
    parser for parsing hyperlink from http response
'''
import re

from chelper import Helper

class Link:
    '''
        link for url in the http response content
    '''
    def __init__(self, tag, url, title = None):
        self.__tag = tag
        self.__url = url
        self.__title = title

    def tag(self):
        return self.__tag

    def url(self):
        return self.__url

    def title(self):
        return self.__title


class Pattern:
    '''
        regex pattern for parsing job
    '''
    __patterns = {
        "href":[
            ur'<a.* href="([^"]+)"[^>]*>'
        ],

        "img":[
            ur'<img.* src="([^"]+)"[^>]*>'
        ]
    }

    def __init__(self):
        pass

    def patterns(self):
        '''
            get the compiled patterns
        :return: dict, compiled patterns, structure like the @__patterns
        '''
        compiledPatterns = {}

        for key, regs in self.__patterns.items():
            if not compiledPatterns.has_key(key):
                compiledPatterns[key] = []
            for reg in regs:
                regex = re.compile(reg, re.IGNORECASE)
                compiledPatterns[key].append(regex)

        return compiledPatterns

class Parser:
    '''
        default parser for parse hyperlinks from http response content
    '''

    def __init__(self):
        #initialze the regex patterns for parseing url from http response content
        self.__patterns = Pattern().patterns()

    @staticmethod
    def create():
        return Parser()

    def parse(self, url, content, charset = None):
        '''
            default parse method for parsing hyperlinks from response @content
        :param url: string, request url
        :param content: string, http response content of @url
        :param charset: string, http response content charset, if None charset parsed from content will be used
        :return: list, links parsed, with @Link object in the list
        '''

        rootUrl = Helper.rootUrl(url) #root url path
        relativeUrl = Helper.relativeUrl(url) #current url path

        #parse the charset from content if needed
        if charset is None:
            charset = Helper.charset(content)

        #convert @content's charset to unicode
        content = Helper.unicode(content, charset)

        links = []

        for tag, patterns in self.__patterns.items():
            for pattern in patterns:
                urls = pattern.findall(content)
                for url in urls:
                    if  url.startswith("/"):
                        links.append(Link(tag, rootUrl+url[1:].encode(charset, 'ignore')))
                    else:
                        links.append(Link(tag, relativeUrl+url.encode(charset, 'ignore')))

        return links


if __name__ == "__main__":
    from cbrowser import Browser

    url = "https://www.caifuqiao.cn/"


    browser = Browser.create()

    response = browser.open(url)

    content = response.getContent()

    parser = Parser()

    links = parser.parse(url, content)

    for link in links:
        print link.tag()+":"+link.url()