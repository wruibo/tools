'''
    filter for urls to crawl
'''
import re, os, json

from chelper import Helper
from clogger import logger
from clauncher import Launcher


class Filter(Launcher):
    '''
        filter base class, use white list rules
    '''
    def __init__(self, name, workdir):
        Launcher.__init__(self, name, workdir)

    def launch(self):
        self._launch()

    def shutdown(self):
        self._shutdown()

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
        :param obj:
        :return:
        '''
        return self._accept(obj)

    def _launch(self):
        logger.warning("filter: unimplemented launch method, nothing will be done.")

    def _shutdown(self):
        logger.warning("filter: unimplemented shutdown method, nothing will be done.")

    def _filter(self, *cond):
        logger.warning("filter: unimplemented filter method, nothing will be done.")

    def _accept(self, obj):
        logger.warning("filter: unimplemented accept method, nothing will be done.")
        return None


class WhiteListFilter(Filter):
    '''
        default filter for url with preferred white list
    '''
    def __init__(self, workdir, name = "white_list"):
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
        '''
            load filter patterns from file
        :return:
        '''
        try:
            file = Helper.open(self.workdir(), self.name(), "r")
            patterns = json.load(file)
            file.close()
        except Exception, e:
            logger.warning("white list filter: %s launch nothing. %s", self.name(), e.message)
        else:
            if isinstance(patterns, list):
                self._filter(*tuple(patterns))
            logger.info("white list filter: %s launch succeed. ", self.name())


    def _shutdown(self):
        '''
            save filter patterns to file
        :return:
        '''
        try:
            file = Helper.open(self.workdir(), self.name(), "w")
            json.dump(self.__patterns, file)
            file.close()
        except Exception, e:
            logger.warning("white list filter: %s shutdown error, %s", self.name(), e.message)
        else:
            logger.info("white list filter: %s shutdown succeed.", self.name())

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
                return True

        return False


class BlackListFilter(Filter):
    '''
        default filter for url with preferred white list
    '''
    def __init__(self, workdir, name = "black_list"):
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
        '''
            load filter patterns from file
        :return:
        '''
        try:
            file = Helper.open(self.workdir(), self.name(), "r")
            patterns = json.load(file)
            file.close()
        except Exception, e:
            logger.warning("black list filter: %s launch nothing. %s", self.name(), e.message)
        else:
            if isinstance(patterns, list):
                self._filter(*tuple(patterns))
            logger.info("black list filter: %s launch succeed. ", self.name())

    def _shutdown(self):
        '''
            save filter patterns to file
        :return:
        '''
        try:
            file = Helper.open(self.workdir(), self.name(), "w")
            json.dump(self.__patterns, file)
            file.close()
        except Exception, e:
            logger.warning("black list filter: %s shutdown error, %s", self.name(), e.message)
        else:
            logger.info("black list filter: %s shutdown succeed.", self.name())

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
    filter = WhiteListFilter("/tmp/spider/filter")
    filter.launch()

    filter.filter("http://www.baidu.com/a", "http://wwww.caifuqiao.cn/.*")

    print filter.accept("http://www.baidu.com/")
    print filter.accept("http://www.baidu.com/a/b")
    print filter.accept("http://www.baidu1.com/")

    filter.shutdown()

    filter = BlackListFilter("/tmp/spider/filter")
    filter.launch()

    filter.filter("http://www.baidu.com/a", "http://wwww.caifuqiao.cn/.*")

    print filter.accept("http://www.baidu.com/")
    print filter.accept("http://www.baidu.com/a/b")
    print filter.accept("http://www.baidu1.com/")

    filter.shutdown()