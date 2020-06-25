# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 17:51:50 2020

@author: ShenWeijie
"""


import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

file_name = r'car_data.csv'
df = pd.read_csv(file_name, encoding='gbk')


train_x = df[['人均GDP', '城镇人口比重', '交通工具消费价格指数', '百户拥有汽车量']]


# 规范化到 [0,1] 空间
min_max_scaler = MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)

# 使用KMeans聚类
predict_y = KMeans(n_clusters=4).fit_predict(train_x)

# 合并聚类结果，插入到原数据中
result = pd.concat((df, pd.DataFrame(predict_y)), axis=1)
result.rename({0: u'K-Means聚类结果'}, axis=1, inplace=True)
print(result)

# 将结果导出到CSV文件中
result.to_csv("customer_cluster_result.csv", index=False, encoding='gbk')
