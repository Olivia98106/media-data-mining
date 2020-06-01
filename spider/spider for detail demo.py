# -*- coding: utf-8 -*-

import time
import re
from typing import List, Set, Tuple
import gc
import pickle
import requests

from cache import Cache
from browser import DoubanBrowser, InternetError

cacheFile = '.cache'


def get(url, useCache=False):    
    if useCache and not hasattr(get, 'cache'):
        get.cache = Cache(path=cacheFile)
    if not hasattr(get, 'browser'):
        get.browser = DoubanBrowser()
    if useCache == True and url in get.cache:
        return get.cache[url]
    else:
        #print('get:', url)
        time.sleep(3)
        try:
            html = get.browser.get(url)
        except InternetError as e:
            print(e)
            time.sleep(5)
            return get(url, useCache=useCache)
        if useCache:
            get.cache.set(url, html)
        return html

class Post:
    title: str = ''
    post_id: str = ''
    time: str = ''
    note: str = ''

    def __init__(self, post_id: str):
        self.post_id = str(post_id)
        self.home_page = 'https://www.douban.com/note/'+str(post_id)+'/'

    def parse(self):
        # parse user info from homepage
        html = get(url=self.home_page)
        if not('2020' in html):
            return
        if '页面不存' in html:
            return

        if '隔离霜' in html:
            return
        
        if '隔离乳' in html:
            return 

        def getElement(pattern, default=None):
            nonlocal html
            r = re.findall(pattern, html,re.S)
            if default == None:
                assert(len(r) <= 1)
            else:
                #assert(len(r)>= 1)
                return r
            if len(r) == 0:
                return default
            else:
                #return r[0]
                return r

        self.title = getElement(r"<title>(.*?)</title>")[0].strip()

        self.time = getElement(r'<span class="pub-date">(.*?)</span>')[0].strip()

        note_ = getElement(r'<div class="note">(.*?)<div class="mod-tags">')

        if note_:
            self.note = note_[0].strip()
        else:
            self.note = ''

    
    @property
    def data(self):
        D = dict()
        D['title'] = self.title
        D['post_id'] = self.post_id
        D['time'] = self.time
        D['note'] = self.note
          
        return D


if __name__ == '__main__':
    # get post info
    post_list = YOUR_POSTLIST #fill it please~
    cnt = 0
    posts = dict()

    for post_id in post_list:
        print('scrawl the group:', post_id)
        #for each post
        post = Post(post_id=post_id)
        post.parse()
        if post == None:
            print('   there is nothing here')
            continue
        else:
            posts[post_id] = post
            cnt += 1
            print('   total:'+str(cnt))
        #print('   total:'+D)
            
    # save data to file
    pickle.dump({'posts': posts}, open('posts.data', 'wb'))
    print('Over!')

