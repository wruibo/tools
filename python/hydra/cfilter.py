'''
    filter for urls to crawl
'''
import json
import re

from clauncher import Launcher

from .chelper import Helper
from .util.log import Logger


class Filter(Launcher):
    '''
        filter base class, use white list rules
    '''
    def __init__(self, workdir, name = "filter"):
        Launcher.__init__(self, workdir, name)

    def launch(self):
        '''
            launch filter
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._launch)
            Logger.info("filter: launch filter - %s, time used: %fs", self.name(), time_used)
        except IOError as e:
            pass
        except Exception as e:
            Logger.info("filter: launch filter - %s, error: %s", self.name(), e.message)

    def persist(self):
        '''
            persist filter data
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._persist)
            Logger.info("filter: persist filter - %s, time used: %fs", self.name(), time_used)
        except Exception as e:
            Logger.info("filter: persist filter - %s, error: %s", self.name(), e.message)

    def shutdown(self):
        '''
            shutdown filter
        :return:
        '''
        try:
            time_used, ret = Helper.timerun(self._shutdown)
            Logger.info("filter: shutdown filter - %s, time used: %fs", self.name(), time_used)
        except Exception as e:
            Logger.info("filter: shutdown filter - %s, error: %s", self.name(), e.message)

    def filter(self, *cond):
        '''
            add a condition object @cond into the filter
        :param cond: tuple, filter condition objects
        :return:
        '''
        self._filter(*cond)

    def accept(self, obj):
        '''
            test if obj is accept by filter
        :param obj: object, object to be test
        :return: boolean
        '''
        return self._accept(obj)

    def _launch(self):
        Logger.warning("filter: unimplemented launch method.")

    def _persist(self):
        Logger.warning("filter: unimplemented persist method.")

    def _shutdown(self):
        Logger.warning("filter: unimplemented shutdown method.")

    def _filter(self, *cond):
        Logger.warning("filter: unimplemented filter method.")

    def _accept(self, obj):
        Logger.warning("filter: unimplemented accept method.")


class WhiteListFilter(Filter):
    '''
        default filter for url with preferred white list
    '''
    def __init__(self, workdir, name = "filter"):
        Filter.__init__(self, workdir, name)

        # regex patterns for white list
        self.__patterns = []
        # compiled patterns
        self.__cpatterns = []

    def exists(self, pattern):
        for p in self.__patterns:
            if p == pattern:
                return True

        return False

    def _launch(self):
        file = Helper.open(self.workdir(), self.name(), "r")
        patterns = json.load(file)
        file.close()
        self._filter(*tuple(patterns))

    def _persist(self):
        file = Helper.open(self.workdir(), self.name(), "w")
        json.dump(self.__patterns, file)
        file.close()

    def _shutdown(self):
        self._persist()

    def _filter(self, *patterns):
        for pattern in patterns:
            if not self.exists(pattern):
                self.__patterns.append(pattern)
                self.__cpatterns.append(re.compile(pattern, re.IGNORECASE))

    def _accept(self, str):
        for cpattern in self.__cpatterns:
            result = cpattern.match(str)
            if result is not None:
                return True

        return False


class BlackListFilter(Filter):
    '''
        default filter for url with preferred white list
    '''
    def __init__(self, workdir, name = "filter"):
        Filter.__init__(self, workdir, name)

        # regex patterns for white list
        self.__patterns = []
        # compiled patterns
        self.__cpatterns = []

    def exists(self, pattern):
        for p in self.__patterns:
            if p == pattern:
                return True

        return False

    def _launch(self):
        file = Helper.open(self.workdir(), self.name(), "r")
        patterns = json.load(file)
        file.close()

        self._filter(*tuple(patterns))

    def _persist(self):
        file = Helper.open(self.workdir(), self.name(), "w")
        json.dump(self.__patterns, file)
        file.close()

    def _shutdown(self):
        self._persist()

    def _filter(self, *patterns):
        if len(patterns) == 0:
            return

        for pattern in patterns:
            if not self.exists(pattern):
                self.__patterns.append(pattern)
                self.__cpatterns.append(re.compile(pattern, re.IGNORECASE))

    def _accept(self, str):
        #accept if @url is in the white list
        for cpattern in self.__cpatterns:
            result = cpattern.match(str)
            if result is not None:
                return False

        return True


if __name__ == "__main__":
    filter = WhiteListFilter("/tmp/spider/filter", "white list filter")
    filter.launch()

    filter.filter("http://www.baidu.com/a", "http://wwww.caifuqiao.cn/.*")

    print(filter.accept("http://www.baidu.com/"))
    print(filter.accept("http://www.baidu.com/a/b"))
    print(filter.accept("http://www.baidu1.com/"))

    filter.shutdown()

    filter = BlackListFilter("/tmp/spider/filter", "black list filter")
    filter.launch()

    filter.filter("http://www.baidu.com/a", "http://wwww.caifuqiao.cn/.*")

    print(filter.accept("http://www.baidu.com/"))
    print(filter.accept("http://www.baidu.com/a/b"))
    print(filter.accept("http://www.baidu1.com/"))

    filter.shutdown()