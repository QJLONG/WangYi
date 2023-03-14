'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-09 13:48:13
FilePath: \WangYi\GUI.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from tkinter import *


class Application():
    def __init__(self):
        win = Tk()
        win.geometry('800x800')
        win.title("test")
        self.master = win
        win.mainloop()
        



if __name__ == '__main__':
    app = Application()
