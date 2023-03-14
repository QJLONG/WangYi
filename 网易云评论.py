# 1.url:'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='
# 2.data:params和encSecKey
from Crypto.Cipher import AES
import json
import base64
import requests

data = {
    "cursor": -1,
    "offset": 0,
    "orderType": 1,
    "pageNo": 1,
    "pageSize": 20,
    "rid": "R_SO_4_32507038",
    "threadId": "R_SO_4_32507038"
}
encSecKey = "d7101edd07546dc383fd947d64f8689deecbefd83ba95b206cde5f1e7eb50c340250604c7f53c618301fd21b367775ca531e4d64fc1a7251d414fdc560dbea0f2fb78f975b8e306d580d2066fb96f6ba95a6471b19d52f0db5873a9b7ba38749fc2810ed0764cb9f17ea343903669e38cf83af3133ac844737cd0077cb7b2669"
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
e = '010001'
g = '0CoJUm6Qyw8W8jud'
i = "bJH7kP6B8YxRLB1n"
iv = '0102030405060708' 

'''
加密函数
function() {
    function a(a=16) {
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1) 循环16次
            e = Math.random() * b.length,
            e = Math.floor(e),
            c += b.charAt(e);
        return c
    }
     function b(a, b) {
            var c = CryptoJS.enc.Utf8.parse(b)
              , d = CryptoJS.enc.Utf8.parse("0102030405060708")
              , e = CryptoJS.enc.Utf8.parse(a)
              , f = CryptoJS.AES.encrypt(e, c, {
                iv: d,
                mode: CryptoJS.mode.CBC
            });
            return f.toString()
        }
        function c(a, b, c) {
            var d, e;
            return setMaxDigits(131),
            d = new RSAKeyPair(b,"",c),
            e = encryptedString(d, a)
        }
        入口函数：
        function d(d, e, f, g) {        d:data  e:010001   f:字符串 g:'0CoJUm6Qyw8W8jud'
            var h = {}
              , i = a(16);          function a：生成16个随机字符，返回组成的随机字符串
            return h.encText = b(d, g),  加密函数   g为密钥
            h.encText = b(h.encText, i),    用随机字符串i作为密钥再次进行AES加密
            h.encSecKey = c(i, e, f),       
            h
        }
        function e(a, b, d, e) {
            var f = {};
            return f.encText = c(a + e, b, d),
            f
        }
    }
'''

d = str(json.dumps(data))

# 将字符串补全为16的倍数
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad)*pad
    return data


def get_encText(data):
    first_enc = encrypt(data, g)
    second_enc = encrypt(first_enc, i)
    return second_enc


def encrypt(data, key):
    data = to_16(data)
    aes = AES.new(key=key.encode('utf-8'), mode=AES.MODE_CBC, IV=iv.encode('utf-8'))
    bs = aes.encrypt(data.encode('utf-8'))
    return str(base64.b64encode(bs), 'utf-8')


data = {
    "params": get_encText(d),
    "encSecKey": encSecKey
}

resp = requests.post("https://music.163.com/weapi/comment/resource/comments/get?csrf_token=", data=data)
text = resp.text

# 获取所有的评论
data_dic = json.loads(text)
comments = data_dic['data']['comments']

for comment in comments:
    # 遍历所有评论
    print('#' + comment['content'])
    replies = comment['beReplied']
    if replies:
        for reply in replies:
            print('reply:' + reply['content'])
    print('\n')
