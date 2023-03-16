'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-16 15:52:25
FilePath: \WangYi\GUI.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from tkinter import *
from tkinter import scrolledtext
from search import InfoSearcher
from spider import Spider
import os
import json
from threading import Thread
import time


class Application():
    def __init__(self):
        win = Tk()
        win.geometry('800x800+550+150')
        win.title("网易云评论获取")
        win.resizable(0, 0)     # 固定窗口大小
        self.master = win
        self.add_header()
        self.add_search()
        self.add_song_info()
        self.thread_it(self.song_info_refresh)
        win.mainloop()
    
    # 添加头部标签
    def add_header(self):
        self.header_lab = Label(self.master,  text="网易云音乐评论抓取程序",
                                 font=('黑体', 25, "bold"), justify='center')
        self.header_lab.place(x=0, y=15, height=50, width=800)

    # 添加歌曲搜索部分
    def add_search(self):
        # 添加歌曲名搜索框
        self.song_name_var = StringVar()
        lab1 = Label(self.master, text="歌曲名:", justify="center",
                     font=("黑体", 18))
        lab1.place(x=50, y=100, width=90, height=30)
        entry1 = Entry(self.master, justify="center", font=("黑体", 18), textvariable=self.song_name_var)
        entry1.place(x=160, y=100, width=250, height=30)

        # 添加歌手搜索框
        self.singer_name_var = StringVar()
        lab2 = Label(self.master, text="歌手名:", justify="center",
                     font=("黑体", 18))
        lab2.place(x=450, y=100, width=90, height=30)
        entry2 = Entry(self.master, justify="center", font=("黑体", 18), textvariable=self.singer_name_var)
        entry2.place(x=560, y=100, width=190, height=30)

    # 添加歌曲信息框部分
    def add_song_info(self):
        # 添加歌曲信息框
        self.scroll = scrolledtext.ScrolledText(self.master, font=("黑体", 15))
        self.scroll.place(x=50, y=175, width=500, height=175)
        
        # 添加搜索按钮
        search_btn = Button(self.master, text="查找歌曲", font=("黑体", 18), command= lambda: self.search_song(self.song_name_var.get(), self.singer_name_var.get()))
        search_btn.place(x=570, y=175, width=200, height=50)

        # 添加歌曲ID输入框
        self.songs_id_var = StringVar(value="歌曲ID(逗号分割)")
        entry = Entry(self.master, justify="center", font=("黑体", 18, "bold"), textvariable=self.songs_id_var)
        entry.place(x=570, y=235, width=200, height=50)

        # 添加获取评论按钮
        get_info_btn = Button(self.master, text="获取评论", font=("黑体", 18), command= lambda: self.get_comments(self.songs_id_var.get()))
        get_info_btn.place(x=570, y=300, width=200, height=50)

    # 搜索歌曲功能
    def search_song(self, song_name, singer_name):
        info_searcher = InfoSearcher(song_name, singer_name)
        info_searcher.start()

    # 获取评论功能
    def get_comments(self, songs_id):
        self.songs_id = songs_id.split(",")
        print(self.songs_id)
        for song_id in self.songs_id:
            spider = Spider(song_id)
            spider.start()
            time.sleep(1)
            
            
    
    # 不断刷新歌曲信息框
    def song_info_refresh(self):
        while True:
            if os.path.exists("data/songs.tmp"):
                self.scroll.configure(state="normal")
                self.scroll.delete(1.0, END)
                with open("data/songs.tmp", 'r', encoding='utf-8') as f:
                    infos_json = f.read()
                self.songs_info = json.loads(infos_json)
                for song_info in self.songs_info:
                    row = "%10s   %s\n" % (song_info["song_id"], song_info['song_name'])
                    self.scroll.insert(END, row)
                self.scroll.configure(state="disabled")
                os.remove("data/songs.tmp")

    # 将函数转换为子线程执行
    def thread_it(self, func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

        

        



if __name__ == '__main__':
    app = Application()
