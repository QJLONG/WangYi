'''
Author: Hummer hzlqjmct@163.com
Date: 2023-04-03 11:11:24
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-04-03 16:33:49
FilePath: \WangYi\test.py
'''
import jieba
from wordcloud import WordCloud

cont = "弱小的人,才习惯,嘲讽和否定，而内心,强大的人,从不吝啬赞美和鼓励！我们就是后浪，奔涌吧！后浪，奔涌吧！"
font_path = "font/msyh.ttc"
words = jieba.lcut(cont)
new_cont = "".join(words)
wordcloud = WordCloud(font_path=font_path).generate(new_cont)
wordcloud.to_file("test.jpg")