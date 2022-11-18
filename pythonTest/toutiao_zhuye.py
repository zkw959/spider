
import os
from time import sleep
from openpyxl import workbook
import requests

class Toutiao:
    def __init__(self):
        self.req_url = " https://www.toutiao.com/api/pc/list/user/feed"
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "referer": "https://www.toutiao.com/c/user/token/MS4wLjABAAAAP09LrX61xFpIWrgGdBDqkp-5om9Lans_kuIZ_ipAGRE/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
        }
        self.params = {
            "category": "profile_all",
            "token": "MS4wLjABAAAAP09LrX61xFpIWrgGdBDqkp-5om9Lans_kuIZ_ipAGRE",
            "max_behot_time": 1652494835823,
            "aid": 24,
            "app_name": "toutiao_web",
            "_signature":"_02B4Z6wo00d01gEiCTQAAIDDimmS1Yl-jFIBBg2AAOJFeF02Lluw6XPPidig3Vaiibbyu1ZhqXu-4alxacyy9DFn8-Jo072DTKkaRjzcKWL87mq-HILKVGxWHODsqJ2q61iPy4.hFeErOcCh73"
        }
    #获取签名
    def get_signature(self):
        re = os.popen('node ../toutiao2.js')
        _signature = re.read()
        re.close()
        return _signature.strip()

    #获取新闻
    def getNews(self):  
        # self.params['_signature'] = self.get_signature()
        res = requests.get(self.req_url,headers=self.headers,params=self.params)
        res_dc = res.json()
        print(res_dc['has_more'])  



    def run(self):
        self.getNews()

if __name__ == '__main__':
    t = Toutiao()
    t.run()
    


