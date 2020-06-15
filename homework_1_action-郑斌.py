#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


# In[ ]:


import pandas as pd


# In[ ]:


a = np.array(range(2,102,2))


# In[ ]:


Action1 = np.sum(a)
print('2+4+6+8+...+100 = ',Action1)


# In[ ]:


b = {'语文':[68,95,98,90,80],'数学':[65,76,86,88,90],'英语':[30,98,88,77,90]}


# In[ ]:


df_b = pd.DataFrame(b,index=['张飞','关羽','刘备','典韦','许褚'])
df_b.index.name = '姓名'


# In[ ]:


print('各学科平均成绩：')
print(df_b.mean())


# In[ ]:


print('各学科最小成绩：')
print(df_b.min())


# In[ ]:


print('各学科最大成绩：')
print(df_b.max())


# In[ ]:


print('各学科成绩方差：')
print(df_b.var())


# In[ ]:


print('各学科最大标准差：')
print(df_b.std())


# In[ ]:


df2_b = pd.DataFrame(df_b.sum(axis=1),columns=['总分'])
df2_b = df2_b.sort_values('总分',ascending=False)
print('总分排序：')
print(df2_b)


# In[ ]:


df = pd.read_csv('C:/Users/ZhengBin2/Desktop/Data_Engine_with_Python-master/L1/car_data_analyze/car_complain.csv')
df


# In[ ]:


df2_problem = df.join(df.problem.str.get_dummies(','))
df2_problem


# In[ ]:


df2 = df2_problem.groupby(['brand'])['id'].agg(['count'])
df2 = df2.sort_values('count',ascending=False)
print('品牌投诉总数：')
print(df2)


# In[ ]:


df3 = df2_problem.groupby(['car_model'])['id'].agg(['count'])
df3 = df3.sort_values('count',ascending=False)
print('车型投诉总数：')
print(df3)


# In[ ]:


df4 = df2_problem.groupby(['brand','car_model'])['id'].agg(['count']).groupby(['brand']).mean()
df4 = df4.sort_values('count',ascending=False)
print('品牌平均车型投诉数：')
print(df4)

