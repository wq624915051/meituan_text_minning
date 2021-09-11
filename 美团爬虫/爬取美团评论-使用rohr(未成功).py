from numpy.core.numeric import base_repr
import requests
from urllib import parse
from pyquery import PyQuery as pq
import pandas as pd
import os
import time
import random
from selenium import webdriver
import re

#初始化
def init():
    global store_url, store_list, city, url, file_path, user_agent, cookie
    store_url = []
    store_list = []
    city = 'wh'   #选择不同城市的首字母小写 'wh'=武汉
    category = 'meishi'  # 不同分类会有变化
    classification = 'c17' #代表美食下面的不同菜系分类 例如 火锅、自助餐、西餐、日韩料理等  不同的类别代表不同的编号  c17代表火锅
    area = '' #代表美食下面的不同区域分类 例如 洪山区、汉阳区、江汉区等  不同的类别代表不同的编号  b112代表洪山区
    file_path = "C:/Users/62491/desktop/"
 
    url = 'https://' + city + '.meituan.com/' + category + '/' + classification + '/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    cookie = '_lxsdk_cuid=17af4e0abd1c8-0f68456f1d5ddd-2343360-144000-17af4e0abd187; lsu=; _hc.v=ebd8df08-051e-4ae2-9c7d-2e2c799cbaa1.1627874951; iuuid=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; cityname=%E5%8C%97%E4%BA%AC; _lxsdk=E0F15A727A308745C86B34DD5EA5F9A55B5457E57AE060DD55719E2DA904E155; ci=57; rvct=57%2C1124%2C1; mtcdn=K; client-id=aa30c147-6677-4579-b2db-b40fe6543be4; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; uuid=1387fa52d53a496bb694.1628822981.1.0.0; userTicket=lzejKbPxWxxKFTEpxwJFvXXSvbfplxUgwGMxRwah; __mta=55538196.1627606094437.1628867434387.1628868201102.27; u=625054939; n=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; lt=6YVhNqYkIlWt5USB_EY5fySM6JoAAAAAUg4AAK36A3G3evQ92yxL5Y_l62KwiekWEYbYNaliag9hPVDbuS2OLXxM4KHjNISxlWKoAg; mt_c_token=6YVhNqYkIlWt5USB_EY5fySM6JoAAAAAUg4AAK36A3G3evQ92yxL5Y_l62KwiekWEYbYNaliag9hPVDbuS2OLXxM4KHjNISxlWKoAg; token=6YVhNqYkIlWt5USB_EY5fySM6JoAAAAAUg4AAK36A3G3evQ92yxL5Y_l62KwiekWEYbYNaliag9hPVDbuS2OLXxM4KHjNISxlWKoAg; token2=6YVhNqYkIlWt5USB_EY5fySM6JoAAAAAUg4AAK36A3G3evQ92yxL5Y_l62KwiekWEYbYNaliag9hPVDbuS2OLXxM4KHjNISxlWKoAg; firstTime=1628868215939; unc=%E7%8E%8B%E7%8E%8B%E7%90%A6%E7%90%A6%E7%90%A6; _lxsdk_s=17b40108f1b-63e-2ba-c2%7C%7C27'


def get_uuid():
    headers = {
        'user-agent': user_agent,
        'host': 'wh.meituan.com',
        'cookie': cookie
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

#破解token
def take_token(page_num, uuid, userid):
    jv = 'https://wh.meituan.com/meishi/api/poi/getPoiList?cityName=武汉&cateId=17&areaId=0&sort=&dinnerCountAttrId=&page=%s&userId=%s&uuid=%s&platform=1&partner=126&originUrl=%spn%s&riskLevel=1&optimusCode=10'%(page_num, userid, uuid, url, page_num)
    path = file_path + 'rohr-1.html'
    with open(path) as f:
        f.read().replace("bbbb",jv)
    try:
        browser = webdriver.Chrome()
        browser.get(url= path)
    # token_data = browser.execute_script('return meituan_token()', jv)   # 这里使用execute_script调用了ssss函数，并传入参数jv
        token_data = browser.title
        time.sleep(5)
        browser.close()
        return token_data
    except Exception as e:
        print('打开网页出错')

# 获取不同店铺的数据
def get_store(page, uuid, userid, token):
    headers = {
        'user-agent': user_agent,
        'host': 'wh.meituan.com',
        'referer': 'https://wh.meituan.com/meishi/c17/pn' + str(page) + '/',
        'cookie': cookie,
    }
    params = {
        'cityName': '武汉',
        'cateId': '17',
        'areaId': '0',
        'sort': '',
        'dinnerCountAttrId': '',
        'page': str(page),
        'userId': userid,
        'uuid': uuid,
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
        print('爬取商铺信息出错')
    
    
if __name__ == '__main__':
    init()
    user_uu_id = get_uuid()
    token = take_token(1, user_uu_id[0], user_uu_id[1])
    get_store(1, user_uu_id[0], user_uu_id[1], token)
    df = pd.DataFrame(store_list, columns=["商家信息"])
    df.to_excel('美团.xlsx')

