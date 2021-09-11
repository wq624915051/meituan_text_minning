from numpy.core.numeric import False_
import requests
import pandas as pd
import os
import time
import random
import re
import base64
import zlib
from datetime import datetime
import json
import math
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def init():
    global store_comments, user_agent, user_agents, cookie
    store_comments = []
    user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.132 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.133 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.134 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.135 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.136 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.137 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.138 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.139 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.140 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.141 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',]

    user_agent = ['user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
              'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
              'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',]


def get_cookies(url):
    chromeoption = webdriver.ChromeOptions()
    chromeoption.add_argument(random.choice(user_agent))
    chromeoption.add_experimental_option('excludeSwitches',
                                            ['enable-automation'])
    driver = webdriver.Chrome(executable_path=(r'chromedriver.exe'), chrome_options=chromeoption)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        """
    })
    driver.get('https://passport.meituan.com/account/unitivelogin')
    time.sleep(random.randint(0,4))
    account_box = driver.find_element_by_id('login-email')
    account_box.send_keys('18899532807')
    password_box = driver.find_element_by_id('login-password')
    password_box.send_keys('wq981019.')
    time.sleep(10)
    driver.find_element_by_xpath('//input[@data-mtevent="login.normal.submit"]').click()
    driver.window_handles
    n = driver.window_handles # 获取当前页句柄
    driver.switch_to.window (n[-1])
    time.sleep(10)
    a = driver.find_element_by_xpath('//a[text()="武汉"]')
    url1 = a.get_attribute('href')
    driver.get(url1)
    driver.get('https://wh.meituan.com/meishi/c17/')
    driver.get(url)
    time.sleep(25)
    cookies_list = driver.get_cookies()
    driver.quit()
    return cookies_list


def get_param_cookie(cookies):
    cookie_str = ""
    for item_cookie in cookies:
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + "; "
        cookie_str += item_str
    cookie = cookie_str[:-2]
    return cookie



def store_comment(poiid, page, cookie):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'host': 'wh.meituan.com',
        'referer': 'https://wh.meituan.com/meishi/%s/'%poiid,
        'cookie': cookie,
    }
    store_url = 'https://wh.meituan.com/meishi/api/poi/getMerchantComment?'
    params = {
        'uuid': 'f24c05a9c0d8464490b0.1630861808.1.0.0',
        'platform': '1',
        'partner': '126',
        'originUrl': 'https://wh.meituan.com/meishi/' + str(poiid) + '/',
        'riskLevel': '1',
        'optimusCode': '10',
        'id': str(poiid),
        'userId': '625054939',
        'offset': str(page*10),
        'pageSize': '10',
        'sortType': '1',
    }
    response = requests.get(url=store_url, headers=headers, params=params)
    json = response.json()
    comments = json.get('data').get('comments')
    for comment in comments:
        person = {}
        person['评论店铺'] = poiid
        person['评论用户姓名'] = comment['userName']
        person['评论用户id'] = comment['userId']
        person['评论用户星级'] = comment['star']
        person['评论用户菜品'] = comment['menu']
        person['评论用户内容'] = comment['comment']
        person['评论时间'] = comment['commentTime']
        store_comments.append(person)
    time.sleep(random.randint(0,8))

    
    
store_comments = []
data = pd.read_excel('C:/Users/62491/desktop/wh美团c17店铺.xlsx')
for row in data.itertuples(index=True, name='Pandas'):
    poiid = getattr(row, "poiId")
    allCommentNum = getattr(row, "allCommentNum")
    page_count = math.ceil(allCommentNum/10)
    if page_count > 0:
        for page in range(page_count):
            try:
                store_comment(poiid, page, cookie)
            except Exception as e:
                t = 'https://wh.meituan.com/meishi/' + str(poiid)
                cookies_list = get_cookies(t)
                cookie = get_param_cookie(cookies_list)
                print(cookie)
                store_comment(poiid, page, cookie)
            print(page)
df2 = pd.DataFrame(store_comments)
df2.to_excel('C:/Users/62491/desktop/wh美团c17店铺评论.xlsx')


