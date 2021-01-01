import requests
import re
import unicodedata
from bs4 import BeautifulSoup
import sys
import datetime
from db_tools import db_tools
import time
#import pandas as pd
url0 = "https://www.ithome.com/list/2019-"

#Remove "'" in artile

regex = re.compile(r"'")
#IT home https://www.ithome.com/list/2020-11-01.html

#China https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp?cb=china
#World https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/world_1.jsonp?cb=world
#Society https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/society_1.jsonp?cb=society
#Law https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/law_1.jsonp?cb=law
#Entertainment https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/ent_1.jsonp?cb=ent
#Technology https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/tech_1.jsonp?cb=tech
#Life https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/life_1.jsonp?cb=life

sign = 1 #时间标志

fake_headers = {    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'    }
#response = requests.get(url,headers = fake_headers)
#news_url = get_news_list_url(url0)
#type = ['china','world','society','law','ent','tech','life']

db = db_tools()
db.connect()

month=['9','10','11','12']

#已经抓取的月份 1~11

# for n in range(1,11):
#     month.append(str(n))
    

def get_news_list_url(url0):
    news_url_list=[]
    news_url=[]
    for m in month:
        #day = []
        if (m=='1' or m=='3' or m=='5' or m=='7' or m=='8' or m=='10' or m=='12'):
            for n in range(1,32):
                news_url_list.append(url0+m+'-'+str(n)+'.html')
        elif (m=='4' or m=='6' or m=='9' or m=='11'):
            for n in range(1,31):
                news_url_list.append(url0+m+'-'+str(n)+'.html')
        else:
            for n in range(1,29):
                    news_url_list.append(url0+m+'-'+str(n)+'.html')
        

    for url in news_url_list:
        response = requests.get(url,headers = fake_headers)
        for t in BeautifulSoup(response.content,'html.parser').select('.t'):
            news_url.append(t.get('href'))
    return news_url    
#fake_headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43'}
news_url = get_news_list_url(url0)
#print(news_url)

#




for item in news_url:
    try:
        response = requests.get(item,headers = fake_headers)
        soup=BeautifulSoup(response.content,'html.parser')
        text = soup.select('.post_content p')
        content=''
        for t in text:
            content += t.text.strip()
        content = re.sub(regex, ' ', content)
    #contentt = re.sub(r'<.+?>','',str(soup.find_all('div',id='content_area')))
        timep = soup.find('span',id='pubtime_baidu').text
        time0 = time.strptime(timep,'%Y/%m/%d %H:%M:%S')
        timep = time.strftime("%Y-%m-%d %H:%M:%S", time0)
        title = re.sub(regex, ' ', soup.find('h1').text)
    #title=''

    
    #print(timep)
        dateTime_p = datetime.datetime.now()
        str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
        news=dict(url=item,title=title,
                  #publish_time=(str(timet)+':00'),
                  publish_time=timep,
                  content=content,source="IT之家",
                  collect_time=str_p
                  )
        db.insert(news,"news_data")
    except Exception as e:
        pass
        print(item)
    continue
        #item_id.append(n)
    #n+=1
    #print(n)
    #break
#data = pd.DataFrame({'id':item_id,'url':url,'time':time,'title':title,'content':content})
#data.to_csv('data.csv',sep=',')

db.close()
