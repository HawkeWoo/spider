# -*- coding: utf-8 -*-
# @Author  : HulkWu
# @Time    : 2017/3/30 14:33
# @File    : proxy.py

import cookielib
import urllib

import urllib2
import random
from bs4 import BeautifulSoup


headers = {  # 伪装为浏览器抓取
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}


def get_proxy():
    '''
    获取 http://www.xicidaili.com/ 上的代理ip列表
    :return: [ip:port]列表
    '''
    proxies = [None]
    try:
        # 试图获取西刺代理的 IP 列表
        req = urllib2.Request('http://www.xicidaili.com/', headers=headers)
    except:
        print('无法获取代理信息!')
        return
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
    ip_tags = soup.find_all('tr', class_='odd')
    for ip_info in ip_tags:
        if ip_info.contents[11].string == "HTTP":
            proxies.append(ip_info.contents[3].string + ':' + ip_info.contents[5].string)
    return proxies


# def change_proxy():
#     '''
#     更改当前使用的ip代理
#     '''
#     proxies = get_proxy()
#     proxy = random.choice(proxies)
#     if proxy:
#         proxy_handle = urllib2.ProxyHandler({})
#     else:
#         proxy_handle = urllib2.ProxyHandler({'http': proxy})
#     opener = urllib2.build_opener(proxy_handle)
#     opener.addheaders = [('User-Agent', headers['User-Agent'])]
#     urllib2.install_opener(opener)
#     print 'ip: %s' % ('localhost' if proxy == None else proxy)


def change_proxy():
    '''
    更改当前使用的ip代理
    '''
    proxies = get_proxy()
    proxy = random.choice(proxies)
    if proxy:
        proxy_handle = urllib2.ProxyHandler({})
    else:
        proxy_handle = urllib2.ProxyHandler({'http': proxy})


    c = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(c), proxy_handle)
    url_login = "https://pixabay.com/zh/accounts/login/"
    value = {
        'username': 'justfortest',
        'password': 'haokun88'
    }
    post_info = urllib.urlencode(value)
    request = urllib2.Request(url_login, post_info)

    opener.addheaders = [('User-Agent', headers['User-Agent'])]
    opener.open(request)
    urllib2.install_opener(opener)
    print 'ip: %s' % ('localhost' if proxy == None else proxy)
    return opener


if __name__ == "__main__":
    change_proxy()
