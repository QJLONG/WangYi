'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-22 18:20:22
FilePath: \WangYi\spider.py
'''
from DataEncer import DataEncer
import requests
import threading
import os
import json


class Spider(threading.Thread):
    def __init__(self, songs_id=["32507038"], num=20):
        super().__init__()
        self.songs_id = songs_id
        self.data =  {
            "cursor": -1,
            "offset": 0,
            "orderType": 1,
            "pageNo": 1,
            "pageSize": f"{num}",
            "rid": f"R_SO_4_{self.songs_id[0]}",    # 根据song_id识别不同歌曲
            "threadId": f"R_SO_4_{self.songs_id[0]}"
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
        result = []
        for comment in comments:
        # 遍历所有评论
            result.append('#' + " " + comment['content'] + "\n")
            replies = comment['beReplied']
            if replies:
                for reply in replies:
                    result.append('  reply:' + reply['content'] + "\n")
        return result

    def run(self):
        comments = {}
        for id in self.songs_id:
            self.data['rid'] = f"R_SO_4_{id}"
            self.data['threadId'] = f"R_SO_4_{id}"
            comments[id] = self.get_comments()

        # 将评论组成的字典转为json字符串并保存到本地
        comment_json = json.dumps(comments)
        if not os.path.exists('data'):
            os.mkdir("data")
        with open('data/comments.tmp', 'w', encoding='utf-8') as f:
            f.write(comment_json)
        
            


if __name__ == '__main__':
    s = Spider(["32507038", "415792881"])
    s.start()