# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 09:09:05 2020

@author: ShenWeijie
"""


import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
import time
import matplotlib.pyplot as plt


start = time.time()  # 程序开始时间


# 1.数据导入
order_table = pd.read_csv('订单表.csv', encoding='gbk')


# 2.数据格式整理，保留*产品名称*，*客户ID*两列
df = order_table[['产品名称', '客户ID']].astype(str)
# 根据*客户ID*进行group，并转化为transaction的格式
transactions = pd.DataFrame(df.groupby('客户ID'))
dataset = []
for i in range(transactions.shape[0]):
    dataset.append(list(set(transactions.iloc[i,1]['产品名称'])))  # 多次购买的产品只保留一次，使用set去除重复项
# 进行one-hot编码
te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)


# 3.利用Apriori找出频繁项集和频繁规则
frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True)
frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False)
print('='*10, '支持度TOP 10频繁项集', '='*10)
print(frequent_itemsets.head(10))  # 打印支持度最高的10个频繁项集
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(by='lift', ascending=False)
print('='*10, '提升度TOP 10关联规则', '='*10)
print(rules.head(10))  # 打印提升度最高的10条关联规则


# 4.可视化显示各条关联规则的 支持度，置信度，提升度分布
img = plt.scatter(rules['antecedent support'], rules['confidence'],
                  marker='o',
                  s=80,
                  c=rules['lift'],
                  cmap='Reds')
plt.xlabel('antecedent support')
plt.ylabel('confidence')
c = plt.colorbar()
c.set_label('lift')


end = time.time()  # 程序结束时间
running_time = str(round(end - start, 4)) + 's'
print('running time: ' + running_time)
