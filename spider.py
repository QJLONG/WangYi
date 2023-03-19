'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-17 16:32:41
FilePath: \WangYi\spider.py
'''
from DataEncer import DataEncer
import requests
import threading
import os


class Spider(threading.Thread):
    def __init__(self, song_id="32507038", num=20):
        super().__init__()
        self.song_id = song_id
        self.data =  {
            "cursor": -1,
            "offset": 0,
            "orderType": 1,
            "pageNo": 1,
            "pageSize": f"{num}",
            "rid": f"R_SO_4_{self.song_id}",    # 根据song_id识别不同歌曲
            "threadId": f"R_SO_4_{self.song_id}"
        }

    # 携带加密过后的data请求评论
    def get_comments(self):
        data_encer = DataEncer(self.data)
        enc_data = data_encer.data_enc()
        resp = requests.post("https://music.163.com/weapi/comment/resource/comments/get?csrf_token=", data=enc_data)
        data_dic = resp.json()
        comments = data_dic['data']['comments']
        # 将获取的评论保存到本地
        if not os.path.exists("data"):
            os.makedirs("data")
        with open("data/comments.tmp", "w", encoding='utf-8') as f:

            for comment in comments:
            # 遍历所有评论
                f.write('#' + " " + comment['content'] + "\n")
                replies = comment['beReplied']
                if replies:
                    for reply in replies:
                        f.write('  reply:' + reply['content'] + "\n")

    def run(self):
        self.get_comments()


if __name__ == '__main__':
    s = Spider("32507038")
    s.get_comments()