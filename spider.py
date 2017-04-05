# -*- coding: utf-8 -*-
# @Author  : HulkWu
# @Time    : 2017/3/29 17:09
# @File    : spider.py

from bs4 import BeautifulSoup
from PIL import Image
import threading
import cookielib
import urllib2
import urllib
import random
import os
import io
import proxy


headers = {  # 伪装为浏览器抓取
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
value = {
        'username': 'justfortest',
        'password': 'xxx'
    }

file_dir = u".\image"

login_url = "https://pixabay.com/zh/accounts/login/"
spider_url = "https://pixabay.com/zh/photos/?q=&image_type=&min_width=&min_height=&cat=people&pagi="


def get_bs4_soup(website_url=""):
    '''
    :param website_url: 需要解析的web页面url
    :return: 利用beautifulsoup解析完的soup
    '''
    req = urllib2.Request(website_url, headers=headers)
    content = urllib2.urlopen(req).read()
    soup = BeautifulSoup(content, 'html.parser', from_encoding='GB18030')
    return soup


def get_web_pages(url_header="", page_start=0, page_end=10):
    '''
    :param url_header: url前面的组成部分
    :param page_start: 起始网页索引
    :param page_end: 终止网页索引
    :return: 目标网页集合
    '''
    web_pages = []
    for i in range(page_start, page_end):
        web_pages.append(url_header + str(i))
    return web_pages


def get_img_urls(web_url=""):
    '''
    :param web_url: 当前访问页面的url
    :return: 获取当前页面所有图片的目标链接
    '''
    img_urls = []
    soup = get_bs4_soup(web_url)
    tags = soup.find_all("div", class_="item")
    for tag in tags:
        img_url = "https://pixabay.com" + tag.a['href']
        img_urls.append(img_url)
    return img_urls


def get_img_dl_urls(img_url=""):
    '''
    :param img_url: 需要下载的图片url
    :return: 该图片不同分辨率下载url集合
    '''
    result = []
    url_head = "https://pixabay.com/zh/photos/download/"
    soup = get_bs4_soup(img_url)
    tags = soup.find_all("div", class_="download_menu")
    for tag in tags:
        little_tags = tag.find_all("input")
        flag = True
        for little_tag in little_tags:
            if os.path.splitext(little_tag['value'])[1] in ['.jpg']:
                if flag:
                    result.append(little_tag['value'])
                    flag = False
                else:
                    result.append(url_head + little_tag['value'])
    return result


def save_img(img_url="", file_name=""):
    print "downloading img: " + img_url
    url = urllib2.urlopen(img_url).geturl()
    data = urllib2.urlopen(url).read()
    # 判断图片是否完整
    if not valid_image(data):
        return
    with open(file_name, 'wb') as f:
        f.write(data)
    return


def valid_image(buf):
    try:
        Image.open(io.BytesIO(buf)).verify()
    except:
        return False
    return True


def change_proxy(proxies=[]):
    '''
    更改当前使用的ip代理
    '''
    # cookie
    cookie = cookielib.CookieJar()
    if len(proxies) > 0:
        proxy = random.choice(proxies)
    else:
        proxy = None
    if proxy:
        proxy_handler = urllib2.ProxyHandler({'http': "http://" + proxy})
    else:
        proxy_handler = urllib2.ProxyHandler({})
    # 实例化一个opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie), proxy_handler)
    # 将post数据进行编码
    login_info = urllib.urlencode(value)
    # 构造一个request对象
    request = urllib2.Request(login_url, login_info)
    # 添加header信息
    opener.addheaders = [('User-Agent', headers['User-Agent'])]
    # 利用opener打开请求
    opener.open(request)
    return opener


def main():
    web_pages = get_web_pages(spider_url, 1, 10)
    for web_page in web_pages:
        print "visiting web:  " + web_page
        img_urls = get_img_urls(web_page)
        for img_url in img_urls:
            print "visiting image:  " + img_url
            img_dl_urls = get_img_dl_urls(img_url)
            for img_dl_url in img_dl_urls:
                urllib2.install_opener(change_proxy(proxy.proxy_pool))
                file_name = os.path.join(file_dir, os.path.basename(img_dl_url))
                save_img(img_dl_url, file_name)


if __name__ == "__main__":
    proxy.init_proxy_pool(proxy.proxy_file)
    threads = []
    threads.append(threading.Thread(target=proxy.update_proxy_pool))
    threads.append(threading.Thread(target=proxy.check_proxy_pool))
    threads.append(threading.Thread(target=main))
    for thread in threads:
        thread.start()
