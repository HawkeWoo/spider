# -*- coding: utf-8 -*-
# @Author  : HulkWu
# @Time    : 2017/3/30 14:33
# @File    : proxy.py

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


def change_proxy(proxies=[]):
    '''
    更改当前使用的ip代理
    :param proxies: 代理ip列表池
    :return:
    '''
    proxy = random.choice(proxies)
    if proxy:
        proxy_handle = urllib2.ProxyHandler({})
    else:
        proxy_handle = urllib2.ProxyHandler({'http': proxy})
    opener = urllib2.build_opener(proxy_handle)
    opener.addheaders = [('User-Agent', headers['User-Agent'])]
    urllib2.install_opener(opener)
    print 'ip: %s' % ('localhost' if proxy == None else proxy)


if __name__ == "__main__":
    proxies = get_proxy()
    change_proxy(proxies)
