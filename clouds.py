'''
Author: Hummer hzlqjmct@163.com
Date: 2023-04-04 10:11:21
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-04-04 16:00:00
FilePath: \WangYi\wordcloud.py
'''
from wordcloud import WordCloud
import jieba
from tkinter import filedialog
import os
from tkinter import messagebox
import datetime

class CreateWL:
    def __init__(self):
        pass

    # 获取停用词列表
    def get_stopword_list(self):
        with open("stopwords/cn_stopwords.txt", 'r', encoding='utf-8') as f:
            stopword_list = [word.strip("\n") for word in f.readlines()]
            return stopword_list

    def create_cloud(self):
        # 用户选择评论文件
        self.file_names = filedialog.askopenfilenames()
        # 用于存放词语的字典
        self.words = []
        # 获取停用词列表
        self.stopword_list = self.get_stopword_list()
        for file_name in self.file_names:
            if os.path.splitext(file_name)[1] != '.txt':
                messagebox.showerror("警告", "请选择正确的评论文件(txt文件)")
                return
            with open(file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip("\n")
                    line = line.replace("reply", "")
                    line = line.replace("#", "")
                    if not line:
                        continue
                    words = jieba.lcut(line)
                    for word in words:
                        if word not in self.stopword_list:
                            self.words.append(word)
                    # print(words)
                    # print("-----------------------------------------------------")
            # print(file_name)
        print("共识别%d个词语"%len(self.words))
        words_str = " ".join(self.words)
        word_cloud = WordCloud(font_path="font/msyh.ttc",scale=10).generate(words_str)
        time = datetime.datetime.now()
        time = time.strftime("%m_%d_%H_%M_%S")
        word_cloud.to_file("data/word_clouds/"+time+".png")
        messagebox.showinfo("消息", "已成功生成词云:"+"data/word_clouds/"+time+".png")
        


if __name__ == '__main__':
    wl = CreateWL()
    wl.create_cloud()
    