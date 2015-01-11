# -*- coding: utf-8 -*-
import socket
import time
import os
import re

dirList = ['cookie', 'message pattern', 'response data', 'request data']
path=os.path.join(os.path.abspath(os.path.dirname('creeperlib.py')))
for i in dirList:
    new_path = os.path.join(path, i)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)


pattern_header = {
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding':'gzip, deflate, sdch',
      'Accept-Language':'zh-CN,zh;q=0.8',
      'Connection':'keep-alive',
      'Host':'/',
      'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}


class CookieProcessor:
    """docstring for CookieProcessor"""
    def __init__(self, header):
        self.header = header
        self.domain = ''

    def getCookie(self):
        pass

    def addCookie(self):
        pass


class HttpRequest:
    """docstring for HttpRequest"""
    global pattern_header, path
    def __init__(self, url, method = 'GET', cookie = '', postData = {}):
        self.method = method
        self.url = url
        self.protocol = 'HTTP/1.1'
        self.header = pattern_header
        self.cookie = cookie
        self.postData = postData
        self.header_instance = ''
        self.postData_instance = ''
        self.message_instance = None

    def __compile(self):
        for i in range(len(self.url)):
            if self.url[i] == '/':
                self.header['Host'] = self.url[:i]
                self.url = self.url[i:]
                break
        if(len(self.url)-i) == 1:
            self.header['Host'] = self.url
            self.url = '/'
        if self.cookie:
            self.header['Cookie'] = self.cookie

        for i in self.header:
            self.header_instance += '%s:%s\r\n' %(i,self.header[i])
            
        if self.postData:
            if self.method == 'GET':
                print "Warning: 'GET' method is supposed to have no post data."
            for i in self.postData:
                self.postData_instance += '%s:%s\r\n' %(i,self.postData[i])
            self.postData_instance += '\r\n'

        self.message_instance = '%s %s %s\r\n%s\r\n%s'%(self.method, self.url, self.protocol, self.header_instance, self.postData_instance)

    def message(self):
        self.__compile()
        return self.message_instance

    def saveMessage(self, name = ''):
        self.__compile()

        if not name:
            time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
            name = 'request%s.txt' % time_stamp
        p = os.path.join(path,'request data')
        p = os.path.join(p, name)

        f = open(p, 'w')
        f.write(self.message_instance)
        f.close()


class Creeper:
    """docstring for Creeper"""
    def __init__(self, url):
        self.Request_instance = HttpRequest()
        self.url = url
            

a = HttpRequest('www.baidu.com','GET',})
#a.saveMessage('data.txt')
print a.message()
