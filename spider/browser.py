# -*- coding: utf-8 -*-
# browser simulator
import time
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get(url, useCache=True):
    # naive get url method, abandoned
    time.sleep(3)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Cpasshrome/79.0.3945.88 Safari/537.36'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200 and r.url == url:
        return r.text
    else:
        err_info = "!Error:get(url).  url="+url+" r.status_code=" + \
            str(r.status_code)+" r.text="+repr(r.text)+" r.url="+r.url
        raise Exception(err_info)


class InternetError(Exception):
    """Exception for Internet not connected."""

    def __init__(self):
        self.message = '未连接到互联网'

    def __str__(self):
        return self.message


class DoubanBrowser():
    # chrome-headless based url-get
    browser: webdriver.chrome.webdriver.WebDriver = None
    username: str = ''
    password: str = ''
    login_page_url = 'accounts.douban.com/passport/login'

    def __init__(self):
        if self.username == None or self.password == None:
            raise Exception('请在browser.py里填入用户名密码！')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.browser = webdriver.Chrome(
            chrome_options=chrome_options)  # headless mode
        #self.browser = webdriver.Chrome() # brower with GUI

    def get(self, url):
        time.sleep(1)
        self.browser.get(url)
        '''
        print('wait me for 120s...')
        
        self.browser.get(url)
        time.sleep(120)
        '''

        if '无法访问此网站</span>' in self.browser.page_source or '未连接到互联网</span>' in self.browser.page_source:
            raise InternetError
      
        if self.browser.current_url != url:
            # check login error
            if self.login_page_url in self.browser.current_url:
                self.login()
                time.sleep(1)
                #full page
                self.browser.find_element_by_class_name('taboola-open-btn taboola-open').click()
                return self.get(url)
            elif 'sec.douban.com' in self.browser.current_url:
                self.sec_login()
                #full page
                self.browser.find_element_by_class_name('taboola-open-btn taboola-open').click()
                return self.get(url)
            else:
                # other error
                err_info = "!Error:DoubanBrowser.get.  url=" + \
                    url+" r.url="+self.browser.current_url
                with open('error_page.html', 'w', encoding='utf-8') as f:
                    f.write(self.browser.page_source)
            raise Exception(err_info)
        else:
            return self.browser.page_source
    
    def sec_login(self):
        self.browser.get('https://'+self.login_page_url)
        self.login()


    def login(self):
        #username password login mode
        time.sleep(1)
        self.browser.find_element_by_class_name(
            "account-tab-account").click()
        # enter username
        time.sleep(1)
        self.browser.find_element_by_id(
            'username').send_keys(self.username)
        # enter password
        time.sleep(1)
        self.browser.find_element_by_id('password').send_keys(self.password)
        time.sleep(1)
        # summit
        self.browser.find_element_by_class_name(
            "account-form-field-submit").click()
        for _ in range(10):
            if self.browser.current_url == 'https://www.douban.com/':
                print('login error', self.browser.current_url)
                return True
            time.sleep(3)
        raise Exception('login failed')

