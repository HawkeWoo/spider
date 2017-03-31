# -*- coding: utf-8 -*-
# @Author  : HulkWu
# @Time    : 2017/3/30 14:33
# @File    : proxy.py

import cookielib
import urllib
import urllib2
import random
from bs4 import BeautifulSoup

value = {
        'username': 'justfortest',
        'password': 'xxx'
    }
headers = {  # 伪装为浏览器抓取
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
agent_url = 'http://www.xicidaili.com/'
target_url = 'https://pixabay.com/'
login_url = "https://pixabay.com/zh/accounts/login/"


def get_proxy():
    '''
    获取 http://www.xicidaili.com/ 上的代理ip列表
    :return: [ip:port]列表
    '''
    proxies = [None]
    try:
        # 试图获取西刺代理的 IP 列表
        req = urllib2.Request(agent_url, headers=headers)
    except:
        print('无法获取代理信息!')
        return
    try:
        content = urllib2.urlopen(req).read()
        soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
        ip_tags = soup.find_all('tr', class_='odd')
        for ip_info in ip_tags:
            if ip_info.contents[11].string == "HTTP":
                proxy = ip_info.contents[3].string + ':' + ip_info.contents[5].string
                if check_ip(proxy):
                    proxies.append(proxy)
    except:
        return proxies
    return proxies


def change_proxy(proxies=[]):
    '''
    更改当前使用的ip代理
    '''

    # cookie
    cookie_file = './cookie.txt'
    cookie = cookielib.MozillaCookieJar(cookie_file)
    cookie.save(ignore_discard=True, ignore_expires=True)

    proxy = random.choice(proxies)
    if proxy == None:
        proxy_handler = urllib2.ProxyHandler({})
    else:
        proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    #cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), proxy_handler)
    # 将post数据进行编码
    post_info = urllib.urlencode(value)
    # 构造一个request对象
    request = urllib2.Request(login_url, post_info)
    # 添加header信息
    opener.addheaders = [('User-Agent', headers['User-Agent'])]
    # 利用opener打开请求
    opener.open(request)
    # 安装opener
    # urllib2.install_opener(opener)
    # urllib2.urlopen(request)
    return opener


def check_ip(proxy=''):
    '''
    检查代理ip是否可用
    :param proxy: 代理ip:端口
    :return: 可用则true，否则false
    '''
    proxy_handler = urllib2.ProxyHandler({"http": "http://" + proxy})
    opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    try:
        content = urllib2.urlopen("http://ip.catr.cn/", timeout=3)
        soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
        ip = soup.find('span').a.string
        if ip == proxy.split(':')[0]:
            return True
        return False
    except Exception:
        return False


# test
def print_cur_ip():
    try:
        content = urllib2.urlopen('http://ip.catr.cn/').read()
        soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
        # tags = soup.find('span')
        # if len(tags) == 0:
        #     print soup
        # else:
        #     for tag in tags:
        #         print tag
        ip = soup.find('span').a.string
        print ip
        print "======>"
    except urllib2.URLError, e:
        print e.reason


if __name__ == "__main__":
    print_cur_ip()
    a = get_proxy()
    print "proxy"
    print len(a)
    for x in a:
        print x
    b = change_proxy(a)

