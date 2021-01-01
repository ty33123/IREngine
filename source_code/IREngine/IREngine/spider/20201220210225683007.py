"""
@author: SongMX
@e-mail: smxiao@outlook.com
@introduction:
    新浪新闻网站爬取
"""
import requests
from bs4 import BeautifulSoup
import re
import datetime
from db_tools import db_tools

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error!!!'

def parsePage(html, list):
    soup = BeautifulSoup(html, "html.parser")
    flag=True
    count=0
    try:
        for li in soup.find_all('div', {'class':'main-content'}):
            for link in li.find_all('a', href = re.compile('^(https://news.sina.com.cn/).*')):
                text = link.get_text().replace('\n', '')
                ur = link.attrs["href"]
                html2=getHTMLText(ur)
                soup2=BeautifulSoup(html2,"html.parser")
                try:
                    p_time=datetime.datetime.strptime(soup2.select('.date-source')[0].select('.date')[0].text,"%Y年%m月%d日 %H:%M")#
                    p_time=datetime.datetime.strftime(p_time,'%Y-%m-%d %H:%M')
                except Exception:
                    print("时间格式错误！！！")
                    continue
                a_content='  '.join([p.text.strip() for p in soup2.select('#article p')[:-1]])
                dateTime_p = datetime.datetime.now()
                str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
                news = dict(url=ur, title=text, publish_time=p_time, content=a_content,source="新浪新闻", collect_time=str_p)
                #if db.query(ur,"news_data_test")==0:
                db.insert(news, "news_data_test")
                list.append([ ur,text,a_content,str_p,p_time])
                count+=1
                if count>=500:
                    print("结束！！！")
                    flag=False
                    break
            if flag==False:
                break
    except AttributeError as e:
        print(e)

def printList(ulist, num):
    for i in range(num):
        print(ulist[i][0], ulist[i][1], ulist[i][2], ulist[i][3], ulist[i][4])

if __name__ == '__main__':
    db = db_tools()
    db.connect()
    url = 'https://news.sina.com.cn/china/'
    html = getHTMLText(url)
    ulist = []
    parsePage(html, ulist)
    #url2 = 'https://news.sina.com.cn/world/'
    #html3 = getHTMLText(url2)
    #ulist2 = []
    #parsePage(html3, ulist2)
    #printList(ulist, 4)
    db.close()


