# -*- coding: utf-8 -*-

"""
This code refers to the following blog written by @karaage and edited by @r_beginners
http://karaage.hatenadiary.jp/entry/2017/08/23/073000
"""

import os
import sys
import traceback
from mimetypes import guess_extension
from time import time, sleep
from urllib.request import urlopen, Request
from urllib.parse import quote
from bs4 import BeautifulSoup

MY_EMAIL_ADDR = ''

class Fetcher:
    def __init__(self, ua=''):
        self.ua = ua

    def fetch(self, url):
        req = Request(url, headers={'User-Agent': self.ua})
        try:
            with urlopen(req, timeout=3) as p:
                b_content = p.read()
                mime = p.getheader('Content-Type')
        except:
            sys.stderr.write('Error in fetching {}\n'.format(url))
            sys.stderr.write(traceback.format_exc())
            return None, None
        return b_content, mime

fetcher = Fetcher(MY_EMAIL_ADDR)

def fetch_and_save_img(word):
    data_dir = '/root/share/local_data/sandbox/yahoo_imgs'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for i, img_url in enumerate(img_url_list(word)):
        #sleep(8.8) # 400 access restrictions in 1 hour
        img, mime = fetcher.fetch(img_url)
        if not mime or not img:
            continue
        ext = guess_extension(mime.split(';')[0])
        if ext in ('.jpe', '.jpeg'):
            ext = '.jpg'
        if not ext:
            continue
        result_file = os.path.join(data_dir, str(i) + ext)
        with open(result_file, mode='wb') as f:
            f.write(img)
        print('fetched', img_url)


def img_url_list(word):
    """
    Scraping method for yahoo only (this script can't use at google)
    """
    page_count = 1
    img_all = []
    try:
        for k in range(0,2000,20):
            url = 'http://search.yahoo.co.jp/image/search?oq=&ktot=6&dtot=0&ei=UTF-8&p={}'.format(quote(word))
            full_url = url+"&xargs="+str(page_count)+"&b="+str(k+1)

            byte_content, _ = fetcher.fetch(full_url)
            sleep(10)  # 400 access restrictions in 1 hour
            structured_page = BeautifulSoup(byte_content.decode('UTF-8'), 'html.parser')
            img_link_elems = structured_page.find_all('a', attrs={'target': 'imagewin'})
            img_urls = [e.get('href') for e in img_link_elems if e.get('href').startswith('http')]
            img_all = img_all + list(set(img_urls))

            page_count = page_count+1
        return k

    finally:
        return img_all


'''
def img_url_list(word):
    """
    using yahoo (this script can't use at google)
    """
    url = 'http://image.search.yahoo.co.jp/search?n=60&p={}&search.x=1'.format(quote(word))
    byte_content, _ = fetcher.fetch(url)
    structured_page = BeautifulSoup(byte_content.decode('UTF-8'), 'html.parser')
    img_link_elems = structured_page.find_all('a', attrs={'target': 'imagewin'})
    img_urls = [e.get('href') for e in img_link_elems if e.get('href').startswith('http')]
    img_urls = list(set(img_urls))
    return img_urls
'''

if __name__ == '__main__':
    #word = sys.argv[1]
    word = '猫'
    fetch_and_save_img(word)
