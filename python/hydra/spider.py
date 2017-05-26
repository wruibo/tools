'''
    spider base class
'''
import threading


class HttpSpider(threading.Thread):
    def __init__(self):
        #urls to be feed the spider
        self.urls = []
        #http client for crawl the url


        #flag for start or stop the spider
        self.stop = True
        self.stopped = True

    def init(self):
        '''
            initialize the spider, relate with @destroy.
        subclass need realize this method
        :return:
        '''
        pass

    def start(self):
        '''
            start the spider, use @stop methond to stop the spider after it's started
        :return:
        '''
        #check if the spider has been started
        if not self.stopped:
            return

        #reset the stop flag to start spider thread
        self.stop = False

        #start the spider thread
        threading.Thread.start(self)

    def parse(self, url, code, message, header, content):
        '''
            parse the http response content of @url
        :param url: request url
        :param code: response code
        :param message: response message
        :param header: response header
        :param content: response content
        :return:
        '''
        pass

    def error(self, url, code, message):
        '''
            process the http response error of @url
        :param url: request url
        :param code: response error code
        :param message: response error message
        :return:
        '''
        pass

    def stop(self):
        '''
            stop the spider, relate with the @start method
        :return:
        '''
        #check if the spider has been stopped
        if self.stopped:
            return

        #set the stop flag to stop spider thread
        self.stop = True

        #wait until the spider thread exit
        self.join()

    def destroy(self):
        '''
            destroy the spider, relate with @init
        subclass need realize this method
        :return:
        '''
        pass

    def run(self):
        '''
            running the spider until all the urls has crawled
        :return:
        '''
        #set the stopped flag first
        self.stopped = False

        #process all urls waiting crawled
        while not self.stop:
            #check if there has more urls
            if len(self.urls) == 0:
                break

            #get the next url to be crawled
            url = self.urls.pop(0)





        self.stopped = True