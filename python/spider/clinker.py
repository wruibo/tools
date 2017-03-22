'''
    link database for crawling
'''
import re, sys, json, time, pickle

from clogger import logger
from cprotocol import Http
from chelper import Helper
from clauncher import Launcher
from cfilter import DefaultFilter
from cserializer import Serializer


class CConfig:
    def __init__(self, origin=False, retry_count=1, crawl_period=sys.maxint):
        '''
            initialize link crawl configure
        :param origin: boolean, where the link is origin link
        :param retry_count: int, retry count when crawl failed
        :param crawl_period: int, crawl period in seconds
        '''
        self.__origin = origin  # origin link flag
        self.__retry_count = retry_count  # retry count when crawl failed
        self.__crawl_period = crawl_period  # crawl period in seconds for next crawl action

    def origin(self, o=None):
        if o is not None:
            self.__origin = o
        else:
            return self.__origin

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

    def encode(self):
        return {"origin":self.__origin, "retry_count":self.__retry_count, "crawl_period":self.__crawl_period}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__origin = bool(obj.get("origin", self.__origin ))
            self.__retry_count = int(obj.get("retry_count", self.__retry_count))
            self.__crawl_period = int(obj.get("crawl_period", self.__crawl_period))


class PConfig:
    '''
        pattern of url with its related configure
    '''
    def __init__(self, pattern = None, config = None):
        self.config(pattern, config)

    def get(self, uri):
        if self.__cpattern.match(uri.url()):
            return self.__config
        else:
            return None

    def config(self, pattern, config):
        self.__pattern = pattern
        self.__cpattern = re.compile(pattern, re.IGNORECASE)
        self.__config = config

    def encode(self):
        return {"pattern":self.__pattern, "config":self.__config.encode()}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__pattern = str(obj.get("pattern", self.__pattern))
            self.__config = CConfig()
            self.__config.decode(obj.get("config", self.__config))



class CContext:
    '''
        crawl context for link
    '''

    def __init__(self, uri, tm, **extras):
        '''
            initialize context of link for a crawl action
        :param tm: int, unix timestamp for context
        :param extras: dict, extras message for context
        '''
        self.__uri = uri
        self.__tm = tm
        self.__extras = extras

    def uri(self, u = None):
        if u is not None:
            self.__uri = u
        else:
            return self.__uri

    def tm(self, t = None):
        if t is not None:
            self.__tm = t
        else:
            return self.__tm

    def extras(self, **e):
        if e is not None:
            self.__extras = e
        else:
            return self.__extras

    def encode(self):
        return {"uri":self.__uri.encode(), "tm":self.__tm, "extras":self.__extras}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__uri = Protocol.Uri()
            self.__uri.decode(obj.get("uri", self.__uri.encode()))

            self.__tm = int(obj.get("tm", self.__tm))
            self.__extras = obj.get("extras", self.__extras)
            if not isinstance(self.__extras, dict):
                self.__extras = {}


class CLink:
    '''
        crawl link class for spider
    '''
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
        self.__contexts += contexts

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

    def contexts(self, *c):
        if len(c) > 0:
            self.__contexts += c
        else:
            return self.__contexts

    def last_context(self):
        if len(self.__contexts) > 0:
            return self.__contexts[-1]
        return None


class Linker(Launcher):
    '''
        linker who manage crawl links from spider
    '''
    def __init__(self, name, workdir, filter = DefaultFilter()):
        '''
            initialize linker instance with a url filter
        :param name: string, linker name, an unique identifier
        :param filter: object, @Filter object for filter uri before push to linker
        :param configs: list, PatternConfig objects in list
        '''
        Launcher.__init__(self, name, workdir)

        self.__filter = filter
        self.__configs = configs


    def filter(self, f = None):
        if f is not None:
            self.__filter = f
        else:
            return self.__filter

    def configs(self, *cs):
        if len(cs) > 0:
            self.__configs.append(cs)
        else:
            return self.__configs

    def config(self, uri):
        #find the matched configure for uri
        for cfg in self.__configs:
            if cfg.match(uri):
                return cfg.config()

        #default configure for uri returned
        return Link.Config()

    def push(self, uri, **extras):
        '''
            push a uri into link database
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return: object, key of stored link
        '''
        key = None

        if self.__filter is None or self.__filter.accept(uri.url()):
            key = self._push(uri, **extras)
            logger.info("linker: push link %s, completed.", uri.url())
        else:
            logger.info("linker: push link %s, skipped by filter.", uri.url())

        return key

    def get(self, key):
        '''
            get a link object by specified key
        :return: object, Link object or None
        '''
        link = self._get(key)

        if link is not None:
            logger.info("linker: get link: %s, fetched.", link.uri.url())
        else:
            logger.info("linker: get link: none, no more links.")


        return link

    def reset(self):
        '''
             reset cursor to the first link record
        :return:
        '''
        self.reset()

        logger.info("linker: reset linker. next link cursor will be moved to head.")

    def next(self):
        '''
            get next link in database
        :return: object, Link object or None
        '''
        link = self.next()

        if link is not None:
            logger.info("linker: next link: %s, fetched.", link.uri.url())
        else:
            logger.info("linker: next link: none, no more links.")

        return link

    def _push(self, uri, **extras):
        '''
            push a uri into link database, subclass must implement this method
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return: object, key of stored link
        '''
        logger.warning("linker: unimplemented push method, nothing will be done.")

    def _get(self, key):
        '''
            get a link object by specified key
        :return: object, Link object or None
        '''
        logger.warning("linker: unimplemented get method, nothing will be done.")

        return None

    def _reset(self):
        '''
             reset cursor to the first link record
        :return:
        '''
        logger.warning("linker: unimplemented reset method, nothing will be done.")

    def _next(self):
        '''
            get next link in database
        :return: object, Link object or None
        '''
        logger.warning("linker: unimplemented next method, nothing will be done.")

        return None


class HttpLinker(Linker):
    '''
        default link database using memory as self defined database
    '''
    #current cursor of link position in link list
    __cursor = 0

    #links for crawling, with Link object in the list
    __links = []

    #index for find a link in @__links, <key:md5 of url, value:index of array @__links>
    __indexs = {}

    #crawl configure for specified uri pattern
    __configs = {}

    def __init__(self, filter = None, configs = []):
        '''
            initialize linker instance with @filter
        :param filter: object, Filter object
        '''
        Linker.__init__(self, "http/https", filter, configs)

    def _push(self, uri, **extras):
        '''
            store the uri into database
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return: string, key of uri
        '''
        key = Helper.md5(uri.url())

        if not self.__index.has_key(key):
            #new link for linker
            self.__links.append(Link(uri, self.config(uri), Link.Context(time.time(), **extras)))
            self.__index[key] = len(self.__links) - 1
        else:
            #old link for linker
            id = self.__index.get(key)
            self.__links[id].add_context(Link.Context(time.time(), **extras))

        return key

    def _get(self, uri):
        '''
            get Link from database by specified uri
        :param uri: object, Uri object
        :return: object, Link object or None
        '''
        key = Helper.md5(uri.url())
        id = self.__index.get(key, None)
        if id is not None:
            return self.__links[id]

        return None

    def _reset(self):
        '''
            reset cursor to the first link record
        :return:
        '''
        self.__cursor = 0

    def _next(self):
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

    def serialize(self, file):
        data = {"name":self.name(), "filter":self.filter(), "configs":self.configs(), "cursor":self.__cursor, "links":self.__links, "index":self.__index}
        pickle.dump(data, open(file, "w"))

    def unserialize(self, file):
        data = pickle.load(open(file, "r"))

        self.name(data["name"])
        self.filter(data["filter"])
        self.configs(data["configs"])

        self.__cursor = data["cursor"]
        self.__links = data["links"]
        self.__index = data["index"]


class LinkerMgr(Serializer):
    '''
        linker manager for manage linker instance, there is only not more than one linker instance in manager
    '''
    def __init__(self, workdir):
        # link database instance for spider
        self.__workdir = workdir
        self.__linker = None

    def start(self):
        pass

    def stop(self):
        pass

    def register(self, linker):
        '''
            load @linker into linker manager, replace current linker
        :param linker: object, linker to be loaded
        :return: object, old linker or None
        '''
        old = self.__linker

        self.__linker = linker
        if self.__linker is not None:
            logger.info("linker manager: load new linker %s.", self.__linker.name())
        else:
            if old is None:
                logger.warning("linker manager: linker is none, nothing loaded.")
            else:
                logger.warning("linker manager: linker is none, old linker %s is unloaded.", old.name())

        return old

    def push(self, uri, **extras):
            return self.__linker.push(uri, **extras)

    def get(self, key):
        return self.__linker.get(key)

    def reset(self):
        self.__linker.reset()

    def next(self):
        return self.__linker.next()

if __name__ == "__main__":
    from cprotocol import Protocol

    filter = DefaultFilter()
    filter.patterns("http://www.baidu.com/.*", "black_pattern2", "black_pattern3")

    configs = [Link.PatternConfig("pattern1", Link.Config(True, 3, 3600)), Link.PatternConfig("pattern2", Link.Config(False, 1))]
    linker = HttpLinker(filter, configs)

    linker_manager = LinkerMgr(linker)
    linker_manager.push(Protocol.Uri("http://www.baidu.com/1"), code=200, message="OK")
    linker_manager.push(Protocol.Uri("http://www.baidu.com/2"), code=404, message="Not Found")
    linker_manager.push(Protocol.Uri("http://www.baidu.com/4"), code=501, message="Internal Server Error")


    linker_manager.serialize("/tmp/spider1/links")

    linker_manager1 = LinkerMgr(HttpLinker())
    linker_manager1.unserialize("/tmp/spider1/links")


