# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:19:35 2020

@author: ShenWeijie
"""


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd



def get_car_price_data(url):
    '''从url中获取价格信息列表
    '''
    doc = requests.get(url).text
    soup = bs(doc, 'html.parser', from_encoding='utf-8')
    table = soup.find('div', class_='search-result-list')
    return table



def get_price_info(table):
    '''从table中提取具体信息，返回DataFrame
    '''
    df = pd.DataFrame()
    item_list = table.find_all('div', class_='search-result-list-item')
    name_list = []
    price_low_list = []
    price_high_list = []
    img_url_list = []
    for item in item_list:
        name = item.find('p', class_='cx-name text-hover').text  # 车型名称
        price_range = item.find('p', class_='cx-price').text  # 车型价格
        # 部分车型价格没有最低，最高；设置最低=最高
        try:
            price_low = price_range.split('-')[0] + '万'
            price_high = price_range.split('-')[1]
        except IndexError:
            price_low = price_range
            price_high = price_range

        img_url = item.find('img', class_='img').attrs['src']  # 图片链接
        img_url = 'http:' + img_url

        name_list.append(name)
        price_low_list.append(price_low)
        price_high_list.append(price_high)
        img_url_list.append(img_url)

    df['车型名称'] = name_list
    df['最低价格'] = price_low_list
    df['最高价格'] = price_high_list
    df['产品图片链接'] = img_url_list

    return df



df_car_prices = pd.DataFrame()
base_url = 'http://car.bitauto.com/xuanchegongju/?mid=8&page='  # 基础网址
page_no = 3  # 需要爬取的页数
for page in range(1, page_no + 1):
    url = base_url+str(page)
    table = get_car_price_data(url)
    df_car_prices = df_car_prices.append(get_price_info(table), ignore_index=True)

# 保存文件
df_car_prices.to_csv('car_prices.csv', encoding='gbk')
