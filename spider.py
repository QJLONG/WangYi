'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-14 16:05:07
FilePath: \WangYi\spider.py
'''
from DataEncer import DataEncer
import requests
import threading


class Spider(threading.Thread):
    def __init__(self, song_id):
        super().__init__()
        self.song_id = song_id
        self.data =  {
            "cursor": -1,
            "offset": 0,
            "orderType": 1,
            "pageNo": 1,
            "pageSize": 20,
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
        for comment in comments:
        # 遍历所有评论
            print('#' + comment['content'])
            replies = comment['beReplied']
            if replies:
                for reply in replies:
                    print('reply:' + reply['content'])

    def run(self):
        self.get_comments()


if __name__ == '__main__':
    s = Spider("32507038")
    s.get_comments()