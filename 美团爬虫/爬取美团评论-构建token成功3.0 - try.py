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
              'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73',
             ]


def get_cookies(cookies_list, url):
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
    driver.get(url)
    for cookie in cookies_list:
        cookie['domain'] = '.meituan.com'
        driver.add_cookie(cookie)
    time.sleep(10)
    driver.refresh()
    time.sleep(10)
    driver.get(url)
    time.sleep(10)
    cookies_list1 = driver.get_cookies()
    driver.quit()
    return cookies_list1


def get_param_cookie(cookies):
    cookie_str = ""
    for item_cookie in cookies:
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + "; "
        cookie_str += item_str
    cookie = cookie_str[:-2]
    return cookie



def store_comment(poiid, page, cookie):
    headers = {
        'user-agent': random.choice(user_agents),
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
    try:
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
        return '成功'
    except Exception as e:
        return '出错'


    





data = pd.read_excel('C:/Users/62491/desktop/wh美团c17店铺.xlsx')
for row in data.itertuples(index=True, name='Pandas'):
    poiid = getattr(row, "poiId")
    allCommentNum = getattr(row, "allCommentNum")
    page_count = math.ceil(allCommentNum/10)
    if page_count > 0:
        cookies_list = [{'domain': '.meituan.com',
                'httpOnly': False,
                'name': 'firstTime',
                'path': '/',
                'secure': False,
                'value': '1630899984627'},
                {'domain': '.meituan.com',
                'expiry': 1630986383,
                'httpOnly': True,
                'name': 'client-id',
                'path': '/',
                'secure': False,
                'value': 'dee1a9ff-6144-47dc-973e-598052d8a22c'},
                {'domain': '.meituan.com',
                'expiry': 1693107811,
                'httpOnly': False,
                'name': '__mta',
                'path': '/',
                'secure': False,
                'value': '150372233.1630899811256.1630899811256.1630899811256.1'},
                {'domain': '.meituan.com',
                'expiry': 1636083810,
                'httpOnly': False,
                'name': 'rvct',
                'path': '/',
                'secure': False,
                'value': '57'},
                {'domain': '.meituan.com',
                'expiry': 1636083810,
                'httpOnly': False,
                'name': 'ci',
                'path': '/',
                'secure': False,
                'value': '57'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'lng',
                'path': '/',
                'secure': False,
                'value': '114.308028'},
                {'domain': '.meituan.com',
                'httpOnly': False,
                'name': 'unc',
                'path': '/',
                'secure': False,
                'value': '%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'lat',
                'path': '/',
                'secure': False,
                'value': '30.653038'},
                {'domain': '.meituan.com',
                'expiry': 1725507801,
                'httpOnly': False,
                'name': '_lxsdk_cuid',
                'path': '/',
                'secure': False,
                'value': '17bb9340ce2c8-0a33132aec6702-4343363-144000-17bb9340ce3c8'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'token2',
                'path': '/',
                'secure': False,
                'value': 'f7WwmqViwA7Gl9DydL9SAM5j6JAAAAAAcw4AAO8pY8lkpswZRxjLcd2c39Ujs9djJd6Tb_PaXp_QTMWsK2bwfrED0-DSqruOFlvWlw'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'token',
                'path': '/',
                'secure': False,
                'value': 'f7WwmqViwA7Gl9DydL9SAM5j6JAAAAAAcw4AAO8pY8lkpswZRxjLcd2c39Ujs9djJd6Tb_PaXp_QTMWsK2bwfrED0-DSqruOFlvWlw'},
                {'domain': '.meituan.com',
                'expiry': 1725507801,
                'httpOnly': False,
                'name': '_lxsdk',
                'path': '/',
                'secure': False,
                'value': '17bb9340ce2c8-0a33132aec6702-4343363-144000-17bb9340ce3c8'},
                {'domain': '.meituan.com',
                'expiry': 1662435837,
                'httpOnly': False,
                'name': '_hc.v',
                'path': '/',
                'secure': False,
                'value': '13f84155-6f5e-9e81-740c-0eeab0e339bd.1630899838'},
                {'domain': '.meituan.com',
                'expiry': 1631504586,
                'httpOnly': False,
                'name': 'mtcdn',
                'path': '/',
                'secure': False,
                'value': 'K'},
                {'domain': '.meituan.com',
                'expiry': 1632109400,
                'httpOnly': True,
                'name': 'lsu',
                'path': '/',
                'secure': False,
                'value': ''},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'mt_c_token',
                'path': '/',
                'secure': False,
                'value': 'f7WwmqViwA7Gl9DydL9SAM5j6JAAAAAAcw4AAO8pY8lkpswZRxjLcd2c39Ujs9djJd6Tb_PaXp_QTMWsK2bwfrED0-DSqruOFlvWlw'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'lt',
                'path': '/',
                'secure': False,
                'value': 'f7WwmqViwA7Gl9DydL9SAM5j6JAAAAAAcw4AAO8pY8lkpswZRxjLcd2c39Ujs9djJd6Tb_PaXp_QTMWsK2bwfrED0-DSqruOFlvWlw'},
                {'domain': '.meituan.com',
                'expiry': 1630901783,
                'httpOnly': False,
                'name': '_lxsdk_s',
                'path': '/',
                'secure': False,
                'value': '17bb9340ce3-322-46a-3c3%7C%7C10'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'n',
                'path': '/',
                'secure': False,
                'value': '%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6'},
                {'domain': '.meituan.com',
                'httpOnly': False,
                'name': 'u',
                'path': '/',
                'secure': False,
                'value': '625054939'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'uuid',
                'path': '/',
                'secure': False,
                'value': '5c24129c426d42eda0e7.1630899785.1.0.0'}]
        cookie = ''
        store_comments = []
        for page in range(page_count):
            strp = store_comment(poiid, page, cookie)
            if strp == '出错':
                t = 'https://wh.meituan.com/meishi/' + str(poiid)
                cookies_list = get_cookies(cookies_list, t)
                cookie = get_param_cookie(cookies_list)
                print(cookie)
                store_comment(poiid, page, cookie)
                cookie = cookie
            print(page)
df2 = pd.DataFrame(store_comments)
df2.to_excel('C:/Users/62491/desktop/wh美团c17店铺评论.xlsx')


