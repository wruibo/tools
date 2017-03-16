'''
    link data for crawling
'''
from chelper import Helper


class Link:
    '''
        link for url in the http response content
    '''
    #number for unserialize
    __ITEM_NUM = 5

    def __init__(self, tag = None, path = None, ref = None):
        self.__tag = tag
        self.__path = path
        self.__ref = ref
        self.__url = Helper.combine_path(ref, path)
        self.__protocol = Helper.protocol(self.__url)

    def tag(self, t = None):
        if t is not None:
            self.__tag = t
        else:
            return self.__tag

    def path(self, p = None):
        if p is not None:
            self.__path = p
        else:
            return self.__path

    def ref(self, r = None):
        if r is not None:
            self.__ref = r
        else:
            return self.__ref

    def url(self, u = None):
        if u is not None:
            self.__url = u
        else:
            return self.__url

    def protocol(self, p = None):
        if p is not None:
            self.__protocol = p
        else:
            return self.__protocol

    def str(self, spliter = ",", s = None):
        if s is not None:
            objs = Helper.objsplit(spliter, s)
            if len(objs) == self.__ITEM_NUM:
                self.__protocol, self.__tag, self.__ref, self.__path, self.__url = objs
        else:
            return Helper.strjoin(spliter, self.__protocol,  self.__tag, self.__ref, self.__path, self.__url)

class Context:
    '''
        crawl context for link
    '''
    #number for unserialize context records
    __ITEM_NUM = 4

    def __init__(self):
        self.__crawled = False  # crawled flag
        self.__crawledtm = None  # last crawled timestamp
        self.__interval = None  # crawl interval in seconds
        self.__next_crawltm = None # next crawl timestamp

    def crawled(self, flag = None):
        if flag is not None:
           self.__crawled = flag
        else:
            return self.__crawled

    def crawltm(self, tm = None):
        if tm is not None:
            self.__crawledtm = tm

            #update next crawl timestamp
            if self.__interval is not None:
                self.__next_crawltm = self.__crawledtm + self.__interval
        else:
            return self.__crawledtm

    def interval(self, seconds = None):
        if seconds is not None:
            self.__interval = seconds

            #update next crawl timestamp
            if self.__crawledtm is not None:
                self.__next_crawltm = self.__crawledtm + self.__interval
        else:
            return self.__interval

    def next_crawltm(self, tm = None):
        if tm is not None:
            self.__next_crawltm = tm
        else:
            return self.__next_crawltm

    def str(self, spliter = ",", s = None):
        if s is not None:
            objs = Helper.objsplit(spliter, s)
            if len(objs) == self.__ITEM_NUM:
                self.__crawled, self.__crawledtm, self.__interval, self.__next_crawltm = objs
        else:
            return Helper.strjoin(spliter, self.__crawled, self.__crawledtm, self.__interval, self.__next_crawltm)


class ContextLink:
    '''
        context link for link database
    '''

    def __init__(self, link = Link(), context = Context()):
        self.__link = link
        self.__context = context

    def link(self, l = None):
        if l is not None:
            self.__link = l
        else:
            return self.__link

    def context(self, c = None):
        if c is not None:
            self.__context = c
        else:
            return self.__context

    def str(self, spliter = "|", s = None):
        if s is not None:
            strs = s.split(spliter)
            if len(strs) == 2:
                self.__link.str(",", strs[0])
                self.__context.str(",", strs[1])
        else:
            return spliter.join([self.__link.str(","), self.__context.str(",")])