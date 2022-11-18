import csv
import json
from time import time
import os
import requests
import re

# 以csv形式存储
def save_csv(list):
    field_name = ['day', 'open', 'high', 'low', 'close', 'volume']
    with open(f'{stock_code}.csv', mode='a', newline='', encoding='utf-8-sig') as f:
        write = csv.DictWriter(f, fieldnames=field_name)
        if not os.path.getsize(f'{stock_code}.csv'):
            write.writeheader()
        write.writerows(stock_info_list)
        print("保存成功")
stock_code = 'sh600010' # 股票代码
scale = 240 # 日线
datalen = 60 # 获取数据条数

# 当前时间戳
now = int(time()*1000)  #js是毫秒级别

# 请求的url地址
req_utl = f'https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_{stock_code}_{scale}_{now}=/CN_MarketDataService.getKLineData'

# get请求参数
params = {
    'symbol':stock_code,
    'scale':scale,
    'ma':'no',
    'datalen':datalen
}

res = requests.get(req_utl,params=params)
# 提取括号里的内容
p1 = re.compile(r"[(](.*?)[)]", re.S)
json_str = re.findall(p1,res.text)[0]


stock_info_list = json.loads(json_str)
save_csv(stock_code)






