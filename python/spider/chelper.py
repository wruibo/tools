'''
    useful functions for spider
'''
import re

class Helper:
    def __init__(self):
        pass

    @staticmethod
    def charset(content):
        regex = re.compile('charset=["]*([a-zA-Z-0-9]+)["]*', re.IGNORECASE)
        result = regex.search(content)
        if result is not None:
            return result.group(1)

        return None

    @staticmethod
    def unicode(content, charset = None):
        #try to get charset of content from itself
        if charset is None:
            charset = Helper.charset(content)

        #unknown charset just return the original content
        if charset is None:
            return content

        try:
            return content.decode(charset, 'ignore')
        finally:
            return content

    @staticmethod
    def rootUrl(url):
        '''
            parse absolute path url from @url
        :param url: string, base url will be parsed from
        :return: string, base url of @url
        '''
        regex = re.compile(r'(^[^/]+//[^/]+/?)', re.IGNORECASE)
        result = regex.search(url)
        if result is not None:
            url = result.group(1)
            if (url[-1] != u'/'):
                url += u'/'
            return url
        return None

    @staticmethod
    def relativeUrl(url):
        '''
            parse current relative url from @url
        :param url: string, complete url
        :return: string, relative url parsed
        '''
        regex = re.compile(r'(.*/)[^/]+$')

        result = regex.search(url)
        if result is not None:
            return result.group(1)

        return url
