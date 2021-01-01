import requests
import re
import unicodedata
from bs4 import BeautifulSoup
import sys
import datetime
from db_tools import db_tools
#import pandas as pd
url0 = "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/"
#China https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
#World https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_1.jsonp?cb=world
#Society https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/society_1.jsonp?cb=society
#Law https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/law_1.jsonp?cb=law
#Entertainment https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/ent_1.jsonp?cb=ent
#Technology https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/tech_1.jsonp?cb=tech
#Life https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_1.jsonp?cb=life
sign = 1 #时间标志
f=open('time.dat','r+')
time_old = f.readline()

fake_headers = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'
    }
#response = requests.get(url,headers = fake_headers)
#news_url = get_news_list_url(url0)
type = ['china','world','society','law','ent','tech','life']

db = db_tools()
db.connect()

def get_news_list_url(url0):
    news_url_list=[]
    news_url=[]
    for n in range(1,8):
        for t in type:
        
            news_url_list.append(url0+t+'_'+str(n)+".jsonp?cb="+t)
    for json_url in news_url_list:
        response = requests.get(json_url,headers = fake_headers)
        news_url+=re.findall(r'"url":"https:.+?shtml"',response.content.decode('utf-8',errors='ignore'))
    return news_url    
#fake_headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'}
news_url = get_news_list_url(url0)
#print(news_url)

#
url=[]

n=0

for item in news_url:
    url+=re.findall(r'https:.+?shtml',item)
for item in url:
    response = requests.get(item,headers = fake_headers)
    soup=BeautifulSoup(response.content,'html.parser')
    text = title=soup.select('.title_area h1')
    title=''
    for t in text:
        title += t.text.strip()
    #contentt = re.sub(r'<.+?>','',str(soup.find_all('div',id='content_area')))
    timet = re.findall(r'\d\d\d\d.+\d\d',str(soup.find_all('div',class_='info1')))
    text = soup.select(".content_area p")
    content=''
    for t in text:
        content += t.text.strip()
    
    timet = re.sub(r'[年月]','-',str(timet))
    
    timet = re.sub(r'[日]','',timet)
    
    timet = timet[2:18]+':00'
    if sign :
        time2write = timet
        sign = 0
    #print(timet)
    if timet<time_old:
        break
    dateTime_p = datetime.datetime.now()
    str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
    news=dict(url=item,title=title,
                  #publish_time=(str(timet)+':00'),
              publish_time=timet,
              content=content,source="央视新闻",
              collect_time=str_p
              )
    db.insert(news,"news_data")
        
        #item_id.append(n)
    #n+=1
    #print(n)
    #break
#data = pd.DataFrame({'id':item_id,'url':url,'time':time,'title':title,'content':content})
#data.to_csv('data.csv',sep=',')
f.seek(0)
f.truncate()
f.write(time2write)
f.close
db.close()
