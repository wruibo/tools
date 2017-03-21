'''
    filter for urls to crawl
'''
import re, os, json

from chelper import Helper

from cserializer import Serializer


class Filter:
    '''
        filter base class
    '''

    def __init__(self):
        pass

    def accept(self, url):
        pass


class DefaultFilter(Filter, Serializer):
    '''
        default filter for url with preferred white list
    '''
    #white list regex pattern for filter
    __white_list = []

    #black list regex pattern for filter
    __black_list = []

    def __init__(self):
        pass

    def accept(self, url):
        #accept if @url is in the white list
        for pattern in self.__white_list:
            result = re.match(pattern, url, re.IGNORECASE)
            if result is not None:
                return True

        #accept if @url is not in the black list
        for pattern in self.__black_list:
            result = re.match(pattern, url, re.IGNORECASE)
            if result is not None:
                return False

        return True

    def add_white_pattern(self, pattern):
        self.__white_list.append(pattern)

    def add_black_pattern(self, pattern):
        self.__black_list.append(pattern)

    def serialize(self, file):
        #combine the black&white list into a dictionary
        data = {"black_list":self.__black_list, "white_list":self.__white_list}

        Helper.makedirs(file)

        json.dump(data, open(file, "w"))

    def unserialize(self, file):
        if os.path.isfile(file):
            data = json.load(open(file, "r"))
            if isinstance(data, dict):
                self.__black_list = data.get("black_list", [])
                self.__white_list = data.get("white_list", [])


if __name__ == "__main__":
    filter = DefaultFilter()
    filter.add_black_pattern("http://wwww.baidu.com/")
    filter.add_black_pattern("http://wwww.abc.com/")
    filter.add_white_pattern("http://www.caifuqiao.com/")
    filter.add_white_pattern("http://www.caifuqiao.cn/")

    file_path = "/tmp/spider/filter"
    filter.serialize(file_path)

    filter1 = DefaultFilter()
    filter1.unserialize(file_path)

    print filter1
