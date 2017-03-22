'''
    filter for urls to crawl
'''
import re, os, json

from chelper import Helper

from clauncher import Launcher


class Filter(Launcher):
    '''
        filter base class, use white list rules
    '''
    def __init__(self, name, workdir):
        Launcher.__init__(self, name, workdir)

    def filter(self, str):
        '''
            test @str is pass or denied by the filter
        :param str: string, string to be test
        :return: boolean, True - @str is denied by filter, False-@str is passed by filter
        '''
        return True

    def accept(self, *cond):
        '''
            add a condition object @cond into the filter
        :param cond: tuple, filter condition objects
        :return:
        '''
        pass


class DefaultFilter(Filter):
    '''
        default filter for url with preferred white list
    '''
    #regex patterns for white list
    __patterns = []

    #compiled patterns
    __cpatterns = []

    def __init__(self, name, workdir):
        Filter.__init__(self, name, workdir)

    def launch(self):
        '''
            load filter patterns from file
        :return:
        '''
        if not Helper.exists(self.workdir(), self.name()):
            return

        file = Helper.open(self.workdir(), self.name(), "r")
        if file is not None:
            self.__patterns = json.load(file)
            for pattern in self.__patterns:
                self.__cpatterns.append(re.compile(pattern, re.IGNORECASE))


    def shutdown(self):
        '''
            save filter patterns to file
        :return:
        '''
        file = Helper.open(self.workdir(), self.name(), "w")
        json.dump(self.__patterns, file)
        file.close()


    def filter(self, str):
        #accept if @url is in the white list
        for cpattern in self.__cpatterns:
            result = cpattern.match(str)
            if result is not None:
                return True

        return False

    def accept(self, *patterns):
        if len(patterns) > 0:
            for pattern in patterns:
                if not self.exists(pattern):
                    self.__patterns.append(pattern)
                    self.__cpatterns.append(re.compile(pattern, re.IGNORECASE))
        else:
            return self.__patterns

    def exists(self, pattern):
        for p in self.__patterns:
            if p == pattern:
                return True

        return False

if __name__ == "__main__":
    filter = DefaultFilter("filter1", "/tmp/spider2/filter")
    filter.launch()

    filter.accept("http://www.baidu.com/a", "http://wwww.caifuqiao.cn/.*")

    print filter.filter("http://www.baidu.com/")
    print filter.filter("http://www.baidu.com/a/b")
    print filter.filter("http://www.baidu1.com/")

    filter.shutdown()