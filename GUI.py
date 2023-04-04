'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-04-04 10:58:14
FilePath: \WangYi\GUI.py
'''
from tkinter import *
from search import InfoSearcher
from spider import Spider
import os
import json
from threading import Thread
from tkinter import scrolledtext
from tkinter import messagebox
from hotkey import HotKey
from wordcloud import WordCloud
import jieba
import clouds

class Application():
    def __init__(self):
        win = Tk()
        win.geometry('800x800+550+150')
        win.title("网易云评论获取")
        win.resizable(0, 0)     # 固定窗口大小
        self.master = win
        self.master.configure(bg='white')
        self.clouds = clouds.CreateWL()

        self.songs_id = []
        self.check_boxs = []
        self.check_btns = []
        self.comment_texts = []
        self.comment_frames = []
        self.song_info_frames = []
        self.hot_key = HotKey(self.master)
        self.add_menu_bar()
        self.add_header()
        self.add_search()
        self.add_song_info()
        # self.thread_it(self.song_info_refresh)
        self.thread_it(self.song_info_frame_refresh)
        self.add_comment()
        self.thread_it(self.comments_refresh)
        
        
        win.mainloop()

    # 添加菜单栏
    def add_menu_bar(self):
        # 创建menubar
        self.menu_bar = Menu(self.master, font=("黑体", 14))
        self.master.configure(menu=self.menu_bar)
        # 创建file菜单
        self.file_menu = Menu(self.menu_bar, tearoff=0, font=("黑体", 10))
        self.file_menu.add_command(label="保存到本地", command=self.save_to_local)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.master.quit)
        # 将file菜单添加到menubar中
        self.menu_bar.add_cascade(label="文件", menu=self.file_menu)
        
        # 创建热词分析菜单
        self.analyze_menu = Menu(self.menu_bar, tearoff=0, font=("黑体", 10))
        self.analyze_menu.add_command(label="热词导入", command=self.hot_key.hot_key_import)
        self.analyze_menu.add_command(label="热词导出", command=self.hot_key.hot_key_export)
        self.analyze_menu.add_command(label="热词设置", command=self.hot_key.hot_key_setting)
        self.analyze_menu.add_command(label="热词统计", command=self.hot_key.hot_key_stat)
        # 将热词分析菜单添加到menubar中
        self.menu_bar.add_cascade(label="热词分析", menu=self.analyze_menu)

        # 创建生成词云菜单
        self.wordcloud_menu = Menu(self.menu_bar, tearoff=0, font=("黑体", 10))
        self.wordcloud_menu.add_command(label="生成词云(已选中歌曲)", command=self.create_word_cloud)
        self.wordcloud_menu.add_command(label="生成词云(从本地选择文件)", command=self.clouds.create_cloud)

        # 将生成词云菜单添加到menubar中
        self.menu_bar.add_cascade(label="生成词云", menu=self.wordcloud_menu) 

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

    # 添加歌曲信息部分，创建4个frame页面
    def add_song_info(self):
        # 添加歌曲信息框
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

        # 添加评论数量输入框
        Label(self.master, text='获取评论的条数：', font=('黑体', 16), bg='white').place(x=50, y=145, width=180, height=30)
        self.comment_num_var = IntVar()
        self.comment_num_var.set(100)
        Entry(self.master, font=('黑体', 16), textvariable=self.comment_num_var).place(x=240, y=145, width=80, height=30)

        # 添加全选按钮
        Button(self.master, text='全选', font=('黑体', 16), bg='white', command=self.all_select).place(x=330, y=145, width=50, height=30)

        # 添加查找歌曲按钮按钮
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
        self.comment_frame = Frame(self.master, bg='#f2f2f3')
        self.comment_frame.place(x=50, y=370, width=700, height=400)
        # 页数的刷新在self.click_check_button中实现

        # 添加评论展示部分翻页按钮
        # 下一页
        btn_next = Button(self.master, text="下一页",
                          command=self.click_next_page)
        btn_next.place(x=700, y=770, width=50, height=25)
        # 选页跳转部分
        btn_jump = Button(self.master, text="跳转",
                          command=self.page_jump)
        btn_jump.place(x=650, y=770, width=50, height=25)
        self.comments_pages_var = IntVar()
        page_num_entry = Entry(self.master, font=(
            "黑体", 20), width=2, justify=CENTER, textvariable=self.comments_pages_var)
        page_num_entry.place(x=600, y=770, width=50, height=25)
        self.comments_pages_var.set(1)
        # 上一页
        btn_previous = Button(self.master, text="上一页",
                              command=self.click_previous_page)
        btn_previous.place(x=550, y=770, width=50, height=25)

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

    # 设置刷新歌曲信息复选框 创建20个checkbutton，添加到self.song_info_frames中
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
                        # print(lab_str)
                        box = BooleanVar()
                        self.check_boxs.append(box)
                        btn = Checkbutton(
                            self.song_info_frames[i//5], text=lab_str, font=("黑体", 16), bg='#f2f2f3', variable=self.check_boxs[i])
                        btn.bind("<ButtonPress-1>", self.click_check_button)
                        self.check_btns.append(btn)
                        btn.pack(anchor="w", side=TOP, padx=15)
                        i += 1
                os.remove("data/songs.tmp")

    # 实现歌曲信息区域选页的效果  func -> self.page_btns[]
    def switch_page(self, event):
        for frame in self.song_info_frames:
            frame.pack_forget()
        for btn in self.page_btns:
            btn['bg'] = 'white'
        index = int(event.widget['text'])
        self.song_info_frames[index-1].pack(fill=BOTH)
        event.widget['bg'] = 'blue'

    # 搜索歌曲功能 func -> search_btn
    def search_song(self, song_name, singer_name):
        self.gui_init()
        info_searcher = InfoSearcher(song_name, singer_name)
        info_searcher.start()

    # 点击复选按钮功能 点击的同时添加评论frame  func -> self.check_btns[]
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
        for frame in self.comment_frames:
            frame[0].destroy()
        self.comment_frames.clear()
        self.comments_pages_var.set(1)
        pages_num = len(self.songs_id)
        for i in range(pages_num):
            frame = Frame(self.comment_frame, bg='#f2f2f3')
            frame.pack_forget()
            # False表示当前页面没有被显示出来，方便后续页面跳转
            self.comment_frames.append([frame, False])
        # 显示出第一个frame
        if self.comment_frames:
            self.comment_frames[0][0].pack(expand=1, fill=BOTH)
            self.comment_frames[0][1] = True

    # 全选功能
    def all_select(self):
        # 更新self.songs_id
        self.songs_id.clear()
        for info in self.songs_info:
            self.songs_id.append(str(info['song_id']))
        self.songs_id_var.set(",".join(self.songs_id))
        # check_boxs全部设置为true
        for btn in self.check_btns:
            btn.select()
        # 刷新评论frame的页数
        for frame in self.comment_frames:
            frame[0].destroy()
        self.comment_frames.clear()
        self.comments_pages_var.set(1)
        pages_num = len(self.songs_id)
        for i in range(pages_num):
            frame = Frame(self.comment_frame, bg='#f2f2f3')
            frame.pack_forget()
            # False表示当前页面没有被显示出来，方便后续页面跳转
            self.comment_frames.append([frame, False])
        # 显示出第一个frame
        if self.comment_frames:
            self.comment_frames[0][0].pack(expand=1, fill=BOTH)
            self.comment_frames[0][1] = True
        

    
    # 获取评论功能  func -> get_info_btn
    def get_comments(self, songs_id):
        # 清楚已经被绑定的text
        self.comment_texts.clear()
        self.songs_id = songs_id.split(",")
        spider = Spider(self.songs_id, num=int(self.comment_num_var.get()))
        spider.start()

    # 将函数转换为子线程执行
    def thread_it(self, func, *args):
        t = Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    # 刷新评论显示区
    def comments_refresh(self):
        while True:
            if os.path.exists("data/comments.tmp"):
                # print("检测到文件存在！")
                with open("data/comments.tmp", "r", encoding='utf-8') as f:
                    content = f.read()
                    self.comments = json.loads(content)
                # 根据comments的数量创建文本框
                index = 0
                for song_id in self.songs_id:
                    song_name = ""
                    # print(song_id)
                    # 获取歌曲id和歌曲名
                    for info in self.songs_info:
                        if info['song_id'] == int(song_id):
                            song_name = info['song_name']
                            # print("song_name:", song_name)

                    content = self.comments[song_id]
                    text = scrolledtext.ScrolledText(self.comment_frames[index][0], font=(
                        "黑体", 14), bg='#f2f2f3')
                    text.pack(side=LEFT,fill=Y, expand=1)
                    text.insert(1.0, "歌曲id: "+song_id+ "        歌曲名:" + song_name +"\n\n")
                    for line in content:
                        text.insert(END, line)

                    # # 添加滚动条
                    # scroll = Scrollbar(self.comment_frames[index][0], command=text.yview)
                    # scroll.pack(side=RIGHT, fill=Y)
                    # text.config(yscrollcommand=scroll.set)
                    
                    self.comment_texts.append(text)
                    index += 1
                os.remove("data/comments.tmp")

    # 清空frame中的所有组件
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    # 初始化GUI界面和所有资源
    def gui_init(self):
        # 清空现有的checkbutton``
        for frame in self.song_info_frames:
            self.clear_frame(frame)
        # 清空评论frame上的所有组件
        for frame in self.comment_frames:
            frame[0].destroy()
        # 重置变量
        self.songs_id.clear()
        self.comment_texts.clear()
        self.comment_frames.clear()
        self.check_boxs.clear()
        self.check_btns.clear()
        # 清空临时文件
        ls = os.listdir("data")
        for dir in ls:
            dir = os.path.join("data", dir)
            if os.path.isdir(dir):
                continue
            if dir.split(".")[-1] == 'tmp':
                os.remove(dir)
        # 初始化页面页码
        self.comments_pages_var.set(1)
        for btn in self.page_btns:
            btn.configure(bg='white')
        self.page_btns[0].configure(bg='blue')

    # 保存到本地功能
    def save_to_local(self):
        for song_id in self.songs_id:
            content = self.comments[song_id]
            # 获取歌曲名
            song_name = ""
            for info in self.songs_info:
                if info['song_id'] == int(song_id):
                    song_name = info['song_name']
                    # print("song_name:", song_name)
            # 将歌曲评论写入csv文件
            if not os.path.exists('data/comments'):
                os.mkdir('data/comments')
            file_name = song_id + "_" + song_name + ".txt"
            with open("data/comments/"+file_name, 'w', encoding='utf-8') as f:
                for line in content:
                    if line == "" or line =="\n":
                        continue
                    f.write(line)
        messagebox.showinfo("消息", "成功保存到:data/comments")

    # 生成词云
    def create_word_cloud(self):
        # 判断文件夹是否存在
        if not os.path.exists("data/word_clouds"):
            os.mkdir("data/word_clouds")
        # 获取歌曲评论
        for song_id in self.songs_id:
            content = self.comments[song_id]
            # 获取歌曲名
            song_name = ""
            for info in self.songs_info:
                if info['song_id'] == int(song_id):
                    song_name = info['song_name']
            # 对歌曲评论进行分词
            content = ",".join(content).replace("reply:", "")
            words = jieba.lcut(content)
            new_words = "".join(words)
            word_cloud = WordCloud(font_path="font/msyh.ttc").generate(new_words)
            word_cloud.to_file("data/word_clouds/" + song_name + ".png")

            
        
if __name__ == '__main__':
    app = Application()
