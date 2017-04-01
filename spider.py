# -*- coding: utf-8 -*-
# @Author  : HulkWu
# @Time    : 2017/3/29 17:09
# @File    : spider.py

from bs4 import BeautifulSoup
import urllib2
import os
import io
import proxy
from PIL import Image


headers = {  # 伪装为浏览器抓取
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }


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
    data = urllib2.urlopen(img_url).read()
    # print data
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


if __name__ == "__main__":

    file_dir = u".\image"
    url = "https://pixabay.com/zh/photos/?q=&image_type=&min_width=&min_height=&cat=people&pagi="
    web_pages = get_web_pages(url, 38, 50)
    for web_page in web_pages:
        print "visiting web:  " + web_page
        img_urls = get_img_urls(web_page)
        proxies = proxy.get_proxy()
        index = 0
        for img_url in img_urls:
            index += 1
            if index % 3 == 0:
                proxies = proxy.get_proxy()
            print "visiting image:  " + img_url
            img_dl_urls = get_img_dl_urls(img_url)
            opener = proxy.change_proxy(proxies)
            urllib2.install_opener(opener)
            for img_dl_url in img_dl_urls:
                file_name = os.path.join(file_dir, os.path.basename(img_dl_url))
                save_img(img_dl_url, file_name)
