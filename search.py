'''
Author: Hummer hzlqjmct@163.com
Date: 2023-03-13 17:49:20
LastEditors: Hummer hzlqjmct@163.com
LastEditTime: 2023-03-14 16:21:21
FilePath: \WangYi\search.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import requests
from Crypto.Cipher import AES
import json
import base64
import requests
from DataEncer import DataEncer

class InfoSearcher():
    # 根据歌曲名和歌手获取歌曲信息
    def __init__(self, song="", singer=""):
        self.song = song
        self.singer = singer
        self.req_url = f"https://music.163.com/#/search/m/?s={self.song}-{self.singer}"
        self.data = {
            "csrf_token": "",
            "hlposttag": "</span>",
            "hlpretag": "<span class=\"s-fc7\">",
            "limit": "30",
            "offset": "0",
            "s": f"{self.song}-{self.singer}",
            "total": "true",
            "type": "1"
        }

    def get_info(self):
        self.songs_info = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        # print(enc_data)
        data_encer = DataEncer(self.data)
        enc_data = data_encer.data_enc()
        resp = requests.post("https://music.163.com/weapi/cloudsearch/get/web?csrf_token=", data=enc_data)
        songs_info = resp.json()['result']['songs']
        # song_name = songs_info[0]['name']
        # song_id = songs_info[0]['id']
        for info in songs_info:
            if 'ar' in info:
                singer_name = info['ar'][0]['name']
            song_name = info['name'] + " " + singer_name
            song_id = info['id']
            self.songs_info.append({"song_name": song_name, "song_id": song_id})
        return self.songs_info
        

if __name__ == '__main__':
    sea = InfoSearcher(song='刚刚好', singer='薛之谦')
    print(sea.get_info())