'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-22 17:34:40
FilePath: \WangYi\GUI.py
'''
from tkinter import *
from search import InfoSearcher
from spider import Spider
import os
import json
from threading import Thread
import time
from tkinter import scrolledtext
from tkinter import messagebox


class Application():
    def __init__(self):
        win = Tk()
        win.geometry('800x800+550+150')
        win.title("网易云评论获取")
        win.resizable(0, 0)     # 固定窗口大小
        self.master = win
        self.master.configure(bg='white')
        self.songs_id = []
        self.add_header()
        self.add_search()
        self.add_song_info()
        # self.thread_it(self.song_info_refresh)
        self.thread_it(self.song_info_frame_refresh)
        self.add_comment()
        self.thread_it(self.comments_refresh)
        
        win.mainloop()

    # 添加头部标签
    def add_header(self):
        self.header_lab = Label(self.master,  text="网易云音乐评论抓取程序",
                                font=('黑体', 25, "bold"), bg='white', justify='center')
        self.header_lab.place(x=0, y=15, height=50, width=800)

    # 添加歌曲搜索部分
    def add_search(self):
        # 添加歌曲名搜索框
        self.song_name_var = StringVar()
        lab1 = Label(self.master, text="歌曲名:", justify="center",
                     font=("黑体", 18), bg='white')
        lab1.place(x=50, y=100, width=90, height=30)
        entry1 = Entry(self.master, justify="center", font=(
            "黑体", 18), textvariable=self.song_name_var)
        entry1.place(x=160, y=100, width=250, height=30)

        # 添加歌手搜索框
        self.singer_name_var = StringVar()
        lab2 = Label(self.master, text="歌手名:", justify="center",
                     font=("黑体", 18), bg='white')
        lab2.place(x=450, y=100, width=90, height=30)
        entry2 = Entry(self.master, justify="center", font=(
            "黑体", 18), textvariable=self.singer_name_var)
        entry2.place(x=560, y=100, width=190, height=30)

    # 添加歌曲信息部分
    def add_song_info(self):
        # 添加歌曲信息框
        # self.scroll = scrolledtext.ScrolledText(self.master, font=("黑体", 15))
        # self.scroll.place(x=50, y=175, width=500, height=175)
        self.song_info_frame = Frame(self.master, bg='white')
        self.song_info_frame.place(x=50, y=175, width=500, height=175)
        # 创建页面frame
        self.song_info_frames = []
        for i in range(4):
            frame = Frame(self.song_info_frame, width=500,
                          height=175, bg='#f2f2f3')
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
            btn = Button(self.master, text=str(i+1),
                         width=3, height=1, bg='white')
            btn.bind('<ButtonPress-1>', self.switch_page)
            btn.place(x=390+i*40, y=145, width=40, height=30)
            self.page_btns.append(btn)
        self.page_btns[0]['bg'] = 'blue'

        # 添加搜索按钮
        search_btn = Button(self.master, text="查找歌曲", font=("黑体", 17), bg='white',
                            command=lambda: self.search_song(self.song_name_var.get(), self.singer_name_var.get()))
        search_btn.place(x=560, y=175, width=200, height=50)

        # 添加歌曲ID输入框
        self.songs_id_var = StringVar(value="歌曲ID(逗号分割)")
        entry = Entry(self.master, justify="center", font=(
            "黑体", 18, "bold"), textvariable=self.songs_id_var)
        entry.place(x=560, y=235, width=200, height=50)

        # 添加获取评论按钮
        get_info_btn = Button(self.master, text="获取评论", font=("黑体", 18), bg='white',
                              command=lambda: self.get_comments(self.songs_id_var.get()))
        get_info_btn.place(x=560, y=300, width=200, height=50)

    # 添加歌曲评论部分
    def add_comment(self):
        self.comment_frame = Frame(self.master, bg='green')
        self.comment_frame.place(x=50, y=370, width=650, height=300)
        self.comment_frames = []
        # 页数的刷新在self.click_check_button中实现

        # 添加评论展示部分翻页按钮
        # 下一页
        btn_next = Button(self.comment_frame, text="下一页",
                          command=self.click_next_page)
        btn_next.pack(side=RIGHT, anchor="se")
        # 选页跳转部分
        btn_jump = Button(self.comment_frame, text="跳转",
                          command=self.page_jump)
        btn_jump.pack(side=RIGHT, anchor='se')
        self.comments_pages_var = IntVar()
        page_num_entry = Entry(self.comment_frame, font=(
            "黑体", 20), width=2, justify=CENTER, textvariable=self.comments_pages_var)
        page_num_entry.pack(side=RIGHT, anchor='se')
        self.comments_pages_var.set(1)
        # 上一页
        btn_previous = Button(self.comment_frame, text="上一页",
                              command=self.click_previous_page)
        btn_previous.pack(side=RIGHT, anchor="se")

        # 添加评论显示框架：
        # self.commant_text = Text(self.master, font=("黑体", 16), bg='white')
        # self.commant_text.place(x=50, y=370, width=650, height=300)
        # # 为显示框架添加滚动条
        # scroll_bar = Scrollbar(command=self.commant_text.yview)
        # scroll_bar.pack(side=RIGHT, fill=Y)
        # self.commant_text.configure(yscrollcommand=scroll_bar.set)

    # 跳转到下一页功能实现
    def click_next_page(self):
        # for i in range(len(self.comment_frames)):
        #     if self.comment_frames[i][1] == True:
        #         if i == len(self.comment_frames) - 1:
        #             messagebox.showerror("警告","已经是最后一页了！")
        #             continue
        #         # 将已经显示出来的页面隐藏起来
        #         self.comment_frames[i][0].pack_forget()
        #         self.comment_frames[i][1] = False
        #         # 将当前页面的下一个页面显示出来
        #         self.comment_frames[i+1][0].pack(expand=1, fill=BOTH)
        #         self.comment_frames[i+1][1] = True
        #         # 重置选页entry中的页数
        #         self.comments_pages_var.set(i+2)
        #         break
        cur_page = self.comments_pages_var.get()
        index = cur_page - 1
        if self.comment_frames[index][1] == True:
            if self.comments_pages_var.get() == len(self.comment_frames):
                messagebox.showerror("警告", "已经是最后一页了！")
                return
            # 将已经显示出来的页面隐藏起来
            self.comment_frames[index][0].pack_forget()
            self.comment_frames[index][1] = False
            # 将当前页面的下一个页面显示出来
            self.comment_frames[cur_page][0].pack(expand=1, fill=BOTH)
            self.comment_frames[cur_page][1] = True
            # 重置选页entry中的页数
            self.comments_pages_var.set(cur_page+1)
        else:
            messagebox.showerror("警告", "当前页面不存在")
            self.comments_pages_var.set(1)

    # 跳转到上一页功能实现

    def click_previous_page(self):
        # for i in range(len(self.comment_frames)):
        #     if self.comment_frames[i][1] == True:
        #         if i == 0:
        #             messagebox.showerror("警告","已经是第一页了！")
        #             continue
        #         # 将已经显示出来的页面隐藏起来
        #         self.comment_frames[i][0].pack_forget()
        #         self.comment_frames[i][1] = False
        #         # 将当前页面的上一个页面显示出来
        #         self.comment_frames[i-1][0].pack(expand=1, fill=BOTH)
        #         self.comment_frames[i-1][1] = True
        #         # 重置选页entry中的页数
        #         self.comments_pages_var.set(i)
        #         break
        cur_page = self.comments_pages_var.get()
        index = cur_page-1
        if self.comment_frames[index][1] == True:
            if cur_page == 1:
                messagebox.showerror("警告", "已经是第一页了！")
                return
            # 将已经显示出来的页面隐藏起来
            self.comment_frames[index][0].pack_forget()
            self.comment_frames[index][1] = False
            # 将当前页面的上一个页面显示出来
            self.comment_frames[index-1][0].pack(expand=1, fill=BOTH)
            self.comment_frames[index-1][1] = True
            # 重置选页entry中的页数
            self.comments_pages_var.set(cur_page-1)
        else:
            messagebox.showinfo("警告", "当前页面不存在")
            self.comments_pages_var.set(1)

    # 评论显示区页面跳转功能

    def page_jump(self):
        cur_page = self.comments_pages_var.get()
        index = cur_page - 1
        try:
            # 判断如果页码超出范围，则回到第一页
            if cur_page < 1 or cur_page > len(self.comment_frames):
                messagebox.showerror("警告", "页面不存在")
                for frame in self.comment_frames:
                    frame[0].pack_forget()
                    frame[1] = False

                self.comment_frames[0][0].pack(expand=1, fill=BOTH)
                self.comment_frames[0][1] = True
                self.comments_pages_var.set(1)
                return
            # 先将已经显示的页面隐藏
            for frame in self.comment_frames:
                frame[0].pack_forget()
                frame[1] = False
            # 将页码对应的页面显示出来
            self.comment_frames[index][0].pack(expand=1, fill=BOTH)
            self.comment_frames[index][1] = True
        except IOError as e:
            print(e)

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
                        lab_str = str(
                            i+1) + " " + str(info['song_id']) + " " + info['song_name']
                        print(lab_str)
                        box = BooleanVar()
                        self.check_boxs.append(box)
                        btn = Checkbutton(
                            self.song_info_frames[i//5], text=lab_str, font=("黑体", 17), bg='white', variable=self.check_boxs[i])
                        btn.bind("<ButtonPress-1>", self.click_check_button)
                        self.check_btns.append(btn)
                        btn.pack(anchor="w", side=TOP, padx=15)
                        i += 1
                os.remove("data/songs.tmp")

    # 实现歌曲信息区域选页的效果
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
        btn_index = int(event.widget['text'].split()[0]) - 1
        song_id = event.widget['text'].split()[1]
        # 判断如果按未被选中，则将其添加到songs_id中
        if not self.check_boxs[btn_index].get():
            self.songs_id.append(song_id)
        # 如果按钮已经被选中了，则将其从songs_id中删除
        else:
            # self.check_boxs[btn_index].set(False)
            self.songs_id.remove(song_id)
        self.songs_id_var.set(",".join(self.songs_id))

        # 点击checkbutton的同时刷新评论frame的页数
        pages_num = len(self.songs_id)
        self.comment_frames.clear()
        for i in range(pages_num):
            frame = Frame(self.comment_frame, bg='blue')
            frame.pack_forget()
            # False表示当前页面没有被显示出来，方便后续页面跳转
            self.comment_frames.append([frame, False])
        # 显示出第一个frame
        self.comment_frames[0][0].pack(expand=1, fill=BOTH)
        self.comment_frames[0][1] = True

    # 获取评论功能
    def get_comments(self, songs_id):
        self.songs_id = songs_id.split(",")
        # print(self.songs_id)
        for song_id in self.songs_id:
            spider = Spider(song_id)
            spider.start()
            time.sleep(0.5)

    # 将函数转换为子线程执行

    def thread_it(self, func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    # 刷新评论显示区
    def comments_refresh(self):
        while True:
            if os.path.exists("data/comments.tmp"):
                print("检测到文件存在！")
                with open("data/comments.tmp", "r", encoding='utf-8') as f:
                    self.comments = f.read()
                    self.comment_text.insert(1.0, self.comments)
                os.remove("data/comments.tmp")
        


if __name__ == '__main__':
    app = Application()
