import time
import re
from typing import List, Set, Tuple
import gc
import pickle
#import requests

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
        print('get:', url)
        time.sleep(1)
        try:
            html = get.browser.get(url)
        except InternetError as e:
            print(e)
            time.sleep(5)
            return get(url, useCache=useCache)
        if useCache:
            get.cache.set(url, html)
        return html
#隔离日记
home_page = 'https://www.douban.com/search?source=suggest&q=%E9%9A%94%E7%A6%BB%E6%97%A5%E8%AE%B0'
html = get(url=home_page,useCache=False)
#print(html)


def getElement(pattern, default=None):
    r = re.findall(pattern, html,re.S)
    if default == None:
        assert(len(r) == 1)
    else:
        assert(1 == 1)
    if len(r) == 0:
        return None
    else:
        return r

title_list = getElement(r"sid: (.*?), qcat", default=1)

print(title_list)
