
import json
import os
from time import sleep
import time
import requests
from bs4 import BeautifulSoup

class Cls:
    # 初始化请求信息
    def __init__(self):
        self.req_url = " https://www.cls.cn/nodeapi/telegraphList"
        self.headers = {
            "Content-Type": "application/json;charset=utf-8",
            "referer": "https://www.cls.cn/telegraph",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Cookie": "HWWAFSESID=2405e76de2aee92ffd; HWWAFSESTIME=1656830370636; Hm_lvt_fa5455bb5e9f0f260c32a1d45603ba3e=1656418533,1656511029,1656780144,1656830374; hasTelegraphNotification=on; hasTelegraphRemind=on; hasTelegraphSound=on; vipNotificationState=on; isMinimize=off; Hm_lpvt_fa5455bb5e9f0f260c32a1d45603ba3e=1656854735"
        }
        self.params = {
            "app": "CailianpressWeb",
            "category": '',
            "lastTime": "1656843382",
            "last_time": "1656843382",
            "os": "web",
            "refresh_type": "1",
            "rn": "20",
            "sv": "7.7.5",
            "sign": self.get_sign("1656843382")
        }
    #获取签名
    def get_sign(self,lastTime):
        # 强制转换为字符串
        if(type(lastTime) != str):
            lastTime = str(lastTime)
        
        re = os.popen('node ./getSign.js '+ lastTime)
        sign = re.read()
        re.close()
        return sign.strip()
    # 获取头部电报信息
    def getinitTelegraphList(self):
        res = requests.get('https://www.cls.cn/telegraph',headers=self.headers)
        soup = BeautifulSoup(res.text,'html.parser')
        # 获取初始数据的json字符串
        initData = json.loads(soup.select('#__NEXT_DATA__')[0].text)
        # 将json字符串转换为字典,定位到telegraphList
        telegraphList = initData['props']['initialState']['telegraph']['telegraphList']
        # 首个电报的ctime作为属性
        self.firstCreateTime = telegraphList[0]['ctime']
        # print(self.firstCreateTime)
        # 按格式化输出数据
        self.printFormat(telegraphList)

    #获取电报信息
    def getTelegraphList(self):  
        # self.params['_signature'] = self.get_signature()
        res = requests.get(self.req_url,headers=self.headers,params=self.params)
        res_dc = res.json()
        roll_data = res_dc['data']['roll_data']
        # 按格式化输出数据
        self.printFormat(roll_data)

    # 按照指定格式输出数据
    def printFormat(self,dataList):
        print("内容\t\t\t\t\t创建时间")
        for data in dataList:
            lastTime = data['ctime']
            print(data['content']+'\t%s'%time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(data['ctime'])))
        if(lastTime > 0):
            self.params["lastTime"] = str(lastTime)
            self.params["last_time"] = str(lastTime)
            self.params["sign"] = self.get_sign(lastTime)
            sleep(3)
            print('\n\n\n')
            self.getTelegraphList()
    def run(self):
        # print(self.get_sign("1656843382"))
        self.getinitTelegraphList()
        
if __name__ == '__main__':
    t = Cls()
    t.run()
    


