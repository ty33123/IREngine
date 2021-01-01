import pickle
from datetime import datetime

from IREngine import app, db
import json, math, time
from flask import request, render_template, flash, abort, url_for, redirect, session, Flask, g, make_response
from sqlalchemy import func
from IREngine.model.news_data import news_data
import numpy as np
from IREngine.tools.divide import divide
from IREngine.tools.recom_artile import Recom_Artile
import requests

print("loading index....")
gram_index = pickle.load(open("IREngine/index_file/gram.index", "rb"))
score_dict = pickle.load(open("IREngine/index_file/score_dict.index", "rb"))
print("loading index finished!")
RecomA = Recom_Artile("IREngine/index_file/idf_dict.index")


# 检索
@app.route('/search')
def admin_search():
    start_time = time.time()
    q = request.args.get('q')
    id_list, term_list = search(q)
    page = int(request.args.get('page'))
    if type(page) is not int:
        page = 1
    search_type = request.args.get('type')
    if search_type == "undefined":
        search_type = ""
    news_num = len(id_list)
    total_page = math.ceil(news_num / 10)
    id_list = id_list[page * 10 - 10:page * 10 - 1]
    items = []
    lines = []
    flag = True
    for id in id_list:
        news_dict = news_data.query.filter(news_data.id == id).first().dict()
        q_loc = news_dict['content'].find(q)
        s_loc = 0 if q_loc - 100 < 0 else q_loc - 100

        if q_loc > 0:
            news_dict['content'] = news_dict['content'][s_loc:s_loc + 200].replace(q,
                                                                                   "<span style='color:red;'>" + q + "</span> ") + "..."
            if flag: lines.append(news_dict['content'][s_loc:s_loc + 200])
        else:
            news_dict['content'] = news_dict['content'][0:200]
            if flag: lines.append(news_dict['content'][0:200])
        flag = False
        items.append(news_dict)
    # =============================================摘要是否启用============================
    # headers = {'Content-Type': 'application/json'}
    # model_res = requests.post("http://127.0.0.1:3123/getSummary", headers=headers, json=dict(lines=lines))
    # model_json = json.loads(model_res.text)
    # items[0]['content'] = "<span style='color:red;'>摘要：" + model_json[0][0] + "</span> |#| " + items[0]['content']
    # =============================================摘要是否启用============================
    if search_type == "byTime":
        items = sorted(items, key=lambda doc: doc['publish_time'], reverse=True)
    if search_type == "byHot":
        items = sorted(items, key=lambda doc: doc['read_counts'], reverse=True)

    data = json.dumps(dict(items=items, used_time=time.time() - start_time, total_page=total_page, news_num=news_num))
    rsp = make_response(data)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    return rsp


# 根据新闻id获取新闻记录
@app.route('/query/news_id.json', methods=['POST'])
def get_news_byid():
    data = request.get_json()
    id = data['id']
    news_dict = news_data.query.filter(news_data.id == id).first().dict()
    data = json.dumps(dict(item=news_dict))
    rsp = make_response(data)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    return rsp


@app.route('/recom_news', methods=["POST"])
def recom_news():
    t = time.time()
    data = request.get_json()
    id = data['id']
    id_list = RecomA.recom_artile(int(id) - 1)
    items = []
    for id in id_list:
        news_dict = news_data.query.filter(news_data.id == id).first().dict()
        items.append(news_dict)
    data = json.dumps(dict(items=items))
    rsp = make_response(data)
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    print(time.time() - t)
    return rsp


def search(qs):
    dv = divide()
    query = []
    query_id = {}
    if "*" in qs:
        temp = qs.split("*")
        temp[0] = "$" + temp[0]
        temp[-1] = temp[-1] + "$"
        for t in temp:
            for i in range(len(t) - 1):
                term = t[i:i + 2]
                if gram_index.__contains__(term):
                    if not query_id:
                        query_id = term_doc_id(term)
                    else:
                        query_id = dict_intersection(query_id, term_doc_id(term))
        for s in query_id.keys():
            query_id[s][0] = query_id[s][0] / query_id[s][1]
        doc_list = sorted(query_id.items(), key=lambda item: item[1][0], reverse=True)
        res = doc_list
    else:
        query = dv.stop_word(dv.divide(qs))
        res = cal_score(query, score_dict)
    return_list = []
    for item in res:
        return_list.append(item[0])
    return return_list, query


def cal_score(query, score_dict):
    doc_dict = {}
    for term in query:
        if not score_dict.__contains__(term):
            continue
        for item in score_dict[term].items():
            if not doc_dict.__contains__(item[0]):
                doc_dict[item[0]] = item[1]
            else:
                doc_dict[item[0]] += item[1]

    doc_list = sorted(doc_dict.items(), key=lambda item: item[1], reverse=True)
    return doc_list
    # doc_list: [(doc_id,score)...]


def term_doc_id(term):
    terms = gram_index[term]
    score_table = {}
    # {id:[score,counts]}
    for t in terms:
        temp = score_dict[t]
        for k in temp.keys():
            if score_table.__contains__(k):
                score_table[k][0] = score_table[k][0] + temp[k]
                score_table[k][1] += 1
            else:
                score_table[k] = [temp[k], 1]

    return score_table


def dict_intersection(dict1, dict2):
    res = {}
    for k in dict1.keys():
        if dict2.__contains__(k):
            res[k] = np.add(dict1[k], dict2[k])
    return res
