import json

from IREngine import app
from flask import request, render_template, session
from IREngine.tools.jieba_ir import jieba
#------------------------------------静态网页部分------------------------------------------------


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/s')
def search():
    wd = request.args.get("wd")
    return render_template('query_1.html',wd=wd)

@app.route('/test')
def test():
    item = []
    for i in jieba.cut('这是一个测试'):
        item.append(i)
    return json.dumps(item)


# 爬虫管理页面：

@app.route('/spider')
def index():
    return render_template('/spider_manager/admin-list.html')


@app.route('/err-list.html')
def err_list_html():
    return render_template("/spider_manager/err-list.html")


@app.route('/admin-add.html')
def admin_add_html():
    return render_template("/spider_manager/admin-add.html")