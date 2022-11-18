from time import sleep
import requests
import json
from datetime import datetime, timedelta
from enum import Enum

price = '3.59'
type = '1'
tur = 400000
StockID = '000620'

header = {
        
        'Content-Type':'application/x-www-form-urlencoded; charset=utf-8',
        'Connection':'keep-alive',
        'Accept':'*/*',
        'User-Agent':'Mozilla/5.0 (Linux; Android 7.1.2; SM-N976N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36;kaipanla 5.6.0.2',
        'Accept-Language':'zh-Hans-CN;q=1.0, en-CN;q=0.9',
    }
data = {
        'Index':0,
        'PhoneOSNew':2,
        'StockID':StockID,
        'Tur':30,
        'Type':3,
        'VOrder':'',
        'VType':1,
        'VerSion':'5.7.0.1',
        'Vol':500,
        'a':'GetWeiTuo_W14',
        'apiv':'w31',
        'c':'StockL2Data',
        'st':50
}


# 获取今天任意时刻的时间戳
def today_anytime_tsp(hour, minute, second=0):
    now = datetime.now()
    today_0 = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)  
    today_anytime = today_0 + timedelta(hours=hour, minutes=minute, seconds=second)
    tsp = today_anytime.timestamp()

    return int(tsp)


time_start = today_anytime_tsp(9,20,0)
time_end = today_anytime_tsp(9,25,0)


# 指定时间范围获取数据
def save_data_list(taget_list,list_data,time_start,time_end):
    flag = False
    for i in list_data:
        if(time_start<= int(i[9]) < time_end):
            taget_list.append(i)
        elif(int(i[9]) > time_end):
            # 一旦是超出结束时间的设置为True
            flag = True
    return flag


def get_data_list():
    # 返回的最终列表
    data_list = []

    res = requests.post("https://apphq.longhuvip.com/w1/api/index.php",headers=header,data=data)
    json = res.json()
    
    if(save_data_list(data_list,json['List'],time_start,time_end)):
        return data_list

    
    # 如果25分之前还有数据则循环
    while(json['Count'] > data['Index']):
        data['Index'] = data['Index'] + data['st']

        res = requests.post("https://apphq.longhuvip.com/w1/api/index.php",headers=header,data=data)
        json = res.json()

        if(save_data_list(data_list,json['List'],time_start,time_end)):
            break
        
        data['st'] += 1
        sleep(0.5)
        
    return data_list

data_list = get_data_list()


vol_total = 0
for i in data_list:
    if(
        i[5] == type 
        and i[2] > price 
        and (int(i[4]) >= tur)
    ):
        vol_total += int(i[3])
        print(f'time={i[0]} price={i[2]} vol={i[3]} tur={i[4]}')
print(vol_total)