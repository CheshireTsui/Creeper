# -*- coding: utf-8 -*-
#from myproxy import getProxyList
import socket
import time
import os
import re

dirList = ['cookie', 'message pattern', 'response data', 'request data']
path = os.path.join(os.path.abspath(os.path.dirname('creeperlib.py')))
for i in dirList:
    new_path = os.path.join(path, i)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)

m_dict = {'Jan': '01', 'Feb': '02', 'Mar': '03','Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', }

pattern_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Host': '/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
}
class Cookie:
    """docstring for Cookie"""
    def __init__(self):
        self.name = ''
        self.value = ''
        self.domain = ''
        self.path = ''
        self.max_age = ''


class CookieProcessor:
    """docstring for CookieProcessor"""
    global path, m_dict
    def __init__(self, url):
        self.url = url
        self.savepath = os.path.join(path, 'cookie')
        self.cookie = Cookie()
        self.cookie_list = []

    def getCookie(self, header):
        cookie_pattern = re.compile(r'Set-Cookie:\s?(.*?)\n',re.S)
        name_pattern = re.compile(r'^(.*?)=(.*?);',re.S)
        domain_pattern = re.compile(r'domain=(.*?);',re.S)
        path_pattern = re.compile(r'path=(.*?);?',re.S)
        expires_pattern = re.compile(r'expires=\w{3}, (\d{2})-(\w{3})-(\d{2,4}) (\d{2}:\d{2}:\d{2}) GMT;',re.S)
        age_pattern = re.compile(r'max-age=(\d+);',re.S)

        raw_list = cookie_pattern.findall(header)
        for i in raw_list:
            self.cookie = Cookie()

            if i[-1]!=';': i += ';'
            
            self.cookie.path = '/'
            b_domain_pattern = re.compile(r'^\w+([^/]+)(/.*)?$',re.S)
            lis = b_domain_pattern.search(self.url).groups()
            self.cookie.domain = lis[0]
            if lis[1]: self.cookie.path = lis[1]

            self.cookie.max_age = 'session'

            lis = name_pattern.search(i).groups()
            #print lis
            self.cookie.name = lis[0]
            self.cookie.value = lis[1]

            try:
                self.cookie.max_age = age_pattern.search(i).group(1)
            except:
                try:
                    #print i
                    lis = expires_pattern.search(i).groups()
                    lis = '%s-%s-%s %s'%(lis[0],m_dict[lis[1]],lis[2],lis[3])
                    self.cookie.max_age = time.mktime(time.strptime(lis,'%d-%m-%Y %H:%M:%S'))
                except Exception, e:
                    pass
            
            
            try:
                self.cookie.domain = domain_pattern.search(i).group(1)
            except:
                pass
            
            try:
                if path_pattern.search(i).group(1): self.cookie.path = path_pattern.search(i).group(1)
            except:
                pass
            self.cookie_list.append(self.cookie)

        for i in self.cookie_list:
            try:
                p = '%s.xml' % os.path.join(self.savepath, i.domain)
                f = open(p, 'a+')
                ci ='<maxage>%s</maxage>\n<name>%s</name>\n<value>%s</value>\n<path>%s</path>\n\n'%(i.max_age, i.name, i.value, i.path)
                f.write(ci)
            except Exception, e:
                raise e
            finally:
                f.close()

    def addCookie(self):
        pass


class HttpRequest:
    """docstring for HttpRequest"""
    global pattern_header, path

    def __init__(self, url, method='GET', cookie='', postData={}):
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
        if (len(self.url) - i) == 1:
            self.header['Host'] = self.url
            self.url = '/'
        if self.cookie:
            self.header['Cookie'] = self.cookie

        for i in self.header:
            self.header_instance += '%s:%s\r\n' % (i, self.header[i])

        if self.postData:
            if self.method == 'GET':
                print "Warning: 'GET' method is supposed to have no post data."
            for i in self.postData:
                self.postData_instance += '%s:%s\r\n' % (i, self.postData[i])
            self.postData_instance += '\r\n'

        self.message_instance = '%s %s %s\r\n%s\r\n%s' % (
            self.method, self.url, self.protocol, self.header_instance, self.postData_instance)

    def message(self):
        self.__compile()
        return self.message_instance

    def saveMessage(self, name=''):
        self.__compile()

        if not name:
            time_stamp = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
            name = 'request%s.txt' % time_stamp
        p = os.path.join(path, 'request data')
        p = os.path.join(p, name)

        f = open(p, 'w')
        f.write(self.message_instance)
        f.close()


class Creeper:
    """docstring for Creeper"""

    def __init__(self, url):
        self.Request_instance = HttpRequest()
        self.url = url


header = '''HTTP/1.1 200 OK

Cache-Control: private, max-age=0

Transfer-Encoding: chunked

Content-Type: text/html; charset=utf-8

Vary: Accept-Encoding

Server: Microsoft-IIS/8.5

P3P: CP="NON UNI COM NAV STA LOC CURa DEVa PSAa PSDa OUR IND"

Set-Cookie: _FS=1; domain=.bing.com; path=/

Set-Cookie: _SS=2; domain=.bing.com; path=/

Set-Cookie: SRCHD=3; expires=Sun, 08-Jan-2017 12:01:17 GMT; domain=.bing.com; path=/

Set-Cookie: SRCHUID=4; expires=Sun, 08-Jan-2017 12:01:18 GMT; path=/

Set-Cookie: SRCHUSR=5; expires=Sun, 08-Jan-1970 12:01:19 GMT; domain=.bing.com; path=/

Edge-control: no-store

X-MSEdge-Ref: Ref A: 9F5E6306D921459386FCDFCAC2B5C885 Ref B: 7C4A4CEF507C57E94664443038AB00A0 Ref C: Fri Jan 09 04:01:17 2015 PST

Set-Cookie: BDSVRTM=6; path=/

Set-Cookie: BAIDUID=7; expires=Thu, 31-Dec-36 23:55:50 GMT; max-age=2147; path=/; domain=.baidu.com

Set-Cookie: BAIDUPSID=8; expires=Thu, 31-Dec-37 23:55:55 GMT; max-age=2147483647; path=/; domain=.baidu.com

Set-Cookie: BDSVRTM=9; path=/

Date: Fri, 09 Jan 2015 12:01:16 GMT

'''


a = HttpRequest('www.baidu.com', 'GET', )
b = CookieProcessor('www.test-page.me')
b.getCookie(header)
# a.saveMessage('data.txt')
#print a.message()
#print getProxyList()
