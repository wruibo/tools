'''
    crawl security data from different source
'''
from cbrowser import Browser
from cparser import Parser


class Spider:
    '''
        spider class
    '''
    __workingDir = None #working directory for current spider

    __browser = None

    __parser = None

    __extractor = None

    __storage = None

    def __init__(self, **kwargs):
        client = kwargs.get("client", "chrome")
        platform = kwargs.get("platform", "pc")

        self.__browser = Browser.default()
        self.__parser = Parser.default()

    @staticmethod
    def create(workingDir):
        return Spider()



    def start(self):
        pass

    def stop(self):
        pass

    def _fun(self):
        pass





if __name__ == "__main__":

    spider = Spider.create("abc")

    browser = Browser.default()
    parser = Parser.default()

    response = browser.open("http://www.baidu.com/")

    url = response.getUrl()
    content = response.getContent()

    links = parser.parse(url, content)

    print links