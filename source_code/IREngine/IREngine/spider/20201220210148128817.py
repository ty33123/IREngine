# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import datetime
import time
from db_tools import db_tools

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
          }
max_pn = 500

def get_news_page(pn, db):
    req = requests.get("https://v2.sohu.com/integration-api/mix/region/15154? SUV=2009171942306CTV&pvId=2009171942306CTV&page={}&size=20".format(pn),headers=headers)
    #print(req.text)
    req.encoding = 'utf-8'
    news_list = []
    req=req.text
    #print(req)
    res = json.loads(req)
    print(pn)
    for item in res['data']:
        try:
           url = "https://www.sohu.com/a/{}_{}.html".format(item['id'],item['authorId'])
           print(url)
           dateTime_p = datetime.datetime.now()
           str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
           #print(str_p)
           timeStamp = item['publicTime']
           timeArray = time.localtime(int(timeStamp/1000))
           p_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
           #print(p_time)
           news = dict(url=url, title=item['title'], publish_time=p_time, content=get_news_content(url),
                    source="搜狐新闻", collect_time=str_p)
           
           if db.query(url, "news_data") == 0:
               db.insert(news, "news_data")
        except:
            continue
        news_list.append(news)
    return len(news_list)

def get_news_content(url):
    req_content = requests.get(url)
    soup = BeautifulSoup(req_content.text, 'html.parser')
    texts = soup.find_all('p')
    a_content = ""
    i=0
    for text in texts:
         temp=text.text
         if i>1:
             a_content += temp
         i+=1
    return a_content

if __name__ == '__main__':
    db = db_tools()
    db.connect()
    for p in range(1, max_pn):
        try:
            if get_news_page(p,db) == 0:
                break
        except:
            continue
    db.close()

