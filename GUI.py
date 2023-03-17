'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-17 11:05:20
FilePath: \WangYi\GUI.py
'''
from tkinter import *
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
        # self.thread_it(self.song_info_refresh)
        self.thread_it(self.song_info_frame_refresh)
        self.songs_id = []
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

    # 添加歌曲信息部分
    def add_song_info(self):
        # 添加歌曲信息框
        # self.scroll = scrolledtext.ScrolledText(self.master, font=("黑体", 15))
        # self.scroll.place(x=50, y=175, width=500, height=175)
        self.song_info_frame = Frame(self.master ,bg='white')
        self.song_info_frame.place(x=50, y=145, width=500, height=175)
        # 创建页面frame
        self.song_info_frames = []
        for i in range(4):
            frame = Frame(self.song_info_frame, width=500, height=175, bg='white')
            self.song_info_frames.append(frame)
        self.song_info_frames[0].pack(fill=BOTH)
            
        # # 为了测试 设置不同的frame不同的背景色
        # self.song_info_frames[0]['bg'] = "gray"
        # self.song_info_frames[1]['bg'] = "green"
        # self.song_info_frames[2]['bg'] = "blue"
        # self.song_info_frames[3]['bg'] = 'red'

        # 添加info框翻页按钮
        self.page_btns = []
        for i in range(4):
            btn = Button(self.master, text=str(i+1), width=3, height=1, bg='white')
            btn.bind('<ButtonPress-1>', self.switch_page)
            btn.place(x=390+i*40, y=320, width=40, height=30) 
            self.page_btns.append(btn)    
        self.page_btns[0]['bg'] = 'blue'

        
        # 添加搜索按钮
        search_btn = Button(self.master, text="查找歌曲", font=("黑体", 17), command= lambda: self.search_song(self.song_name_var.get(), self.singer_name_var.get()))
        search_btn.place(x=560, y=175, width=200, height=50)

        # 添加歌曲ID输入框
        self.songs_id_var = StringVar(value="歌曲ID(逗号分割)")
        entry = Entry(self.master, justify="center", font=("黑体", 18, "bold"), textvariable=self.songs_id_var)
        entry.place(x=560, y=235, width=200, height=50)

        # 添加获取评论按钮
        get_info_btn = Button(self.master, text="获取评论", font=("黑体", 18), command= lambda: self.get_comments(self.songs_id_var.get()))
        get_info_btn.place(x=560, y=300, width=200, height=50)

    # 设置刷新歌曲信息复选框
    def song_info_frame_refresh(self):
        while True:
            if os.path.exists('data/songs.tmp'):
                with open("data/songs.tmp", "r", encoding='utf-8') as f:
                    self.songs_info = json.loads(f.read())
                    self.check_btns = []
                    self.check_boxs = []
                    # 将20个搜索信息构成checkbutton，并添加到四个frame中
                    i = 0
                    for info in self.songs_info:
                        lab_str = str(i+1) + " " + str(info['song_id']) + " " + info['song_name']
                        print(lab_str)
                        box = BooleanVar()
                        self.check_boxs.append(box)
                        btn = Checkbutton(self.song_info_frames[i//5], text=lab_str, font=("黑体", 17), bg='white') 
                        btn.bind("<ButtonPress-1>", self.click_check_button)
                        self.check_btns.append(btn)
                        btn.pack(anchor="w", side=TOP)
                        i += 1
                os.remove("data/songs.tmp")

                

    # 实现选页的效果
    def switch_page(self, event):
        for frame in self.song_info_frames:
            frame.pack_forget()
        for btn in self.page_btns:
            btn['bg'] = 'white'
        index = int(event.widget['text'])
        self.song_info_frames[index-1].pack(fill=BOTH)
        event.widget['bg'] = 'blue'


    # 搜索歌曲功能
    def search_song(self, song_name, singer_name):
        info_searcher = InfoSearcher(song_name, singer_name)
        info_searcher.start()

    # 点击复选按钮功能
    def click_check_button(self, event):
        btn_index =int(event.widget['text'].split()[0]) - 1
        song_id = event.widget['text'].split()[1]
        # print(self.check_boxs[btn_index].get())
        if not self.check_boxs[btn_index].get():
            self.check_boxs[btn_index].set(True)
            self.songs_id.append(song_id)
        else:
            self.check_boxs[btn_index].set(False)
            self.songs_id.remove(song_id)
        self.songs_id_var.set(",".join(self.songs_id))

    # 获取评论功能
    def get_comments(self, songs_id):
        self.songs_id = songs_id.split(",")
        # print(self.songs_id)
        for song_id in self.songs_id:
            spider = Spider(song_id)
            spider.start()
            time.sleep(1) 


    # 将函数转换为子线程执行
    def thread_it(self, func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()
        

if __name__ == '__main__':
    app = Application()
