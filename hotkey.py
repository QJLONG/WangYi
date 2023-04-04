'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-28 15:22:16
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-04-04 10:05:41
FilePath: \WangYi\hotkey.py
'''
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import re
import os
import csv
import matplotlib.pyplot as plt
from mplfonts import use_font
from mplfonts.bin.cli import init


class HotKey(Frame):
    def __init__(self, master):
        self.master = master
        self.hot_keys = ["喜欢", "爱情", "还好吗"]
        self.keys_dic = {}

    def hot_key_setting(self):
        self.hot_key_window = Toplevel(self.master)
        self.hot_key_window.geometry("400x200+750+400")
        # 添加热词输入框
        Label(self.hot_key_window, text="请输入热词,英文逗号隔开：", font=('黑体', 16), justify="center").pack()
        self.hot_key_var = StringVar()
        self.hot_key_var.set("喜欢,爱情,还好吗")
        self.hot_key_text = Text(self.hot_key_window, font=("黑体", 16),  width=35, height=5)
        self.hot_key_text.pack(pady=10)
        # 确定按钮
        Button(self.hot_key_window, text="确定", font=("黑体", 16), command=self.hot_key_confirm).place(x=120, y=160, width=50, height=30)
        Button(self.hot_key_window, text="取消", font=("黑体", 16), command=self.hot_key_window.destroy).place(x=230, y=160, width=50, height=30)

    def hot_key_confirm(self):
        content = self.hot_key_text.get(0.0, END)
        content = content.strip()
        content = content.strip(",")
        self.hot_keys = re.sub(r"\s+", "", content).split(',')
        self.hot_key_window.destroy()
        messagebox.showinfo("消息", "热词设置成功！")
        print(self.hot_keys)
    
    def hot_key_stat(self):
        self.files = os.listdir("data/comments")
        if not any(file.endswith(".txt") for file in self.files):
            messagebox.showerror("警告", "请先将评论保存至本地！")
        # 将存放统计数据的字典清零
        for key in self.hot_keys:
            self.keys_dic[key] = 0 
        for file in self.files:
            self.song_count(file)
        print(self.keys_dic)

        # 显示为柱状图
        init()
        use_font("Noto Serif CJK SC")
        plt.bar(self.keys_dic.keys(), self.keys_dic.values())
        plt.xlable=("热词")
        plt.ylabel=("出现的数量")
        plt.title('热词统计分析')
        keys = list(self.keys_dic.keys())
        values = list(self.keys_dic.values())
        # print(keys, values)
        for i in range(len(self.keys_dic)):
            plt.text(keys[i], values[i] + 1, str(values[i]), horizontalalignment="center")
        plt.show()
        

        
    # 查找一首歌中所有热词出现的次数
    def song_count(self, file_name):
        with open("data/comments/"+file_name, "r", encoding='utf-8') as f:
            content = f.read()
        for key in self.hot_keys:
            self.keys_dic[key] += content.count(key)


    # 热词导入功能
    def hot_key_import(self):
        self.hot_keys = []
        file_path = filedialog.askopenfilename()
        with open(file_path, "r", encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.hot_keys = row
        
        messagebox.showinfo("消息", "热词导入成功！\n" + ",".join(self.hot_keys))

    # 热词导出功能
    def hot_key_export(self):
        with open("data/hot_heys.csv", 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.hot_keys)
        messagebox.showinfo("消息", "热词成功导出到：data/hot_keys.csv")

if __name__ == '__main__':
    tk = Tk()
    hot_key = HotKey(tk)
    hot_key.hot_key_stat()
    # hot_key.hot_key_import()
    # hot_key.hot_key_export()
