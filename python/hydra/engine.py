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
    from net import http
    resp = http.client.get("http://www.caifuqiao.cn/")
    print resp

    resp = http.client.get("http://www.sohu.com/")
    print resp

    resp = http.client.get("http://www.sina.com.cn/")
    print resp

    http.client.close()
