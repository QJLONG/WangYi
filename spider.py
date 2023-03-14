'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-07 23:31:49
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-14 14:51:14
FilePath: \WangYi\spider.py
'''
from Crypto.Cipher import AES
import json
import base64
import requests


class Spider():
    def __init__(self, song_id):
        self.song_id = song_id
        self.data =  {
            "cursor": -1,
            "offset": 0,
            "orderType": 1,
            "pageNo": 1,
            "pageSize": 20,
            "rid": f"R_SO_4_{self.song_id}",
            "threadId": f"R_SO_4_{self.song_id}"
        }

    def to_16(self, data):
        pad = 16 - len(data) % 16
        data += chr(pad)*pad
        return data
    
    def get_encText(self, data):
        g = '0CoJUm6Qyw8W8jud'
        i = "bJH7kP6B8YxRLB1n"
        first_enc = self.encrypt(data, g)
        second_enc = self.encrypt(first_enc, i)
        return second_enc
    
    # 创建加密器
    def encrypt(self, data, key):
        f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        e = '010001'
        iv = '0102030405060708'
        data = self.to_16(data)
        aes = AES.new(key=key.encode('utf-8'), mode=AES.MODE_CBC, IV=iv.encode('utf-8'))
        bs = aes.encrypt(data.encode('utf-8'))
        return str(base64.b64encode(bs), 'utf-8')
    
    # 对data进行加密
    def data_enc(self):
        encSecKey = "d7101edd07546dc383fd947d64f8689deecbefd83ba95b206cde5f1e7eb50c340250604c7f53c618301fd21b367775ca531e4d64fc1a7251d414fdc560dbea0f2fb78f975b8e306d580d2066fb96f6ba95a6471b19d52f0db5873a9b7ba38749fc2810ed0764cb9f17ea343903669e38cf83af3133ac844737cd0077cb7b2669"
        d = str(json.dumps(self.data))
        enc_data = {
            "params": self.get_encText(d),
            "encSecKey": encSecKey
        }
        return enc_data

    # 携带加密过后的data请求评论
    def get_comments(self):
        enc_data = self.data_enc()
        resp = requests.post("https://music.163.com/weapi/comment/resource/comments/get?csrf_token=", data=enc_data)
        text = resp.text
        data_dic = json.loads(text)
        comments = data_dic['data']['comments']
        for comment in comments:
        # 遍历所有评论
            print('#' + comment['content'])
            replies = comment['beReplied']
            if replies:
                for reply in replies:
                    print('reply:' + reply['content'])


if __name__ == '__main__':
    s = Spider("32507038")
    s.get_comments()