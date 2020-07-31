# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 17:09:14 2020

@author: ShenWeijie
"""


from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import pandas_profiling as pp
import time

start = time.time()  # 程序开始时间
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 1.数据加载
file_name_absolute = r'D:\work\MQSS-2\MQSS-2工作文件\2020长期任务\10.SVW Data Engine 数据分析训练营\数据分析训练营-结营考试\ProjectC\CarPrice_Assignment.csv'
file_name_relative = r'CarPrice_Assignment.csv'
df = pd.read_csv(file_name_relative)


# 2.数据探索
# 使用pandas_profiling进行数据基本探索，文件保存为data_overview_output.html
'''
# Warning:运行时间较长，文件已保存
profile = pp.ProfileReport(df)
profile.to_file(r"data_overview_output.html")
'''
# 查看profile report，未发现缺失值、重复行；
# 部分列（citympg/highwaympg，fueltype/fuelsystem）是High correlation，后续可以做降维处理；
# CarName和car_ID不作为特征列处理


# 3.数据预处理
X_train = df.drop(['car_ID', 'CarName'], axis=1)
# 气缸数转换为int
X_train['cylindernumber'].replace(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'], range(1,13), inplace=True)
# 其余为类别类型的特征，需要做热编码
# 列重排序，将需要做热编码的列放在最后
column_order = ['symboling', 'wheelbase', 'carlength', 'carwidth', 'carheight', 'curbweight', 'cylindernumber', 'enginesize', 'boreratio', 'stroke', 'compressionratio', 'horsepower', 'peakrpm', 'citympg', 'highwaympg', 'price', 'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'fuelsystem']
X_train = X_train[column_order]
# 热编码处理
columns_onehotencode = ['fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'fuelsystem']  # 需要做热编码的列
X = X_train[columns_onehotencode]
result = OneHotEncoder(categories='auto').fit_transform(X).toarray()
X_train = pd.concat([X_train, pd.DataFrame(result)], axis=1)
X_train.drop(columns_onehotencode, axis=1, inplace=True)
# 数据标准化（数据大部分接近正态分布，因此使用StandardScaler）
scaler = preprocessing.StandardScaler()
X_train.iloc[:, 0:16] = scaler.fit_transform(X_train.iloc[:, 0:16])
X_train['price'] = X_train['price'] * 3  # 做竞品分析时，*价格*权重适当放大


# 4.选择聚类模型并训练、使用
# K-Means聚类并评估，设置合适的K值，综合轮廓系数&簇内误方差
silhouette_score = []  # 轮廓系数
SSE = []  # 簇内误方差
for i in range(2, 20):
    n_clusters = i
    clf = KMeans(n_clusters=n_clusters, init='k-means++').fit(X_train)
    Y_pred = clf.labels_
    silhouette_score.append(metrics.silhouette_score(X_train, Y_pred))
    SSE.append(clf.inertia_)
# 画图并寻找合适的K值
plt.subplot(2, 1, 1)
plt.plot(range(2, 20), silhouette_score, marker='^')
plt.ylabel('轮廓系数-silhouette_score')
plt.subplot(2, 1, 2)
plt.plot(range(2, 20), SSE, marker='o')
plt.ylabel('SSE-簇内误方差')
# 综合轮廓系数&簇内误方差，设置K=10，并进行聚类
n_clusters = 10
clf = KMeans(n_clusters)
Y_pred = clf.fit_predict(X_train)
df['Cluster_ID'] = Y_pred
df_trimmed = df[['CarName', 'Cluster_ID']]


# 5.竞品分析
# 与volkswagen同属一类的作为竞品
df_vw = df_trimmed[df_trimmed['CarName'].str.contains('vw') | df_trimmed['CarName'].str.contains('volkswagen') | df_trimmed['CarName'].str.contains('vokwagen')]  # vw车型为CarName中包含了vw/volkswage/vokwagen的行
vw_cluster = df_vw['Cluster_ID'].unique()  # 筛选vw车型属于的类别
df_competitors = df_trimmed[[i in vw_cluster for i in df_trimmed['Cluster_ID']]]
# 输出竞品车型
for i in vw_cluster:
    CarNames = df_competitors[df_competitors['Cluster_ID'] == i]
    print('=' * 55)
    print('=' * 20, 'ClusterID: ', i, '=' * 20)
    print(CarNames['CarName'])


end = time.time()  # 程序结束时间
running_time = str(round(end - start, 4)) + 's'
print('running time: ' + running_time)
