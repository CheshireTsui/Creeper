# -*- coding: utf-8 -*-
import socket
import time
import re

host = '174.140.168.109'
port = 80
req = 'GET / HTTP/1.1\r\nHost:cn-proxy.com\r\nUser-Agent:Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36\r\nConnection:keep-alive\r\n\r\n'

s = socket.socket()
'''
print '='*25
print req
print '='*25
'''
k = ('m','n')
def isEnd(a,msg,lis):
    global k
    a[0] = a[1]
    a[1] = msg
    s = a[0] + a[1]
    rp = r'<tr>\n<td>(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})</td>\n<td>(\d{2,5})</td>'
    p = re.compile(rp,re.S)
    n = p.findall(s)
    if n:
        cnt = 0
        for i in n:
            cnt += 1
            if k == i:
                break
        if cnt != len(n):
            n = n[cnt:]
        if n:
            k = n[-1]
            #raw_input('press to continue...')
            lis += n
      
    p = re.compile(r'</\s?html>',re.S)
    if p.findall(s):
        return True
    return False

def getProxyList():
    try:
        s.connect((host,port))
    except Exception, e:
        print e,"\nFailed to connect the server！"

    try:  
        s.sendall(req)  
    except socket.error, e:  
        print 'Error sending data:%s' % e
    
    lis = []
    try:
        res_list = ['None','None']
        while 1:
            msg = s.recv(256)
            if isEnd(res_list,msg,lis):
                break
    except socket.error, e:  
        print 'Error receiving data:%s' % e
    return lis

#print getProxyList()
