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
    __clinks = []

    #next link position in link list
    __next = 0

    def add(self, clink):
        self.__clinks.append(clink)

    def next(self):
        if self.__next < len(self.__clinks):
            #fetch current link
            link = self.__clinks[self.__next].link()

            #move position to next link
            self.__next += 1

            return link

        return None

    def update(self, idx, code, tm):
        pass

    def serialize(self, path):
        strs = []
        for link in self.__clinks:
            strs.append(link.str(","))

        Helper.write2file(path, "\n".join(strs))

    def unserialize(self, path):
        strs = Helper.readfromfile(path).split("\n")

        for str in strs:
            self.__clinks.append(ContextLink(str))


class LinkMgr(Serializer):
    #link database instance for spider
    __linkdb = None
    #link filter for add-in links
    __filter = None

    def __init__(self):
        pass

    def load(self, linkdb = DefaultLinkDB(), filter = DefaultFilter()):
        self.__linkdb = linkdb
        self.__filter = filter

    def add_white_pattern(self, pattern):
        self.__filter.add_white_pattern(pattern)

    def add_black_pattern(self, pattern):
        self.__filter.add_black_pattern(pattern)

    def add(self, clink):
        '''
            add ContextLink object @link into linkd database
        :param link: object, ContextLink object
        :return:
        '''
        if self.__linkdb is None:
            return

        #only accept url will be add into the link database
        if self.__filter is not None and self.__filter.accept(clink.link().url()):
            self.__linkdb.add(clink)

    def next(self):
        if self.__linkdb is None:
            return

        return self.__linkdb.next()

    def update(self, idx, code, tm):
        pass

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


