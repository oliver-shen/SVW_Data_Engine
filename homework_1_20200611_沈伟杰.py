# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:55:01 2020

@author: ShenWeijie
"""


import pandas as pd
import numpy as np

# Action_1:求2+4+6+8+...+100的求和，用Python该如何写
print('Action_1:求2+4+6+8+...+100的求和，用Python该如何写')
print(sum(range(2, 101, 2)))

# Action_2:统计全班的成绩
df = pd.DataFrame({'姓名': ['张飞', '关羽', '刘备', '典韦', '许褚'],
                   '语文': [68, 95, 98, 90, 80],
                   '数学': [65, 76, 86, 88, 90],
                   '英语': [30, 98, 88, 77, 90]})

print('Action_2:统计全班的成绩')
# 平均成绩
print('平均成绩：')
print(df.iloc[:, 1:].mean(axis=0))
# 最小成绩
print('最小成绩：')
print(df.iloc[:, 1:].min(axis=0))
# 最大成绩
print('最大成绩：')
print(df.iloc[:, 1:].max(axis=0))
# 方差
print('方差：')
print(df.iloc[:, 1:].var(axis=0))
# 标准差
print('标准差：')
print(df.iloc[:, 1:].std(axis=0))
# 总成绩排序
df['总成绩'] = df.iloc[:, 1:].sum(axis=1)
print('总成绩排名：')
print(df.sort_values(by='总成绩', ascending=False))

# Action_3:对汽车质量数据进行统计
print('Action_3:对汽车质量数据进行统计')
file = r'car_complain.csv'
df_car = pd.read_csv(file)
# 拆分problem类型 => 多个字段，保留原'problem'列
df_car = df_car.join(df_car.problem.str.get_dummies(','))
'''只计算投诉次数，不计问题数量'''
# 品牌投诉总数
df_car['投诉次数'] = 1
result_1 = df_car.groupby('brand').agg(np.sum)
result_1 = result_1['投诉次数'].sort_values(ascending=False)
print('品牌投诉总数排名：')
print(result_1)
# 车型投诉总数
result_2 = df_car.groupby('car_model').agg(np.sum)
result_2 = result_2['投诉次数'].sort_values(ascending=False)
print('车型投诉总数排名：')
print(result_2)
# 平均车型投诉
result_3 = df_car.groupby('brand').agg(np.sum)
result_ = df_car.groupby(['brand', 'car_model']).count().groupby('brand').count()
result_3['车型数'] = result_['id']
result_3['平均车型投诉次数'] = result_3['投诉次数']/result_['id']
result_3 = result_3['平均车型投诉次数'].sort_values(ascending=False)
print('平均车型投诉数排名：')
print(result_3)

'''计问题数量'''
df_car_2 = df_car.copy(deep=True)
df_car_2['问题数量'] = [x.count(',') for x in df_car_2['problem']]
# 品牌问题总数
result_4 = df_car_2.groupby('brand').agg(np.sum)
result_4 = result_4['问题数量'].sort_values(ascending=False)
print('品牌问题总数排名：')
print(result_4)
# 车型问题总数
result_5 = df_car_2.groupby('car_model').agg(np.sum)
result_5 = result_5['问题数量'].sort_values(ascending=False)
print('车型问题总数排名：')
print(result_5)
# 平均车型问题
result_6 = df_car_2.groupby('brand').agg(np.sum)
result_ = df_car_2.groupby(['brand', 'car_model']).count().groupby('brand').count()
result_6['车型数'] = result_['id']
result_6['平均车型问题数'] = result_6['问题数量']/result_['id']
result_6 = result_6['平均车型问题数'].sort_values(ascending=False)
print('平均车型问题数排名：')
print(result_6)
