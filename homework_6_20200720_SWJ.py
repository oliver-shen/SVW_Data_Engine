# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 20:59:09 2020

@author: ShenWeijie
"""

import pandas as pd
from itertools import product
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import timedelta
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 数据加载
df = pd.read_csv('train.csv')
df = df[['Datetime', 'Count']]

# 将时间作为df的索引
df.Datetime = pd.to_datetime(df.Datetime, format='%d-%m-%Y %H:%M')
df.index = df.Datetime

# 按照日统计
df_day = df.resample('D').sum()
df_x = df_day.index

# 设置参数范围
ps = range(16, 18)  # 经过试验，ps取值>15时预测比较准确
ds = range(0, 3)
# 对原始数据进行周期分解，发现freq=7时，seasonal曲线比较光滑，residual范围较小；直接设置qs=7，减少循环次数
# result = sm.tsa.seasonal_decompose(df_day.Count, freq=7)
qs = range(7, 8)
parameters = product(ps, ds, qs)
parameters_list = list(parameters)
# 寻找最优ARMA模型参数，即best_aic最小,最优模型保存为best_model
results = []
best_aic = float("inf")  # 正无穷
for param in parameters_list:
    try:
        model = sm.tsa.statespace.SARIMAX(df_day.Count,
                                          order=(param[0], param[1], param[2]),
                                          enforce_stationarity=False,
                                          enforce_invertibility=False).fit()
    except ValueError:
        print('参数错误:', param)
        continue
    aic = model.aic
    if aic < best_aic:
        best_model = model
        best_aic = aic
        best_param = param
    results.append([param, model.aic])
# 输出最优模型
print('最优模型: ', best_model.summary())

# 设置future_day，需要预测的时间date_list
df_day_2 = df_day[['Count']]
last_day = pd.to_datetime(df_day_2.index[len(df_day_2)-1])
begin_date = last_day + timedelta(days=1)
end_date = begin_date + timedelta(days=213)


def get_date_list(begin_date, end_date):
    '''
    返回从begin_date到end_date中间的时间序列（包含）
    Parameters
    ----------
    begin_date : datetime
        起始日期.
    end_date : datetime
        结束日期.

    Returns
    -------
    date_list : list
        日期序列的list

    '''
    date_list = [x.strftime('%Y-%m-%d %H:%M') for x in list(pd.date_range(start=begin_date, end=end_date))]
    return date_list


# 生成需要预测的日期序列
predict_date = pd.to_datetime(get_date_list(begin_date, end_date), format='%Y-%m-%d %H:%M')
# 计算预测值
df_day_forecast = best_model.predict(start=begin_date, end=end_date, dynamic=True)
df_day_forecast = pd.DataFrame(df_day_forecast)
df_day_forecast.columns = ['Count']

# 列车人次预测结果显示
ax = sns.lineplot(x=df_x, y=df_day_2.Count, label='实际人次')
ax_2 = sns.lineplot(x=predict_date, y=df_day_forecast.Count, label='预测人次')
plt.title('列车乘坐人次')
plt.xlabel('时间')
plt.ylabel('人次')
plt.show()
