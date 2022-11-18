
import os
from time import sleep
from typing import final
import requests
from bs4 import BeautifulSoup
import datetime
from concurrent.futures import ThreadPoolExecutor
class Cls:
    # 初始化请求信息
    def __init__(self):
        self.headers = {
            "Content-Type": "text/html; charset=utf-8",
            "referer": "http://www.macrolink.com.cn/index.php?com=com_newspapers&auto_code=1195",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "Cookie": "PHPSESSID=9a00c8fd80ed09c8a7eeedae5db54d98",
            "Upgrade-Insecure-Requests": "1"
        }
    # 获取多个图片列表信息
    def get_imageList(self,url):
        #将所有url放入urlList
        urlList = []
        # 获取页面内的所有url
        res = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(res.text,"html.parser")
        # 获取期刊名字
        date_name = soup.find("div",attrs={"class":"maz-data"}).text
        # print(date_name)
        # 获取div列表
        div_list = soup.find_all("div",attrs={"class":"maz-list"})
        print(f"div_list={div_list}+date_name={date_name}")
        for div in div_list:
            a_list = div.find_all("a")
            for a in a_list:
                href = a['href']
                # 获取单个图片信息
                one_ImageInfo = self.get_one_ImageInfo(href)
                # 如果图片不存在
                if(len(one_ImageInfo) == 0):
                    continue
                urlList.append(one_ImageInfo)

        # 最后返回本期的图片列表信息
        # return {"date_name":date_name,"urlList":urlList}
        result = {"date_name":date_name,"urlList":urlList}
        return result

    # 获取单个图片信息
    def get_one_ImageInfo(self,url):
        res = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(res.text,"html.parser")
        # 获取标题
        title = soup.select(".core h3")[0].text

        # 不存在图片时
        if(len(soup.select(".content p img"))<1):
            return {}
        # 获取图片url
        image_url = soup.select(".content p img")[0]['src']
        print(title)
        print(url)

        # 找到属性列表
        infoList = soup.select(".source ul li")
        # 存放图片信息
        author = infoList[0].text.split('：')[1]
        date = infoList[1].text.split('：')[1]
        referer = infoList[2].text.split('：')[1]
        imagesInfo = {}
        imagesInfo["url"] = image_url
        imagesInfo["title"] = title
        imagesInfo["author"] = author
        imagesInfo["date"] = date
        imagesInfo["referer"] = referer
        return imagesInfo
        
    #保存图片
    def download_images(self,url,date_name,fullName):  
        print(f"{date_name}~正在下载当前模块")
        # 写入图片
        res = requests.get(url,headers=self.headers)
        with open(f"./{date_name}/{fullName}.jpg","wb") as f:
            f.write(res.content)
        

    def main(self):
        base_url = "http://www.macrolink.com.cn/index.php?com=com_newspapers&auto_code="
        for code in range(1191,1196):
            url = f'{base_url}{code}'
            print(url)
            # 获取图片列表信息
            imagesInfo = self.get_imageList(url)

            date_name = imagesInfo["date_name"]
            imageList = imagesInfo["urlList"]
            # 没有改文件夹则创建
            total = len(imageList)
            if(total == 0):
                continue
            if not os.path.exists(f"./{date_name}"):
                os.makedirs(f"./{date_name}")
            i = 1
            
            print(total)
            with ThreadPoolExecutor(100) as executor:
                for imageInfo in imageList:
                    url = imageInfo["url"]
                    title = imageInfo["title"]
                    date = imageInfo["date"]
                    author = imageInfo["author"]
                    referer = imageInfo["referer"]
                    fullName = f"{title}+{date}+{author}+{referer}"
                    executor.map(self.download_images, {url},{date_name}, {fullName})
                    print("???")
                    if(not total == 0):
                        print(f"当前下载进度：{i/total}%")
                

               

    def run(self):
        self.main()
        # imagesInfo = self.get_imageList("http://www.macrolink.com.cn/index.php?com=com_newspapers&auto_code=1195")
        # print(imagesInfo)
        # # self.get_one_ImageInfo("http://www.macrolink.com.cn/index.php?optionid=988&com=com_newspapers&auto_id=6707&auto_code=11951007")
        # self.download_images(imagesInfo)
        
if __name__ == '__main__':
    t = Cls()
    t.run()
    


