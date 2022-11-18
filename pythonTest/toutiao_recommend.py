
import os
from pickle import TRUE
import random
from time import sleep
import time
import requests

class Toutiao:
    def __init__(self):
        self.req_url = "https://www.toutiao.com/api/pc/list/feed"
        self.headers = {
        'referer': 'https://www.toutiao.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
        }
        self.params = {
            "channel_id": 0,
            "max_behot_time": 0,
            "category": "pc_profile_recommend",
            "aid": 24,
            "app_name": "toutiao_web",
            "_signature":"_02B4Z6wo00f01ye5i3wAAIDA2EZ0ghe34pcnm4.AAKubvFxtp1IJ0VqvXRcU3yMKdHJwchjXkGTTwDIbpaXBppPNY.3x1FTQiQHRA8gftliHCJmlBkr2tiyxwLYxHVTQc6PvfBqRHGcoewfIbd"
        }
    #获取签名
    def get_signature(self):
        re = os.popen('node ../toutiao.js')
        _signature = re.read()
        re.close()
        return _signature.strip()

    #获取新闻
    def getNews(self):
        print("标题\t\t\t日期")
        while TRUE:
            self.params['_signature'] = self.get_signature()

            res = requests.get(self.req_url,headers=self.headers,params=self.params)
            res_dc = res.json()
            
            #遍历获取的数据
            for i in res_dc['data']:
                publish_time = i['publish_time']
                format_publish_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(publish_time))
                print(i['title'] + "\t\t" + format_publish_time)

            #是否还有数据
            if(res_dc['has_more']):
                self.params['max_behot_time'] = i['behot_time']
                print("---------------------")
                sleep(random.randint(2,4))
            else:
                break

    def run(self):
        self.getNews()

if __name__ == '__main__':
    t = Toutiao()
    t.run()
    


