# -*- coding: utf-8 -*-
"""
Created on Sat Jun 26 10:18:39 2021

@author: Liu_YK d20091100124@cityu.mo
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import numpy as np
import pandas as pd

# BV2AV AV2BV
# https://blog.csdn.net/jkddf9h8xd9j646x798t/article/details/105124465
alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

def dec(x):
    
    r = 0
    for i, v in enumerate([11, 10, 3, 8, 4, 6]):
        r += alphabet.find(x[v]) * 58**i
    return (r - 0x2_0840_07c0) ^ 0x0a93_b324

def enc(x):
    
    x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
    r = list('BV1**4*1*7**')
    for v in [11, 10, 3, 8, 4, 6]:
        x, d = divmod(x, 58)
        r[v] = alphabet[d]
    return ''.join(r)

# no need!
def getMid(bv):
    
    headers = {
        'authority': 'api.bilibili.com',
        #'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        #'dnt': '1',
        #'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
        #'accept': '*/*',
        #'sec-fetch-site': 'same-site',
        #'sec-fetch-mode': 'no-cors',
        #'sec-fetch-dest': 'script',
        #'referer': 'https://www.bilibili.com/video/BV117411m7Rt?from=search&seid=2289752195809960197',
        'referer': 'https://www.bilibili.com',
        #'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        #'$cookie': '_uuid=A712F69C-90BE-44A4-642C-DA0CD696827488760infoc; buvid3=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(ku|kmm~kRR0J\'uYum)lYk|k; sid=5y2hk6o3; buvid_fp=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; buvid_fp_plain=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; DedeUserID=32178580; DedeUserID__ckMd5=f9e7a3766e37742f; SESSDATA=f091cd7d%2C1635413829%2Cee2cd*51; bili_jct=7dd63b1ef215b1dfdcd769fe88ce35c7; LIVE_BUVID=AUTO9416207851793813; fingerprint3=e33c2a77f63b1b97036339e74e5baef4; fingerprint=da1befcc7a60b6f195fa71747a0a933c; fingerprint_s=74b09d6adf696ce89bc2e7b704640356; CURRENT_QUALITY=112; PVID=2; bsource=search_bing; bfe_id=018fcd81e698bbc7e0648e86bdc49e09',
    }
    
    now_time = int(time.time() * 1000)
    params = (
        ('callback', 'jQuery33105450292163562576_' + str(now_time)),
        ('jsonp', 'jsonp'),
        ('next', '0'),
        ('type', '1'),
        ('oid', dec(bv)),#588676861  630756505
        ('mode', '3'),
        ('plat', '1'),
        ('_', str(int(time.time() * 1000))),
    )
    
    proxy = 'http:\\\\' +  '42.56.239.217' + ':' + '9999'
    proxies = {'proxy':proxy}
    response = requests.get('https://api.bilibili.com/x/v2/reply/main', headers=headers, params=params, proxies = proxies)

    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('https://api.bilibili.com/x/v2/reply/main?callback=jQuery33105450292163562576_1624525906853&jsonp=jsonp&next=0&type=1&oid=98669654&mode=3&plat=1&_=1624525906854', headers=headers)

    rsp_str = response.text.replace('jQuery33105450292163562576_' + str(now_time) + "(", '').strip(')')
    data = json.loads(rsp_str)
    
    mid = data['data']['upper']['mid']
    print("mid:", mid)
    
    return mid

# API随时变动，此方法随时失效
def getCid(bv):
    
    headers = {
        'authority': 'api.bilibili.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'accept': '*/*',
        'dnt': '1',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
        'origin': 'https://www.bilibili.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.bilibili.com',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        #'$cookie': '_uuid=A712F69C-90BE-44A4-642C-DA0CD696827488760infoc; buvid3=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(ku|kmm~kRR0J\'uYum)lYk|k; sid=5y2hk6o3; buvid_fp=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; buvid_fp_plain=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; DedeUserID=32178580; DedeUserID__ckMd5=f9e7a3766e37742f; SESSDATA=f091cd7d%2C1635413829%2Cee2cd*51; bili_jct=7dd63b1ef215b1dfdcd769fe88ce35c7; LIVE_BUVID=AUTO9416207851793813; fingerprint3=e33c2a77f63b1b97036339e74e5baef4; fingerprint=da1befcc7a60b6f195fa71747a0a933c; fingerprint_s=74b09d6adf696ce89bc2e7b704640356; CURRENT_QUALITY=112; PVID=3; bsource=search_bing; bfe_id=5db70a86bd1cbe8a88817507134f7bb5',
    }
    
    params = (
        ('bvid', bv),
        ('jsonp', 'jsonp'),
    )

    response = requests.get('https://api.bilibili.com/x/player/pagelist', headers=headers, params=params)
    
    data = json.loads(response.text)
    
    cid = data["data"][0]["cid"]
    
    return cid


def getDm(bv):
    
    dm = []
    headers = {
        'authority': 'comment.bilibili.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        #'$cookie': '_uuid=A712F69C-90BE-44A4-642C-DA0CD696827488760infoc; buvid3=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(ku|kmm~kRR0J\'uYum)lYk|k; sid=5y2hk6o3; buvid_fp=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; buvid_fp_plain=7B426128-CEB3-467C-AEC7-B23EDD035E9934770infoc; DedeUserID=32178580; DedeUserID__ckMd5=f9e7a3766e37742f; SESSDATA=f091cd7d%2C1635413829%2Cee2cd*51; bili_jct=7dd63b1ef215b1dfdcd769fe88ce35c7; LIVE_BUVID=AUTO9416207851793813; fingerprint3=e33c2a77f63b1b97036339e74e5baef4; fingerprint=da1befcc7a60b6f195fa71747a0a933c; fingerprint_s=74b09d6adf696ce89bc2e7b704640356; CURRENT_QUALITY=112; PVID=3',
        #'if-modified-since': 'Sat, 26 Jun 2021 11:34:26 GMT',
    }

    # set proxy
    proxy = 'http:\\\\' +  '58.255.199.192' + ':' + '9999'
    proxies = {'proxy':proxy}
    
    # https://comment.bilibili.com/{5771902}.xml
    # 这里是cid，非oid(av)/mid
    response = requests.get('https://comment.bilibili.com/' + str(getCid(bv)) + '.xml', headers=headers, proxies = proxies)
    
    # !!!!
    pagetext = response.content.decode("utf-8")
    print(pagetext)
    
    soup = BeautifulSoup(pagetext, 'lxml')
    
    with open(bv + '_dm.txt', 'w', encoding='utf-8') as fp:
        
        for i in soup.find_all('d'):
            print(i.text)
            fp.write(i.text + '\n')
            dm.append(i.text)
    
    return dm

bv = input('请输入bv号：')
dm = getDm(bv)

dm_np = np.array(dm)
dm_pd = pd.DataFrame(dm_np)

dm_pd.to_csv(bv + "_dm" + ".csv", encoding='utf-8-sig') 
            