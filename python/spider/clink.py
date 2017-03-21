'''
    link data for crawling
'''
import sys

from chelper import Helper


class Link:
    '''
        link class for spider
    '''

    class Config:
        def __init__(self, retry_count = 1, crawl_period = sys.maxint):
            '''
                initialize link crawl configure
            :param retry_count: int, retry count when crawl failed
            :param crawl_period: int, crawl period in seconds
            '''
            self.__retry_count = retry_count  # retry count when crawl failed
            self.__crawl_period = crawl_period  # crawl period in seconds for next crawl action

        def retry_count(self, rc=None):
            if rc is not None:
                self.__retry_count = rc
            else:
                return self.__retry_count

        def crawl_period(self, cp=None):
            if cp is not None:
                self.__crawl_period = cp
            else:
                return self.__crawl_period

    class Context:
        '''
            crawl context for link
        '''

        def __init__(self, crawl_time, response_code, response_message, content_file):
            '''
                initialize context of link for a crawl action
            :param crawl_time: int, unix timestamp for the link crawl action
            :param response_code: string, http response code
            :param response_message: string, response message
            :param content_file: string, content file path
            '''
            self.__crawl_time = crawl_time
            self.__response_code = response_code
            self.__response_message = response_message
            self.__content_file = content_file

        def crawl_time(self, ct=None):
            if ct is not None:
                self.__crawl_time = ct
            else:
                return self.__crawl_time

        def response_code(self, rc=None):
            if rc is not None:
                self.__response_code = rc
            else:
                return self.__response_code

        def response_message(self, rm=None):
            if rm is not None:
                self.__response_message = rm
            else:
                return self.__response_message

        def content_file(self, cf=None):
            if cf is not None:
                self.__content_file = cf
            else:
                return self.__content_file

    def __init__(self, uri, config, *contexts):
        '''
            initialize instance with @uri, @config and its crawl @context
        :param uri: object, Uri object
        :param config: object, Config object
        :param contexts: tupple, Context object in the tupple
        '''
        self.__uri = uri
        self.__config = config

        self.__contexts = []
        if contexts is not None:
            self.__contexts.append(contexts)

    def uri(self, u = None):
        if u is not None:
            self.__uri = u
        else:
            return self.__uri

    def config(self, c = None):
        if c is not None:
            self.__config = c
        else:
            return self.__config

    def contexts(self, cs = None):
        if cs is not None:
            self.__contexts = cs
        else:
            return self.__context

    def last_context(self):
        if len(self.__contexts) > 0:
            return self.__contexts[-1]
        return None

    def add_context(self, c):
        self.__context.append(c)
