'''
    link database for crawling
'''
import re, sys, json, time

from cprotocol import Uri
from clogger import logger
from chelper import Helper
from clauncher import Launcher
from cfilter import WhiteListFilter

class CConfig:
    def __init__(self, is_origin = False, crawl_period = sys.maxint):
        '''
            initialize link crawl configure
        :param is_origin: boolean, where the link is origin link
        :param crawl_period: int, crawl period in seconds
        '''
        self.__is_origin = is_origin  # origin link flag
        self.__crawl_period = crawl_period  # crawl period in seconds for next crawl action

    def is_origin(self, o=None):
        if o is not None:
            self.__is_origin = o
        else:
            return self.__is_origin

    def crawl_period(self, cp=None):
        if cp is not None:
            self.__crawl_period = cp
        else:
            return self.__crawl_period

    def encode(self):
        return {"is_origin":self.__is_origin, "crawl_period":self.__crawl_period}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__is_origin = bool(obj.get("is_origin", self.__is_origin ))
            self.__crawl_period = int(obj.get("crawl_period", self.__crawl_period))
        return self


class PConfig:
    '''
        pattern of url with its related configure
    '''
    def __init__(self, pattern = None, config = None):
        self.__pattern = pattern
        self.__config = config
        self.__cpattern = None

        if self.__pattern is not None:
            self.__cpattern = re.compile(pattern, re.IGNORECASE)

    def match(self, uri):
        if self.__cpattern.match(uri.url()):
            return self.__config
        else:
            return CConfig()

    def config(self, pattern = None, config = None):
        if pattern is not None and config is not None:
            self.__pattern = pattern
            self.__config = config
            self.__cpattern = None

            if self.__pattern is not None:
                self.__cpattern = re.compile(pattern, re.IGNORECASE)
        else:
            return self.__config

    def pattern(self):
        return self.__pattern

    def encode(self):
        return {"pattern":self.__pattern, "config":self.__config.encode()}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__pattern = str(obj.get("pattern", self.__pattern))
            self.__config = CConfig()
            self.__config.decode(obj.get("config", self.__config))

            if self.__pattern is not None:
                self.__cpattern = re.compile(self.__pattern, re.IGNORECASE)

        return self


class PConfigs:
    def __init__(self):
        self.__configs = []

    def match(self, uri):
        for config in self.__configs:
            if config.match(uri) is not None:
                #return matched configure
                return config.config()

        #return default configure
        return CConfig()

    def add(self, pattern, config):
        for config in self.__configs:
            if pattern == config.pattern():
                #replace exists configure for @pattern
                config.config(pattern, config)
                return

        #new pattern configure
        self.__configs.append(PConfig(pattern, config))

    def encode(self):
        configs = []
        for c in self.__configs:
            configs.append(c.encode())

        return configs

    def decode(self, obj):
        #reset the configures
        self.__configs = []

        if isinstance(obj, list):
            for config in obj:

                self.__configs.append(PConfig().decode(config))

        return self


class CContext:
    '''
        crawl context for link
    '''

    def __init__(self, extras = {}):
        '''
            initialize context of link for a crawl action
        :param extras: dict, extras message for context
        '''
        self.__tm = time.time()
        self.__extras = extras

    def tm(self, t = None):
        if t is not None:
            self.__tm = t
        else:
            return self.__tm

    def extras(self, e):
        if e is not None:
            self.__extras = e
        else:
            return self.__extras

    def encode(self):
        return {"tm":self.__tm, "extras":self.__extras}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__tm = int(obj.get("tm", self.__tm))
            self.__extras = obj.get("extras", self.__extras)
            if not isinstance(self.__extras, dict):
                self.__extras = {}

        return self


class CContexts:
    def __init__(self):
        self.__contexts = []

    def add(self, *contexts):
        self.__contexts += contexts

    def last(self):
        if len(self.__contexts) > 0:
            return self.__contexts[-1]
        return None

    def encode(self):
        contexts = []
        for context in self.__contexts:
            contexts.append(context.encode())

        return contexts

    def decode(self, obj):
        #reset contexts list
        self.__contexts = []

        if isinstance(obj, list):
            for context in obj:
                self.__contexts.append(CContext().decode(context))

        return self


class CLink:
    '''
        crawl link class for spider
    '''
    def __init__(self, uri = None):
        '''
            initialize instance with @uri, @config and its crawl @context
        :param uri: object, Uri object
        '''
        self.__uri = uri
        self.__contexts = CContexts()

    def uri(self, u = None):
        if u is not None:
            self.__uri = u
        else:
            return self.__uri

    def contexts(self, *c):
        if len(c) > 0:
            self.__contexts.add(*c)
        else:
            return self.__contexts

    def encode(self):
        return {"uri":self.__uri.encode(), "contexts":self.__contexts.encode()}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__uri = Uri().decode(obj.get("uri", {}))
            self.__contexts = CContexts().decode(obj.get("contexts", []))

        return self

class CLinks:
    def __init__(self):
        # current cursor of link position in link list
        self.__cursor = 0
        #link list
        self.__links = []
        # index for find a link in @__links, <key:md5 of url, value:index of array @__links>
        self.__index = {}

    def _key(self, uri):
        '''
            generate key for @uri
        :param uri: object, @Uri object
        :return: string, md5 of url
        '''
        return Helper.md5(uri.url())

    def push(self, uri):
        '''
            push new links to linker
        :param uri:
        :return:
        '''
        key = self._key(uri)

        if not self.__index.has_key(key):
            self.__links.append(CLink(uri))
            self.__index[key] = len(self.__links) - 1

        return key


    def pull(self):
        '''
            pull a link object from link list
        :return: object, @CLink object or None
        '''
        #pull next link by cursor
        if self.__cursor < len(self.__links):
            link = self.__links[self.__cursor]
            self.__cursor += 1
            return link
        else:
            #reset cursor to head
            self.__cursor = 0

        return None

    def update(self, uri, extras):
        '''
            push an uri into the end of link list
        :param uri: object, @Uri object
        :param extras: dict, extras for uri
        :return: string, key of url
        '''
        #use url md5 as index key
        key = self._key(uri)

        if self.__index.has_key(key):
            #old link for linker
            id = self.__index.get(key)

            #update link config and context
            self.__links[id].contexts(CContext(extras))

        return key

    def encode(self):
        links = []
        for link in self.__links:
            links.append(link.encode())

        return {"cursor":self.__cursor, "links":links}

    def decode(self, obj):
        if isinstance(obj, dict):
            self.__cursor = int(obj.get("cursor", 0))

            self.__links = []
            links = obj.get("links", [])
            for link in links:
                clink = CLink().decode(link)
                self.__links.append(clink)

                key = self._key(clink.uri())
                self.__index[key] = len(self.__links) - 1

        return self


class Linker(Launcher):
    '''
        linker who manage crawl links from spider
    '''
    def __init__(self, workdir, name):
        '''
            initialize linker instance
        :param name: string, linker name, an unique identifier
        :param configs: list, PatternConfig objects in list
        '''
        Launcher.__init__(self, workdir, name)

    def launch(self):
        #launch sub class instance
        self._launch()


    def shutdown(self):
        #shutdown sub class instance
        self._shutdown()

    def filter(self, *cond):
        '''
            add accept condition for linker
        :param cond: object, filter accept condition
        :return:
        '''
        self._filter(*cond)

    def accept(self, uri):
        '''
            test if the uri is accept by linker
        :param uri: uri, Uri obejct
        :return: boolean
        '''
        return self._accept(uri)

    def config(self, pattern, config):
        '''
            add configure for url pattern for crawling
        :param pattern:
        :param config:
        :return:
        '''
        self._config(pattern, config)

    def push(self, uri):
        '''
            push a uri into link database
        :param uri: object, Uri object
        :return: object, key of stored link
        '''
        if self.accept(uri):
            stime = time.time()
            key = self._push(uri)
            etime = time.time()

            logger.info("linker: push link %s completed. time used:%fs", uri.url(), etime-stime)
            return key
        else:
            logger.info("linker: push link %s, skipped by filter.", uri.url())

        return None

    def pull(self):
        '''
            get a link object by specified key
        :return: object, Link object or None
        '''
        stime = time.time()
        link = self._pull()
        etime = time.time()

        if link is not None:
            logger.info("linker: pull link: %s completed. time used: %fs", link.uri().url(), etime-stime)
        else:
            logger.info("linker: pull link: none, nothing pulled.")

        return link

    def update(self, uri, extras):
        '''
            push a uri into link database
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return:
        '''
        stime = time.time()
        self._update(uri, extras)
        etime = time.time()

        logger.info("linker: update link %s completed. time used:%fs", uri.url(), etime-stime)

    def _launch(self):
        '''
            launch linker, subclass must implement this method
        :return:
        '''
        logger.warning("linker: unimplemented launch method, nothing will be done.")

    def _shutdown(self):
        '''
            shutdown linker, subclass must implement this method
        :return:
        '''
        logger.warning("linker: unimplemented shutdown method, nothing will be done.")

    def _filter(self, *cond):
        '''
            add accept condition for linker
        :param cond: object, filter accept condition, subclass must implement this method
        :return:
        '''
        logger.warning("linker: unimplemented filter method, nothing will be done.")

    def _accept(self, uri):
        '''
            test if the uri is filtered by linker, subclass must implement this method
        :param uri: uri, Uri obejct
        :return: boolean
        '''
        logger.warning("linker: unimplemented accept method, default denied.")

        return False

    def _config(self, pattern, config):
        '''
            add configure for url pattern for crawling, subclass must implement this method
        :param pattern:
        :param config:
        :return:
        '''
        logger.warning("linker: unimplemented config method, nothing will be done.")

    def _push(self, uri):
        '''
            push a uri into link database, subclass must implement this method
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return: object, key of stored link
        '''
        logger.warning("linker: unimplemented push method, nothing will be done.")
        return None

    def _pull(self):
        '''
            get a link object by specified key
        :return: object, Link object or None
        '''
        logger.warning("linker: unimplemented pull method, nothing will be done.")

        return None

    def _update(self, uri, extras):
        '''
            udpate uri context
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return:
        '''
        logger.warning("linker: unimplemented update method, nothing will be done.")


class DefaultLinker(Linker):
    '''
        default link database using memory as self defined database
    '''
    __CONFIG_FILE_NAME = "configs"
    __LINKS_FILE_NAME = "links"

    def __init__(self, workdir, name = "default_linker"):
        '''
            initialize linker instance with @filter
        :param filter: object, Filter object
        '''
        Linker.__init__(self, workdir, name)

        #filter for link
        self.__filter = WhiteListFilter(workdir, "filter")
        # crawl configure for specified uri pattern
        self.__configs = PConfigs()
        # links for crawling, with Link object in the list
        self.__links = CLinks()

    def _launch(self):
        '''
            lauch default linker
        :return:
        '''
        #launch filter of linker
        self.__filter.launch()

        #load configures of linker
        if Helper.exists(self.workdir(), self.__CONFIG_FILE_NAME):
            try:
                fconfigs = Helper.open(self.workdir(), self.__CONFIG_FILE_NAME, "r")
                jsonobj = json.load(fconfigs)
                fconfigs.close()
            except:
                pass
            else:
                self.__configs.decode(jsonobj)


        #load links of linker
        if Helper.exists(self.workdir(), self.__LINKS_FILE_NAME):
            try:
                flinks = Helper.open(self.workdir(), self.__LINKS_FILE_NAME, "r")
                jsonobj = json.load(flinks)
                flinks.close()
            except:
                pass
            else:
                self.__links.decode(jsonobj)

    def _shutdown(self):
        '''
            shutdown default linker
        :return:
        '''
        #shutdown filter of linker
        self.__filter.shutdown()

        #save configures of linker
        fconfigs = Helper.open(self.workdir(), self.__CONFIG_FILE_NAME, "w")
        json.dump(self.__configs.encode(), fconfigs)
        fconfigs.close()

        #save links of linker
        flinks = Helper.open(self.workdir(), self.__LINKS_FILE_NAME, "w")
        json.dump(self.__links.encode(), flinks)
        flinks.close()

    def _filter(self, *cond):
        return self.__filter.filter(*cond)

    def _accept(self, uri):
        return self.__filter.accept(uri.url())

    def _config(self, pattern, config):
        '''
            link crawl configure with sepcified pattern
        :param pattern:
        :param config:
        :return:
        '''
        self.__configs.add(pattern, config)

    def _push(self, uri):
        '''
            store the uri into database
        :param uri: object, Uri object
        :param extras: dict, extras message for uri
        :return: string, key of uri
        '''
        return self.__links.push(uri)

    def _pull(self):
        '''
            pull Link from database by specified uri
        :param uri: object, Uri object
        :return: object, Link object or None
        '''
        link = self.__links.pull()

        #pull the next link need crawling
        while link is not None:
            config = self.__configs.match(link.uri())
            context = link.contexts().last()

            #crawl period, need to crawl
            if context is None or context.tm() + config.crawl_period() < time.time():
                break
            else:
                logger.info("default linker: pull link: %s, skipped for crawling period not satisfied.", link.uri().url())

            link = self.__links.pull()

        return link

    def _update(self, uri, extras):
        '''
            update context of uri
        :param uri:
        :param extras:
        :return:
        '''
        self.__links.update(uri, extras)

class LinkerMgr(Launcher):
    '''
        linker manager for manage linker instance, there is only not more than one linker instance in manager
    '''
    def __init__(self, workdir, name):
        #initialize super
        Launcher.__init__(self, workdir, name)

        #there is only 1 linker in manager, default none
        self.__linker = None

    def launch(self):
        '''
            launch linker manager
        :return:
        '''
        if self.__linker is None:
            logger.warning("linker manager: there is no linker registered. invoke launch nothing")
            return

        #launch registered linker
        self.__linker.launch()


    def shutdown(self):
        '''
            shutdown linker manager
        :return:
        '''
        if self.__linker is None:
            logger.warning("linker manager: there is no linker registered. invoke shutdown nothing")
            return

        #shutdown registered linker
        self.__linker.shutdown()

    def register(self, linker):
        '''
            load @linker into linker manager, replace current linker
        :param linker: object, linker to be loaded
        :return: object, old linker or None
        '''
        old = self.__linker

        self.__linker = linker
        if self.__linker is not None:
            logger.info("linker manager: register new linker %s.", self.__linker.name())
        else:
            if old is None:
                logger.warning("linker manager: linker is none, no linker registered.")
            else:
                logger.warning("linker manager: linker is none, old linker %s is unregistered.", old.name())

        return old

    def filter(self, *cond):
        '''
            add accept condition for linker
        :param cond: object, filter accept condition
        :return:
        '''
        if self.__linker is None:
            logger.error("linker manager: there is no linker registered. invoke filter failed.")
            return

        self.__linker.filter(*cond)

    def config(self, pattern, config):
        '''
            add configure for url pattern for crawling
        :param pattern:
        :param config:
        :return:
        '''
        if self.__linker is None:
            logger.error("linker manager: there is no linker registered. invoke config failed.")
            return

        self.__linker.config(pattern, config)

    def push(self, uri):
        '''
            push a new uri to linker
        :param uri:
        :return:
        '''
        if self.__linker is None:
            logger.error("linker manager: there is no linker registered. invoke push failed.")
            return None

        return self.__linker.push(uri)

    def pull(self):
        if self.__linker is None:
            logger.error("linker manager: there is no linker registered. invoke pull failed.")
            return None

        return self.__linker.pull()


    def update(self, uri, extras):
        if self.__linker is None:
            logger.error("linker manager: there is no linker registered. invoke update failed.")
            return None

        return self.__linker.update(uri, extras)

    @staticmethod
    def default(workdir = "./linker", name = "linker_manager"):
        linker_manager = LinkerMgr(workdir, name)

        default_linker = DefaultLinker(workdir, "default_linker")
        default_linker.filter(r".*")

        linker_manager.register(default_linker)

        return linker_manager

if __name__ == "__main__":
    linker_manager = LinkerMgr.default("/tmp/spider/linker")

    linker_manager.config(r".*", CConfig(True, 5))

    linker_manager.launch()

    linker_manager.push(Uri("http://www.baidu.com/1"))
    linker_manager.push(Uri("http://www.baidu.com/2"))
    linker_manager.push(Uri("http://www.baidu.com/3"))
    linker_manager.push(Uri("http://www.baidu.com/4/5"))

    link = linker_manager.pull()
    while link is not None:
        link = linker_manager.pull()
        time.sleep(1)


    linker_manager.shutdown()

