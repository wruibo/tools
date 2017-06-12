'''
    hydra engine module for running the spiders
'''
import threading


class Engine(threading.Thread):
    def __init__(self):
        self.spiders = []

    def start(self):
        pass

    def stop(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    from .net import ihttp
    resp = ihttp.client.get("http://www.caifuqiao.cn/")
    print(resp)

    resp = ihttp.client.get("http://www.sohu.com/")
    print(resp)

    resp = ihttp.client.get("http://www.sina.com.cn/")
    print(resp)

    ihttp.client.close()
