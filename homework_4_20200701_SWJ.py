# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 17:13:06 2020

@author: ShenWeijie
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import time
import matplotlib.pyplot as plt

df = pd.read_csv(r'Market_Basket_Optimisation.csv', header=None)
print(df.shape)

start_time = time.time()

# 数据格式整理
df.fillna('', inplace=True)
df['market_basket'] = ''
for i in df.columns:
    if i == 'market_basket':
        break
    else:
        df['market_basket'] = df['market_basket'] + df[i].map(str) + ','

df = pd.DataFrame(df['market_basket'])
items_hot_encoded = df.drop('market_basket',axis=1).join(df.market_basket.str.get_dummies(','))

# 使用mlxtend挖掘频繁项集和频繁规则
frequent_itemsets = apriori(items_hot_encoded, min_support=0.02, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
rules = rules.sort_values(by='lift', ascending=False)

print(rules.head(5))

img = plt.scatter(rules['antecedent support'], rules['confidence'],
                  marker='o',
                  s=80,
                  alpha=0.7,
                  c=rules['lift'],
                  cmap='Reds')
plt.xlabel('antecedent support')
plt.ylabel('confidence')
c = plt.colorbar()
c.set_label('lift')

end_time = time.time()
running_time = str(end_time - start_time)
print('running time: ' + running_time)
