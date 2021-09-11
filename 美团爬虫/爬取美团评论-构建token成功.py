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

#初始化
def init():
    global store_comments, store_list, city,category,classification, url, user_agent, Cookie
    store_comments = []
    store_list = []
    city = 'wh'   #选择不同城市的首字母小写 'wh'=武汉
    category = 'meishi'  # 不同分类会有变化
    classification = 'c17' #代表美食下面的不同菜系分类 例如 火锅、自助餐、西餐、日韩料理等  不同的类别代表不同的编号  c17代表火锅
    area = '' #代表美食下面的不同区域分类 例如 洪山区、汉阳区、江汉区等  不同的类别代表不同的编号  b112代表洪山区
 
    url = 'https://' + city + '.meituan.com/' + category + '/' + classification + '/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    Cookie = '_lxsdk_cuid=17af4e0abd1c8-0f68456f1d5ddd-2343360-144000-17af4e0abd187; _hc.v=ebd8df08-051e-4ae2-9c7d-2e2c799cbaa1.1627874951; iuuid=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; cityname=%E5%8C%97%E4%BA%AC; _lxsdk=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; client-id=cade1835-02c3-408f-8413-f8fc8331058a; mtcdn=K; lsu=; uuid=4e4df34485d6405e913b.1630836233.1.0.0; ci=57; rvct=57%2C1%2C1124; lat=30.653038; lng=114.308028; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; __mta=213849771.1630830669377.1630858387148.1630858388564.8; u=625054939; n=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; lt=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; mt_c_token=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; token=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; token2=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; firstTime=1630858401856; unc=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; _lxsdk_s=17bb6881c33-b36-07f-0ef%7C%7C19'


def get_uuid():
    headers = {
        'user-agent': user_agent,
        'host': 'wh.meituan.com',
        'cookie': Cookie
    }
    resp = requests.get(url, headers=headers)
    text = resp.text
    findUUid = re.compile(r"uuid: '(.*?)',")
    findUserid = re.compile(r"userid: '(.*?)',")
    uuid = re.findall(findUUid,text)[0]
    userid = re.findall(findUserid,text)[0]
    if uuid and userid:
        return [uuid, userid]
    else:
        print('uuid和userid没有获得')


def get_sign(page_num):
    global uu_user_id
    uu_user_id = get_uuid()
    sign = "areaId=0&cateId=17&cityName=武汉&dinnerCountAttrId=&optimusCode=10&originUrl=https://wh.meituan.com/meishi/c17/pn%s&page=%s&partner=126&platform=1&riskLevel=1&sort=&userId=%s&uuid=%s"%(page_num, page_num, uu_user_id[1], uu_user_id[0])
    sign_ = zlib.compress(bytes(json.dumps(sign, ensure_ascii=False), encoding='utf-8'))
    sign_ = str(base64.b64encode(sign_), encoding='utf-8')
    return sign_


#破解token
def take_token(sign, page_num):
    ts = int(datetime.now().timestamp() * 1000)
    params = {
        'rId': 100900,
        'ver': '1.0.6',
        'ts': ts,
        'cts': ts + 100 * 1000,
        'brVD': [547,656],
        'brR': [[1536,864],[1536,824],24,24],
        'bI': [url + '/pn' + str(page_num), url + '/pn' + str(page_num-1)],
        'mT': [],
        'kT': [],
        'aT': [],
        'tT': [],
        'aM': '',
        'sign': sign
    }
    token_decode = zlib.compress(bytes(json.dumps(params, separators=(',', ':'), ensure_ascii=False), encoding="utf8"))
    token = str(base64.b64encode(token_decode), encoding="utf8")
    return token


cookies_list = [{'domain': '.meituan.com',
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
                'expiry': 1725454908,
                'httpOnly': False,
                'name': '_lxsdk_cuid',
                'path': '/',
                'secure': False,
                'value': '17bb60cf898c8-03a5f03aa7a584-c343365-144000-17bb60cf899c8'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'token2',
                'path': '/',
                'secure': False,
                'value': '-B5zoaiHzHkEZYKFOfPFsu4dzLUAAAAAcw4AAK2yknfIODXF7gcTEAbF77j0Uwl9MG3qC0sdKvD_7kpMFUqG2-0DA-CeSzeH5qAK5g'},
                {'domain': '.meituan.com',
                'expiry': 1662382908,
                'httpOnly': False,
                'name': '_hc.v',
                'path': '/',
                'secure': False,
                'value': 'bde8bb01-7f24-3544-015c-bcceec120b4f.1630846909'},
                {'domain': '.meituan.com',
                'expiry': 1631451698,
                'httpOnly': False,
                'name': 'mtcdn',
                'path': '/',
                'secure': False,
                'value': 'K'},
                {'domain': '.meituan.com',
                'expiry': 1632056507,
                'httpOnly': True,
                'name': 'lsu',
                'path': '/',
                'secure': False,
                'value': ''},
                {'domain': '.meituan.com',
                'expiry': 1725454908,
                'httpOnly': False,
                'name': '_lxsdk',
                'path': '/',
                'secure': False,
                'value': '17bb60cf898c8-03a5f03aa7a584-c343365-144000-17bb60cf899c8'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'token',
                'path': '/',
                'secure': False,
                'value': '-B5zoaiHzHkEZYKFOfPFsu4dzLUAAAAAcw4AAK2yknfIODXF7gcTEAbF77j0Uwl9MG3qC0sdKvD_7kpMFUqG2-0DA-CeSzeH5qAK5g'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'mt_c_token',
                'path': '/',
                'secure': False,
                'value': '-B5zoaiHzHkEZYKFOfPFsu4dzLUAAAAAcw4AAK2yknfIODXF7gcTEAbF77j0Uwl9MG3qC0sdKvD_7kpMFUqG2-0DA-CeSzeH5qAK5g'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'lt',
                'path': '/',
                'secure': False,
                'value': '-B5zoaiHzHkEZYKFOfPFsu4dzLUAAAAAcw4AAK2yknfIODXF7gcTEAbF77j0Uwl9MG3qC0sdKvD_7kpMFUqG2-0DA-CeSzeH5qAK5g'},
                {'domain': '.meituan.com',
                'httpOnly': False,
                'name': 'firstTime',
                'path': '/',
                'secure': False,
                'value': '1630846908837'},
                {'domain': '.meituan.com',
                'expiry': 1630933309,
                'httpOnly': True,
                'name': 'client-id',
                'path': '/',
                'secure': False,
                'value': '1e4c0e8d-f8a3-4fb5-aaac-60844700054b'},
                {'domain': '.meituan.com',
                'expiry': 1630848709,
                'httpOnly': False,
                'name': '_lxsdk_s',
                'path': '/',
                'secure': False,
                'value': '17bb60cf89a-4b1-462-968%7C%7C2'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'n',
                'path': '/',
                'secure': False,
                'value': '%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6'},
                {'domain': '.meituan.com',
                'httpOnly': True,
                'name': 'uuid',
                'path': '/',
                'secure': False,
                'value': 'de3b32a69a0e42f6b971.1630846898.1.0.0'},
                {'domain': '.meituan.com',
                'httpOnly': False,
                'name': 'u',
                'path': '/',
                'secure': False,
                'value': '625054939'}]
def get_cookies(url, cookies_list):
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
    time.sleep(10)
    for cookie in cookies_list:
        cookie['domain'] = '.meituan.com'
        driver.add_cookie(cookie)
    driver.get(url)
    driver.refresh()
    time.sleep(10)
    cookies_list1 = driver.get_cookies()
    return cookies_list1


def get_param_cookie(cookies):
    cookie_str = ""
    for item_cookie in cookies:
        item_str = item_cookie["name"] + "=" + item_cookie["value"] + "; "
        cookie_str += item_str
        cookie = cookie_str[:-2]
        return cookie

# 获取不同店铺的数据
def get_store(page, token):
    headers = {
        'user-agent': user_agent,
        'host': 'wh.meituan.com',
        'referer': 'https://wh.meituan.com/meishi/c17/pn' + str(page) + '/',
        'cookie': Cookie,
    }
    params = {
        'cityName': '武汉',
        'cateId': '17',
        'areaId': '0',
        'sort': '',
        'dinnerCountAttrId': '',
        'page': str(page),
        'userId': uu_user_id[1],
        'uuid': uu_user_id[0],
        'platform': '1',
        'partner': '126',
        'originUrl': headers['referer'],
        'riskLevel': '1',
        'optimusCode': '10',
        '_token': token
    }
    base_url = 'https://wh.meituan.com/meishi/api/poi/getPoiList?'
    try:
        response = requests.get(url=base_url, headers=headers, params=params)
        json = response.json()
        poiInfos = json.get('data').get('poiInfos')
        for info in poiInfos:
            del info['dealList']
            store_list.append(info)
    except Exception as e:
        print('爬取第 %s 页商铺信息出错'%page)






def store_comment(store, cookie):
    poiid = store['poiId']
    allCommentNum = store['allCommentNum']
    page_count = math.ceil(allCommentNum/10)
    if page_count > 0:
        for page in range(page_count):
            headers = {
                'user-agent': user_agent,
                'host': 'wh.meituan.com',
                'referer': 'https://wh.meituan.com/meishi/%s/'%poiid,
                'cookie': cookie,
            }
            store_url = 'https://%s.meituan.com/meishi/api/poi/getMerchantComment?'%city
            params = {
                'uuid': uu_user_id[0],
                'platform': '1',
                'partner': '126',
                'originUrl': 'https://%s.meituan.com/%s/%s/'%(city, category, poiid),
                'riskLevel': '1',
                'optimusCode': '10',
                'id': str(poiid),
                'userId': uu_user_id[1],
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
            except Exception as e:
                print('爬取 %s 商铺信息评论第 %s 页出错'%(poiid, page),e)
            time.sleep(random.randint(0,8))

    
    
if __name__ == '__main__':
    init()
    for i in range(1,5):
        sign = get_sign(i)
        token = take_token(sign, i)
        get_store(i, token)
        time.sleep(random.randint(0,10))
    df = pd.DataFrame(store_list)
    df.to_excel('C:/Users/62491/desktop/' + city + '美团'+ classification + '店铺.xlsx', index = False)
    cookie = '_lxsdk_cuid=17af4e0abd1c8-0f68456f1d5ddd-2343360-144000-17af4e0abd187; _hc.v=ebd8df08-051e-4ae2-9c7d-2e2c799cbaa1.1627874951; iuuid=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; cityname=%E5%8C%97%E4%BA%AC; _lxsdk=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; client-id=cade1835-02c3-408f-8413-f8fc8331058a; mtcdn=K; lsu=; uuid=4e4df34485d6405e913b.1630836233.1.0.0; ci=57; rvct=57%2C1%2C1124; lat=30.653038; lng=114.308028; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; __mta=213849771.1630830669377.1630858387148.1630858388564.8; u=625054939; n=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; lt=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; mt_c_token=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; token=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; token2=pG9wnETFH0dcUuaqzqE0ZPBNBHYAAAAAcw4AAHodFWu45H9PrvNAH3fTWCakjkE69C3d0ng7IDFU-RMnD9IsEXZLS9p8yV8xLHNNAw; firstTime=1630858401856; unc=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; _lxsdk_s=17bb6881c33-b36-07f-0ef%7C%7C19'
    for store in store_list:
        poiid = store['poiId']
        t = url + str(poiid)
        try:
            store_comment(store, cookie)
        except Exception as e:
            cookies_list = get_cookies(t, cookies_list)
            cookies = get_param_cookie(cookies_list)
            store_comment(store, cookies)
    df2 = pd.DataFrame(store_comments)
    df2.to_excel('C:/Users/62491/desktop/' + city + '美团店铺评论.xlsx', index = False)



