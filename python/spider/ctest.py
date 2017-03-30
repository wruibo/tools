import cexpt

from chelper import Helper

# coding=utf8
# -*- coding: utf8 -*-

def raise_error(msg):
    raise cexpt.ExpUnsupportedProtocol(msg)

class obj:
    __d = None
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

class obj1:
    def __init__(self, a, b, c):
        self.__a = a
        self.__b = b
        self.__c = c

    def seta(self, a):
        self.__a = a

    def geta(self):
        return self.__a

    def __str__(self):
        return str(self.__a)+","+str(self.__b)+","+str(self.__c)

    def __repr__(self):
        return str(self.__a) + "|" + str(self.__b) + "|" + str(self.__c)

def catch_error(msg, tt):
    try:
        raise_error(msg+tt)
    except Exception, e:
        print e.message
    else:
        print "no error"


def fun(*arg):
    for a in arg:
        print a
    raise ""

import urllib2, cookielib

def saveCookie():
    filename = '/tmp/cookie.txt'
    cookie = cookielib.MozillaCookieJar(filename)
    cookie.set_cookie(cookielib.Cookie())
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    res = opener.open('https://www.caifuqiao.cn/')
    res = opener.open('http://www.baidu.com/')
    res = opener.open('http://www.baidu.com/')
    res = opener.open('https://www.caifuqiao.cn/')
    cookie.save(ignore_discard=True,ignore_expires=True)

if __name__ == "__main__":

    #saveCookie()
    a = obj1(1, 2, 3)
    print a

    print repr(a)

    fun(1)

