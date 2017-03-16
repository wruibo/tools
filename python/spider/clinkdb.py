'''
    link database for crawling
'''

from chelper import Helper
from cfilter import DefaultFilter
from cserializer import Serializer
from clink import Link, Context, ContextLink


class LinkDB:
    '''
        link database from crawling
    '''

    def __init__(self):
        pass

    def add(self, link):
        pass

    def next(self):
        '''
            next link to crawl
        :return: object, Link object
        '''
        pass


class DefaultLinkDB(LinkDB, Serializer):
    '''
        default link database using memory as self defined database
    '''
    #links for crawling, with ContextLink object in the list
    __links = []

    #next link position in link list
    __next = 0

    def add(self, link):
        self.__links.append(link)

    def next(self):
        if self.__next < len(self.__links):
            link = self.__links[self.__next].link()
            self.__next += 1
            return link
        return None

    def serialize(self, path):
        strs = []
        for link in self.__links:
            strs.append(link.str(","))

        Helper.write2file(path, "\n".join(strs))

    def unserialize(self, path):
        strs = Helper.readfromfile(path).split("\n")

        for str in strs:
            self.__links.append(ContextLink(str))


class LinkMgr(Serializer):
    #link database instance for spider
    __linkdb = None
    #link filter for add-in links
    __filter = None

    def __init__(self):
        pass

    def load(self, linkdb = DefaultLinkDB(), filter = DefaultFilter):
        self.__linkdb = linkdb
        self.__filter = filter

    def add(self, link):
        if self.__linkdb is None:
            return

        #only accept url will be add into the link database
        if self.__filter is not None and self.__filter.accept(link.url()):
            self.__linkdb.add(link)

    def next(self):
        if self.__linkdb is None:
            return

        return self.__linkdb.next()

    def serialize(self, path):
        if self.__linkdb is not None:
            self.__linkdb.serialize(Helper.combine_path(path, "links"))

        if self.__filter is not None:
            self.__linkdb.serialize(Helper.combine_path(path, "filter"))

    def unserialize(self, path):
        if self.__linkdb is not None:
            self.__linkdb.unserialize(Helper.combine_path(path, "links"))

        if self.__filter is not None:
            self.__linkdb.unserialize(Helper.combine_path(path, "filter"))