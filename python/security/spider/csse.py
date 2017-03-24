
import sys
import pickle
sys.path.append("../")
sys.path.append("../../")

from spider.cspider import Spider

class SSE(Spider):
    urls = {
        "getAllStocks":"http://www.sse.com.cn/js/common/ssesuggestdataAll.js"
    }

    def getAllStocks(self):
        return self.get(self.urls["getAllStocks"])


if __name__ == "__main__":

    sse = SSE()

    print sse.getAllStocks().getContent()