'''
    link database for crawling
'''
import json, time
import pickle

from clink import Link
from chttp import Http
from chelper import Helper
from cfilter import DefaultFilter
from cserializer import Serializer


class LinkDB:
    '''
        link database from crawling
    '''

    def __init__(self):
        pass

    def store(self, uri, response = None):
        '''
        store link into database
        :param uri: object, Uri object
        :param response: object, Http Response object
        :return: object, key of stored link
        '''
        pass

    def get(self, key):
        '''
            get a link object by specified key
        :return: object, Link object or None
        '''
        pass

    def next(self):
        '''
            get next link in database
        :return: object, Link object or None
        '''
        pass

    def reset(self):
        '''
             reset cursor to the first link record
        :return:
        '''
        pass


class DefaultLinkDB(LinkDB, Serializer):
    '''
        default link database using memory as self defined database
    '''
    #current cursor of link position in link list
    __cursor = 0

    #links for crawling, with Link object in the list
    __links = []

    #index for find a link in @__links, <key:md5 of url, value:index of array @__links>
    __index = {}

    def __init__(self):
        pass

    def store(self, uri, response = None):
        '''
            store the uri into database
        :param uri: object, Uri object
        :param response: object, Http Response Object
        :return: tuple, (key: key of stored uri, id: id of stored uri)
        '''
        key = Helper.md5(uri.url())

        if not self.__index.has_key(key):
            self.__links.append(Link(uri, None, None))
            self.__index[key] = len(self.__links) - 1

        id = self.__index.get(key)
        if response is not None:
            self.__links[id].add_context(Link.Context(time.time(), response.code(), response.message(), None))

        return (key, id)

    def get(self, key):
        '''
            get Link from database by specified key
        :param key: string, md5 of url
        :return: object, Link object or None
        '''
        id = self.__index.get(key, None)
        if id is not None:
            return self.__links[id]

        return None

    def next(self):
        '''
            get next link object by cursor
        :return: object, Link object or None
        '''
        if self.__cursor < len(self.__links):
            #next link
            link = self.__links[self.__cursor]

            #move cursor
            self.__cursor += 1

            return link

        return None

    def reset(self):
        '''
            reset cursor to the first link record
        :return:
        '''
        self.__cursor = 0

    def serialize(self, file):
        pass

    def unserialize(self, file):
        pass


class LinkMgr(LinkDB, Serializer):
    def __init__(self, filter = DefaultFilter(), linkdb = DefaultLinkDB()):
        # link filter for new links
        self.__filter = filter

        # link database instance for spider
        self.__linkdb = linkdb

    def filter(self, f = None):
        if f is not None:
            self.__filter = f
        else:
            return self.__filter

    def store(self, uri, response = None):
        if self.__filter.accept(uri.url()):
            self.__linkdb.store(uri, response)

    def get(self, key):
        return self.__linkdb.get(key)

    def next(self):
        return self.__linkdb.next()

    def reset(self):
        return self.__linkdb.reset()


    def serialize(self, path):
        if self.__linkdb is not None:
            self.__linkdb.serialize(Helper.combine_path(path, "links"))

        if self.__filter is not None:
            self.__filter.serialize(Helper.combine_path(path, "filter"))

    def unserialize(self, path):
        if self.__linkdb is not None:
            self.__linkdb.unserialize(Helper.combine_path(path, "links"))

        if self.__filter is not None:
            self.__filter.unserialize(Helper.combine_path(path, "filter"))


if __name__ == "__main__":
    linkmgr = LinkMgr()
    linkmgr.load()

    linkmgr.add_white_pattern("https://www.caifuqiao.cn/.*")
    linkmgr.add_black_pattern("https://www.baidu.com/.*")

    linkmgr.add(ContextLink(Link("a", "https://www.caifuqiao.cn/"), Context(3600)));
    linkmgr.add(ContextLink(Link("a", "/Index/Index/index_about#page4", "https://www.caifuqiao.cn/"), Context(3600)));

    linkmgr.serialize("/tmp/spider1/")

    print linkmgr.next().str()
    print linkmgr.next().str()

    linkmgr.serialize("/tmp/spider1/")


