'''
    useful functions for spider
'''
import re, os, sys, time


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def charset(content):
        regex = re.compile('charset=["]*([a-zA-Z-0-9]+)["]*', re.IGNORECASE)
        result = regex.search(content)
        if result is not None:
            return result.group(1)

        return None

    @staticmethod
    def str(content, charset = None):
        #try to get charset of content from itself
        if charset is None:
            charset = Helper.charset(content)

        #unknown charset just return the original content
        if charset is None:
            return content

        try:
            return content.decode(charset, 'ignore')
        finally:
            return content

    @staticmethod
    def protocol(url):
        '''
            parse protocol from @url
        :param url: string, url to parse
        :return: string, protocol
        '''
        if url is not None:
            result = re.match(r"(\w+)://", url, re.IGNORECASE)
            if result is not None:
                return result.group(1)

        return ""

    @staticmethod
    def root_path(path):
        '''
            parse root url path from @url
        :param url: string, base url will be parsed from
        :return: string, base url of @url
        '''
        if path.startswith("/"):
            return "/"
        else:
            result = re.match(r'(^\w+://[^/]+/?)', path, re.IGNORECASE)

            if result is not None:
                root = result.group(1)
                if root[-1] != '/':
                    root += '/'
                return root
            else:
                return ""

    @staticmethod
    def current_path(path):
        '''
            parse current url path from @path
        :param url: string, complete url
        :return: string, relative url parsed
        '''
        if Helper.is_relative_path(path):
            return ""

        result = re.match(r'(.*/)[^/]*$', path, re.IGNORECASE)

        if result is not None:
            path = result.group(1)
            if path[-1] != "/":
                path += "/"

        return path

    @staticmethod
    def is_remote_path(path):
        '''
            detect whether @path is remote url, like: http://..., ftp://..., file://...
        :param path: string, path to detect
        :return: boolean
        '''
        result = re.match(r'^\w+://.*', path, re.IGNORECASE)
        if result is not None:
            return True

        return False

    @staticmethod
    def is_local_path(path):
        '''
            detect whether @path is local path, like: /tmp/abc, tmp/abc, ...
        :param path: string, path to detect
        :return: boolean
        '''
        return not Helper.is_remote_path(path)

    @staticmethod
    def is_absolute_path(path):
        '''
        detect whether @path is an absolute path, like: /tmp/abc, /lib/abc, ...
        :param path: string, path to detect
        :return: boolean
        '''
        return path.startswith("/")

    @staticmethod
    def is_relative_path(path):
        '''
            detect whether @path is an relative path, like: tmp/abc, lib/abc, ....
        :param path: string, path to detect
        :return: boolean
        '''
        return not (Helper.is_url(path) or Helper.is_absolute_path(path))

    @staticmethod
    def combine_path(ref, path):
        '''
            combine the path with @ref as an completed url
        :param ref: string, reference of @path
        :param url: string, url correspond with @ref
        :return: string, combined url
        '''
        if ref is None or path == "":
            return path

        if path is None or path == "":
            return ref

        if Helper.is_remote_path(path):
            return path

        if path[0] == "/":
            if Helper.is_remote_path(ref):
                ref = Helper.root_path(ref)
            else:
                ref = "/"
        else:
            while len(ref) > 0 and ref[-1] != "/":
                ref = ref[:-1]

        while len(ref) > 0 and ref[-1] == "/":
            ref = ref[:-1]

        while len(path) > 0 and path[0] == "/":
            path = path[1:]

        return ref + "/" + path

    @staticmethod
    def makedirs(path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    @staticmethod
    def exists(dir, fname):
        fpath = dir + "/" +fname
        return os.path.isfile(fpath)

    @staticmethod
    def open(dir, fname, mode):
        fpath = dir + "/" + fname
        Helper.makedirs(fpath)

        return open(fpath, mode)

    @staticmethod
    def write2file(path, str, mode = "w"):
        Helper.makedirs(path)

        f = open(path, mode)
        f.write(str)
        f.close()

    @staticmethod
    def readfromfile(path, mode = "r"):
        if not os.path.isfile(path):
            return ""

        f = open(path, mode)
        str = f.read()
        f.close()

        return str

    @staticmethod
    def md5(str):
        '''
            compute md5 of @str
        :return: string
        '''
        import  hashlib
        m = hashlib.md5()
        m.update(str)

        return m.hexdigest()

    @staticmethod
    def sha1(str):
        '''
            compute sha1 of @str
        :return: string
        '''
        import hashlib

        h = hashlib.sha1()
        h.update(str)

        return h.hexdigest()

    @staticmethod
    def tidystr(obj):
        if obj is not None:
            return str(obj).strip()

        return "None"

    @staticmethod
    def strjoin(spliter, *objs):
        strs = []
        for obj in objs:
            strs.append(Helper.tidystr(obj))
        return spliter.join(strs)

    @staticmethod
    def objsplit(spliter, str):
        objs = []

        strs = str.split(spliter)
        for str in strs:
            objs.append(Helper.object(str))

        return objs

    @staticmethod
    def object(str):
        if str == str(True):
            return True
        elif str == str(False):
            return False
        elif str == str(None):
            return None
        else:
            return str

    @staticmethod
    def timerun(func, *args):
        stime = time.time()
        ret = func(*args)
        etime = time.time()

        return etime - stime, ret
