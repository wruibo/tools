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
        if (result):
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
