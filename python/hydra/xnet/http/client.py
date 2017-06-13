'''
    http client for access remote http urls
'''
import urllib

from xnet.http import config, handler, response

class Client:
    def __init__(self):
        #urllib opener as http client
        self.client = urllib.request.build_opener(*handler.defaults)

    def get(self, url, filename=None, resume=False):
        try:
            if filename is None:
                return response.HtmlResponse(self.client.open(url))
            else:
                return response.FileResponse(self.client.open(url), filename, resume)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return response.ErrorResponse(e, url)

    def post(self, url, data=None, filename=None):
        pass

    def dld(self, url, filename):
        try:
            response = self.client.open(url)
            with open(filename, "wb") as f:
                content = response.read(config.read_buffer_size)
                while content:
                    f.write(content)
                    content = response.read(config.read_buffer_size)
            return response.getcode(), response.msg, response.headers, filename
        except Exception as e:
            return -1, str(e.__class__.__name__) + ":" + str(e), None, None


default_client = Client()


def get(self, url, filename=None, resume=False):
    return default_client.get(url, filename, resume)


if __name__ == "__main__":
    print(default_client.get("http://www.baidu.com/"))