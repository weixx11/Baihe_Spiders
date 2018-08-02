#!/usr/bin/env python
#coding=utf-8

from bs4 import BeautifulSoup
import requests
import time
import json
import os

from urllib.parse import quote  #编码
from urllib.parse import unquote  #解码

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36',
    'referer': 'http://www.baihe.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

#登录请求
r1 = requests.post(
    url = 'http://my.baihe.com/Getinterlogin/gotoLogin?jsonCallBack=jQuery18308807729283968166_%d&'%(time.time()*1000),
    headers = headers,
    data = {
        # 'txtLoginEMail': "13163339526",
        'txtLoginEMail': "18162963383",
        'txtLoginPwd': "466547071",
        'chkRememberMe': "",
        'codeId': "",
        'codeValue': '',
        'event':'3',
        'spmp':'4.20.53.225.685',
        '_': "%d"%(time.time()*1000)
    },
)

print(r1.text)

cookies_dict1 = r1.cookies.get_dict()  #获取登录后的cookies

age_list = ['18-25','26-30','31-40','41-50','51-60','61-85']
img_urls = []
for age in age_list:   #根据年龄来进行分类
    # print('man/'+age)
    # dir_path = './images/female/'+age
    dir_path = './images/man/'+age
    if not os.path.exists(dir_path):   #如果目录不存在则创建
        print(dir_path)
        os.mkdir(dir_path)
    ages = age.split('-')
    # print(ages[0])
    # print(ages[-1])
    #该网站各省份对应的ID
    city_dict = {"北京": 8611, '天津': 8612, '河北': 8613, '山西': 8614, '内蒙古': 8615, '辽宁': 8621, '吉林': 8622, '黑龙江': 8623,
            '上海': 8631, '江苏': 8632, '浙江': 8633, '安徽': 8634,
            '福建': 8635, '江西': 8636, '山东': 8637, '河南': 8641, '湖北': 8642, '湖南': 8643, '广东': 8644, '广西': 8645, '海南': 8646,
            '重庆': 8650, '四川': 8651, '贵州': 8652,
            '云南': 8653, '西藏': 8654, '陕西': 8661, '甘肃': 8662, '青海': 8663, '宁夏': 8664, '新疆': 8665, '台湾': 8671, '香港': 8681,
            '澳门': 8682, '钓鱼岛': 8683, }
    for city in city_dict:  #根据城市来下载
        city_id = city_dict[city]   #获取城市ID
        for page in range(1,50):
            #根据年龄，页码，省份来调整参数
            params = '{"appId":"1","channel":"appstore","device":"android","apver":"5.8.0","accessToken":"12546879","IMEI":"","minAge":"%s","maxAge":"%s","minHeight":"144","maxHeight":"210","city":"","province":"%s","education":"","income":"","page":"%s","pageSize":"6"}' %(ages[0],ages[-1],city_id,page)
            print(params)
            # params = '{"appId":"1","channel":"appstore","device":"android","apver":"5.8.0","accessToken":"12546879","IMEI":"",minAge":"18","maxAge":"20","minHeight":"144","maxHeight":"211","city":"","province":"8652","education":"","income":"","page":"1","pageSize":"6"}'

            params_quote = (quote(params))  #给该参数进行URL转义
            # print(params)
            url = 'http://i.baihe.com/search/search?traceID=1&systemID=2&params={0}'.format(params_quote)
            # print(url)
            #url的样式，参数后面进行了URL转义
            # url = 'http://i.baihe.com/search/search?traceID=1&systemID=2&params=%7B%22appId%22%3A%221%22%2C%22channel%22%3A%22appstore%22%2C%22device%22%3A%22android%22%2C%22apver%22%3A%225.8.0%22%2C%22accessToken%22%3A%2212546879%22%2C%22IMEI%22%3A%22%22%2C%22minAge%22%3A%2218%22%2C%22maxAge%22%3A%2265%22%2C%22minHeight%22%3A%22144%22%2C%22maxHeight%22%3A%22211%22%2C%22city%22%3A%22%22%2C%22province%22%3A%228652%22%2C%22education%22%3A%22%22%2C%22income%22%3A%22%22%2C%22page%22%3A%221%22%2C%22pageSize%22%3A%226%22%7D'
            # print(url)
            #登录成功后的搜索接口
            r2 = requests.get(
                url=url,
                cookies=cookies_dict1,
                headers = headers
            )

            # print(r1.apparent_encoding)
            # data = r2.text["data"]
            try:
                data = json.loads(r2.text)
                # print(len(data))
                # # print(data['data'])
                # # print(len(data['data']))
                data_res = data['data']
                print('第%s页'%page,len(data_res['result']))
                for i in data_res['result']:
                    # print(len(i))
                    provinceChn = i['provinceChn']   #省份
                    img_url = i['headPhotoUrl_100_100']  #100*100的图片
                    age_true = i['age']   #填写的年龄
                    # print(age_true,'age区间:',ages[0],ages[-1])

                    # if age[0] <=age_true<= age[-1]:   #判断填写的年龄是否在查找的区间，
                        # print(img_urls)
                        # print(img_url)
                    if img_url not in set(img_urls):   #去重
                        img_urls.append(img_url)
                        img_name = img_url.split('/')
                        img_name = img_name[-1]
                        file_name_path = dir_path + '/' + img_name
                        print("age:",age,"城市:",city,"页数:",page,"imageURL:",img_url,'真实省:',provinceChn,'真实年龄:',age_true)
                        try:
                            #下载图片
                            ret_img = requests.get(
                                url= img_url
                            )
                        except Exception:
                            pass
                        with open(file_name_path, 'wb') as f:
                            f.write(ret_img.content)
                    else:
                        print("已经存在",img_url)
                    # else:
                    #     print("Age不在符合区间")
            except Exception:
                pass