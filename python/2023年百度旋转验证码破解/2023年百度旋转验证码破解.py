from urllib.parse import unquote
import requests
import time
import json
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import base64
from Crypto.Cipher import AES
import urllib

BLOCK_SIZE = 16  # Bytes
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
def aesEncrypt(key, data):
    '''
    AES的ECB模式加密方法
    :param key: 密钥
    :param data:被加密字符串（明文）
    :return:密文
    '''
    key = key.encode('utf8')
    # 字符串补位
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 加密后得到的是bytes类型的数据，使用Base64进行编码,返回byte字符串
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf8')
    # print(enctext)
    return enctext

def parseCookiestr(cookie_str):
    """解析cookie"""
    cookielist = []
    for item in cookie_str.split(';'):
        try:
            cookie={}
            itemname=item.split('=')[0]
            iremvalue=item.split('=')[1]
            cookie['name']=itemname
            cookie['value']=urllib.parse.unquote(iremvalue)
            cookielist.append(cookie)
        except:
            pass
    return cookielist

def dama_api(img_b64):
    token = '打码token' #打码接口非常便宜，有需要请联系 v：466867714
    api = f'http://api.h3blog.com/yzm_api/xuanzhuan/{token}/b64'
    result = requests.post(api,data={"img":img_b64}).text
    print('打码返回数据：', result)
    result = json.loads(result)
    return result['data']


class BaiduAiqichaRotate:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://ziyuan.baidu.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        cookie = requests.cookies.RequestsCookieJar()
        cookies = '百度cookie'
        cookielist  = parseCookiestr(cookies)
        for item in cookielist:
            cookie.set(item['name'], item['value'])
        self.session.cookies.update(cookie)

    def get_image_request_data(self):
        """
        :return: 获取需要获取图片的参数
        """
        url = "https://passport.baidu.com/viewlog"
        params = {
            "callback": "jQuery110205449684422426735_" + str(int(time.time() * 1000)),
            "ak": "33c48884b7df83d4230e07cbcd0d07fd",
            "_": str(int(time.time() * 1000))
        }
        response = self.session.get(url, headers=self.headers, params=params)
        res_data = re.findall(r'.*?(\{.*?})\)', response.text)[0]
        res_data = json.loads(res_data)
        item = {
            "tk": res_data['data']['tk'],
            "as": res_data['data']['as'],
            "ds": res_data['data']['ds']
        }
        return item

    def get_img(self, item):
        url = "https://passport.baidu.com/viewlog/getstyle"
        params = {
            "callback": "jQuery110205449684422426735_" + str(time.time() * 1000),
            "ak": '3de47787fd60b30420f868ffbf4dbccd',
            "tk": item["tk"],
            "isios": "0",
            "type": "spin",
            "_": str(time.time() * 1000)
        }
        response = self.session.get(url, headers=self.headers, params=params)
        ret_data = re.findall(r'.*?(\{.*?})\)', response.text)[0]
        ret_data = json.loads(ret_data)
        item_img = {
            "img_url": unquote(ret_data['data']['ext']['img']),
            "backstr": ret_data['data']['backstr'],
            "tk": item["tk"],
            "as": item["as"]
        }
        response = self.session.get(item_img['img_url'], verify=False)
        with open('img.png', 'wb')as f:
            f.write(response.content)
        return item_img

    def build_fs(self, angle,ass,backstr)->str:
        tt = {
            "cl": [
                {
                    "x": 862,
                    "y": 287,
                    "t": 1657760616916
                }
            ],
            "mv": [
                {
                    "fx": 987,
                    "fy": 149,
                    "t": 1657760613905,
                    "bf": 2
                },
                {
                    "fx": 979,
                    "fy": 370,
                    "t": 1657760615529,
                    "bf": 2
                },
                {
                    "fx": 948,
                    "fy": 339,
                    "t": 1657760615688,
                    "bf": 2
                },
                {
                    "fx": 911,
                    "fy": 321,
                    "t": 1657760615848,
                    "bf": 2
                },
                {
                    "fx": 892,
                    "fy": 309,
                    "t": 1657760616008,
                    "bf": 2
                },
                {
                    "fx": 880,
                    "fy": 299,
                    "t": 1657760616176,
                    "bf": 2
                },
                {
                    "fx": 869,
                    "fy": 290,
                    "t": 1657760616440,
                    "bf": 2
                },
                {
                    "fx": 864,
                    "fy": 288,
                    "t": 1657760616641,
                    "bf": 2
                },
                {
                    "fx": 862,
                    "fy": 287,
                    "t": 1657760616866,
                    "bf": 2
                },
                {
                    "fx": 864,
                    "fy": 288,
                    "t": 1657760617026,
                    "bf": 1
                },
                {
                    "fx": 877,
                    "fy": 293,
                    "t": 1657760617186,
                    "bf": 1
                },
                {
                    "fx": 882,
                    "fy": 295,
                    "t": 1657760617360,
                    "bf": 1
                },
                {
                    "fx": 891,
                    "fy": 298,
                    "t": 1657760617537,
                    "bf": 1
                },
                {
                    "fx": 900,
                    "fy": 300,
                    "t": 1657760617688,
                    "bf": 1
                },
                {
                    "fx": 908,
                    "fy": 301,
                    "t": 1657760617864,
                    "bf": 1
                },
                {
                    "fx": 910,
                    "fy": 301,
                    "t": 1657760618585,
                    "bf": 1
                }
            ],
            "sc": [],
            "kb": [
                {
                    "key": "a",
                    "t": 1657760606047
                }
            ],
            "sb": [],
            "sd": [],
            "sm": [],
            "cr": {
                "screenTop": 0,
                "screenLeft": 0,
                "clientWidth": 1920,
                "clientHeight": 979,
                "screenWidth": 1920,
                "screenHeight": 1080,
                "availWidth": 1920,
                "availHeight": 1050,
                "outerWidth": 1920,
                "outerHeight": 1050,
                "scrollWidth": 1920,
                "scrollHeight": 1920
            },
            "simu": 0,
            "ac_c": round((angle * 212 / 360 / 212),2),
            "backstr": backstr
        }

        tt = json.dumps(tt)
        # print(tt)
        # print("key = ", ass + 'appsapi0')
        return aesEncrypt(ass+'appsapi0',tt)

    def verify_data(self, item):
        url = "https://passport.baidu.com/viewlog"
        print("angle：", item['angle'])
        print("as：", item['as'])
        # with open('get_encrypt.js', 'r', encoding='utf-8') as f:
        #     js_text = f.read()
        # fs = execjs.compile(js_text).call('encrypt_', str(item['angle']), str(item['as']), str(item['backstr']))
        # print("fs：", fs)
        fs = self.build_fs(int(item['angle']), item['as'], item['backstr'])

        params = {
            "callback": "jQuery110204100787474351779_" + str(time.time() * 1000),
            "ak": "3de47787fd60b30420f868ffbf4dbccd",
            "as": item['as'],
            "fs": fs,
            "tk": item['tk'],
            "cv": "submit",
            "_": str(time.time() * 1000)
        }
        response = self.session.get(url, headers=self.headers, params=params)
        ret_data = re.findall(r'.*?(\{.*?})\)', response.text)[0]
        ret_data = json.loads(ret_data)
        # print("验证结果：", ret_data)
        return ret_data




if __name__ == '__main__':
    bs = BaiduAiqichaRotate()
    item = bs.get_image_request_data()
    item_img = bs.get_img(item)
    with open('img.png',mode='rb') as f :
        content = f.read()
    base64_data = base64.b64encode(content)
    angle = dama_api(base64_data)
    item_img['angle'] = angle
    # print(item_img)
    ret_data = bs.verify_data(item_img)
    if 1 == ret_data['data']['op']:
        print("验证通过")
