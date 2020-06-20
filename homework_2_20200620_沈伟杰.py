# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 18:05:46 2020
从车质网上爬取投诉信息
@author: ShenWeijie
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_car_complaints_data(url):
    '''从网址中获取投诉信息table
    '''
    doc = requests.get(url).text
    soup = bs(doc, 'html.parser', from_encoding='utf-8')
    table = soup.find('div', class_='tslb_b')
    return table


def get_complaint_info(table):
    '''从table中提取具体信息，返回DataFrame
    '''
    df = pd.DataFrame()
    tr_list = table.find_all('tr')
    for tr in tr_list:
        try:
            # 第一行为表头，无td标签
            id_, brand_, car_model_, type_, desc_, problem_, datetime_, status_ = tr.find_all(
                'td')
            df_tmp = pd.DataFrame([id_.text, brand_.text, car_model_.text, type_.text,
                                   desc_.text, problem_.text, datetime_.text, status_.text]).transpose()
            df = df.append(df_tmp)
        except ValueError:
            pass
    return df


# 网址通过page递增来循环
base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-'
url_suffix = '.shtml'
df_car = pd.DataFrame()
page_no = 3  # 需要爬取的页数
for page in range(1, page_no):
    url = base_url + str(page) + url_suffix
    table = get_car_complaints_data(url)
    df_car = df_car.append(get_complaint_info(table))

# 重命名列
columns = ['投诉编号', '投诉品牌', '投诉车系', '投诉车型', '问题简述', '典型问题', '投诉时间', '投诉状态']
df_car.columns = columns
df_car.to_excel('车质网投诉信息.xls')
