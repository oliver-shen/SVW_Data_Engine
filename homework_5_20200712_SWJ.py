# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:23:28 2020

@author: ShenWeijie
"""

import time
import wordcloud
import imageio
import seaborn as sns
import pandas as pd

start_time = time.time()

# 打开文件并读取数据到txt
f = open('Market_Basket_Optimisation.csv')
txt = f.read()
# 使用购物车图片，作为词云的容器
mk = imageio.imread('basket.jpg')
w = wordcloud.WordCloud(width=1600,
                        height=1200,
                        background_color='white',
                        mask=mk,
                        font_path='msyh.ttc')
w.generate(txt)
w.to_file('basket_word_cloud.png')
f.close()

# 取得词频最高的10件商品
words_freq_sorted = sorted(zip(w.words_.values(), w.words_.keys()))
top_10 = words_freq_sorted[:-10:-1]
df = pd.DataFrame(top_10)
df.columns = ['Freq','Item']

# 使用seaborn进行bar图展示
ax = sns.barplot(x=df.iloc[:,0], y=df.iloc[:,1], data=df)
ax.set_title('TOP 10 Items', fontsize=18)

end_time = time.time()
running_time = str(end_time - start_time)
print('running time: ' + running_time)
