from datetime import datetime
from datetime import timedelta

from IREngine import app, db
from flask import request, render_template, flash, abort, url_for, redirect, session, Flask, g, make_response
from sqlalchemy import func
from IREngine.model.news_data import news_data

import json, time, math
import urllib.parse


# 进行网页的重定向
from IREngine.tools.recom_query import Recom_Query

RecomQ = Recom_Query('IREngine/index_file/idf_dict_term_recom.pickle',
                        'IREngine/index_file/term_list_recom.pickle' )


@app.route('/re_direct')
def re_direct():
    temp = request.url
    url = urllib.parse.unquote(temp[temp.find("url=") + 4:], "utf-8")
    r = news_data.query.filter(news_data.url == url).first()
    if r is not None:
        r.read_counts += 1
        db.session.commit()
    return redirect(url)


# 获取最高阅读
@app.route('/get_readtop.json')
def get_readtop():
    rs1 = news_data.query.filter(news_data.publish_time > (datetime.now() - timedelta(days=30))).order_by(
        db.desc(news_data.read_counts)).limit(5)
    items = []
    for r in rs1:
        items.append(dict(url=r.url, title=r.title, read_counts=r.read_counts))
    data = json.dumps(dict(items=items))
    rsp = make_response(data)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    return rsp


# 获取最高阅读
@app.route('/rel_query.json', methods=['POST'])
def rel_query():
    items = []
    data = request.get_json()
    query_word = data['qw']
    rel_query_data = RecomQ.recom_query(query_word)
    for i in rel_query_data:
        items.append(dict(link="/s?wd="+i, title=i))
    # for r in rs1:
    #     items.append(dict(link=r.link, title=r.title, read_counts=r.read_counts))
    data = json.dumps(dict(items=items))
    rsp = make_response(data)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    return rsp


def strtodate(string):
    try:
        return datetime.strptime(string, "%Y年%m月%d日")
    except:
        return datetime.strptime('2019年1月1日', "%Y年%m月%d日")
