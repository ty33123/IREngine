
import requests
import json
from bs4 import BeautifulSoup
import datetime
from db_tools import db_tools

cls_list = ['BBM54PGAwangning', 'BD29MJTVwangning', 'BD29LPUBwangning']
#              首页                 国际                 国内
headers = {
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
          }
max_pn = 31

def get_news_list(cls, pn, db):
    flag = 0
    # print("https://3g.163.com/touch/reconstruct/article/list/{}/{}-10.html".format(cls, pn))
    req = requests.get("http://3g.163.com/touch/reconstruct/article/list/{}/{}-10.html".format(cls, pn))
    news_list = []
    res = json.loads(req.text[9:-1])
    for item in res[cls]:
        if flag >= 6:
            return 0
        url = "http://3g.163.com/news/article/{}.html".format(item['docid'])
        if db.query(url, "news_data") > 0:
            flag += 1
            continue
        dateTime_p = datetime.datetime.now()
        str_p = datetime.datetime.strftime(dateTime_p, '%Y-%m-%d %H:%M:%S')
        news = dict(url=url, title=item['title'], publish_time=item['ptime'], content=get_news_content(url),
                    source="网易新闻", collect_time=str_p)
        db.insert(news, "news_data")
        news_list.append(news)


    return len(news_list)


def get_news_content(url):
    req_content = requests.get(url)
    soup = BeautifulSoup(req_content.text, 'html.parser')
    lines = soup.select(".content")[0].text
    new_lines = []
    for line in lines:
        if line.strip() == "":
            continue
        else:
            new_lines.append(line)
    return "".join(new_lines)

        # print(etree.tostring(root, encoding="unicode", method="text", with_tail=False))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db = db_tools()
    db.connect()
    for cls in cls_list:
        for p in range(0, max_pn):
            print(p, cls)
            try:
                if get_news_list(cls, p*10, db) == 0:
                    break
            except Exception as e:
                print(e)
                continue
    db.close()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
