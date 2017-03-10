'''
    crawl security data from different source
'''
from spider.cbrowser import Browser
from spider.cparser import Parser


class Spider:
    '''
        spider base class
    '''
    __browser = None

    __parser = None

    __extractor = None

    __storage = None

    def __init__(self, **kwargs):
        client = kwargs.get("client", "chrome")
        platform = kwargs.get("platform", "pc")

        self.__browser = Browser.default()
        self.__parser = Parser.default()


    def run(self):
        pass

    def get(self, url, **kwargs):
        return self.__browser.open(url, None, **kwargs)

    def post(self, url, data, **kwargs):
        return self.__browser.open(url, data, **kwargs)


if __name__ == "__main__":
    browser = Browser.default()
    parser = Parser.default()

    response = browser.open("http://www.baidu.com/")

    url = response.getUrl()
    content = response.getContent()

    links = parser.parse(url, content)

    print links