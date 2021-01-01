# -*- coding: utf-8 -*-#
# Name:         spider_manager
# Description:  
# Author:       刘天昀
# Date:         2020/12/18

from IREngine import app, scheduler, db
from flask import render_template, request, jsonify, make_response, send_file
import datetime
import os
import time
import json
import re
from IREngine.model.Spider import Spider
from IREngine.model.ErrLog import ErrLog


@app.before_first_request
def start_spider():
    print("启动:")
    spiders = Spider.query.filter(Spider.enabled == True).all()
    for spider in spiders:
        id = str(spider.id)
        add_task(id, spider.type, spider.file_name, spider.params)
    print(scheduler.get_jobs())


# 爬虫列表
@app.route('/spider_list')
def spider_list():
    starttime = time.time()
    items = []
    rs = None
    if "name" not in request.args.keys():
        rs = Spider.query.all()
    else:
        rs = Spider.query.filter(Spider.name.like('%' + request.args['name'] + '%')).all()
    for r in rs:
        items.append(dict(id=r.id, name=r.name, desc=r.description, type=r.type, params=r.params,
                          last_acq_num=r.last_acq_num, url=r.url,
                          acq_num=r.acq_num, is_error=r.is_error, last_run_time=str(r.last_run_time),
                          next_run_time=str(r.next_run_time), enabled=r.enabled, file_name=r.file_name))

    usedtime = time.time() - starttime
    data = json.dumps(dict(usedtime=usedtime, items=items))

    rsp = make_response(data)

    rsp.headers['Access-Control-Allow-Origin'] = '*'

    return rsp


# 异常列表
@app.route('/error_list')
def error_list():
    starttime = time.time()
    items = []
    rs = None
    if "spider_name" not in request.args.keys():
        rs = ErrLog.query.filter(ErrLog.is_fix == "否").all()
    else:
        rs = ErrLog.query.filter(ErrLog.spider_name.like('%' + request.args['spider_name'] + '%'),
                                 ErrLog.is_fix == "否").all()
    for r in rs:
        items.append(
            dict(id=r.id, spider_name=r.spider_name, err_msg=r.err_msg, err_time=str(r.err_time)))

    usedtime = time.time() - starttime
    data = json.dumps(dict(usedtime=usedtime, items=items))

    rsp = make_response(data)

    rsp.headers['Access-Control-Allow-Origin'] = '*'

    return rsp


# 任务
def task2(id, spider_file_name):
    print('mession' + str(id))
    print(datetime.datetime.now())
    cwd = os.getcwd()
    spider_dir = cwd + "\\IREngine\\spider\\"
    job = scheduler.get_job(id)
    q = Spider.query.filter(Spider.id == int(id)).first()
    output = ""
    try:

        with os.popen("python " + spider_dir + spider_file_name, "r") as p:
            output = p.read()
        print("output_read:\n" + output)
        q.last_run_time = datetime.datetime.now()
        q.next_run_time = job.next_run_time
        if "<acq_num>" in output:
            acq_num = int(output[output.find('<acq_num>') + 9:output.find('</acq_num>')])
            q.last_acq_num = acq_num
            q.acq_num = q.acq_num + acq_num
        pattern = re.compile(r'<error>.*</error>')
        error_list = pattern.findall(output)
        for error in error_list:
            error_info = error[error.find('<error>') + 7:error.find('</error>')]
            q.is_error = True
            add_err(error_info, q)
    except Exception as e:
        print(e)
        q.is_error = True
        add_err(e, q)

    db.session.commit()


def add_err(e, q):
    new_err = ErrLog()
    new_err.err_msg = str(e)
    new_err.err_time = datetime.datetime.now()
    new_err.spider_name = q.name
    new_err.spider_file = q.file_name
    new_err.spider_id = q.id
    new_err.is_fix = "否"
    db.session.add(new_err)
    db.session.commit()


# 任务停用
@app.route('/pause', methods=['GET'])
def pausetask():  # 暂停
    id = request.args['id']
    # scheduler.pause_job(str(id))
    remove_task(str(id))
    q = Spider.query.filter(Spider.id == int(id)).first()
    q.enabled = False
    q.next_run_time = None
    db.session.commit()
    return "Success!"


# 任务启用
@app.route('/resume', methods=['GET'])
def resumetask():  # 恢复
    id = request.args['id']
    # scheduler.resume_job(str(id))
    q = Spider.query.filter(Spider.id == int(id)).first()
    add_task(str(id), q.type, q.file_name, q.params)
    q.enabled = True
    db.session.commit()
    return "Success!"


# 修复异常接口
@app.route('/fix_bug', methods=['GET'])
def fix_err():
    id = request.args['id']
    # scheduler.resume_job(str(id))
    q = Spider.query.filter(Spider.id == int(id)).first()
    q.is_error = False
    els = ErrLog.query.filter(ErrLog.spider_id == int(id)).all()
    for el in els:
        el.is_fix = "是"

    db.session.commit()
    return "ok"


def remove_task(id):  # 移除
    try:
        scheduler.delete_job(str(id))
    except:
        return False
    return True


def add_task(id, type, file_name, params):
    params = json.loads(params)
    scheduler.add_job(func=task2, id=id, args=(id, file_name), trigger='cron', day_of_week=params['run_day'],
                      hour=params['run_hour'], minute=params['run_min'],
                      second=params['run_sec'], replace_existing=True)
    # trigger='cron' 表示是一个定时任务
    # else:
    #   scheduler.add_job(func=task2, id = id, args=(id,file_name),trigger='interval', seconds=int(params), replace_existing=True)
    # trigger='interval' 表示是一个循环任务，每隔多久执行一次


# 新建爬虫任务
@app.route('/addjob', methods=['GET', 'POST'])
def addtask():
    name = request.form['spider_name']
    desc = request.form['spider_desc']
    run_day = request.form['run_day']
    run_hour = request.form['run_hour']
    run_min = request.form['run_min']
    run_sec = request.form['run_sec']
    url = request.form['spider_url']
    params = json.dumps(dict(run_day=run_day, run_hour=run_hour, run_min=run_min, run_sec=run_sec))
    file = request.files['file_1']
    # 拼年月日时分秒微秒作为文件名称
    ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    # 获取上传文件的扩展名
    ext = file.filename.split(".")[-1]
    filename = ftime + "." + ext
    basedir = os.getcwd()
    upload_path = basedir + "\\IREngine\\spider\\" + filename
    file.save(upload_path)
    spider = Spider()
    spider.name = name
    spider.description = desc
    spider.type = True
    spider.params = params
    spider.last_acq_num = 0
    spider.acq_num = 0
    spider.is_error = False
    spider.enabled = True
    spider.file_name = filename
    spider.url = url
    db.session.add(spider)
    db.session.flush()
    db.session.commit()
    add_task(str(spider.id), spider.type, spider.file_name, spider.params)
    return 'sucess'


@app.route('/editjob', methods=['GET', 'POST'])
def edittask():
    id = request.args['id']
    name = request.form['spider_name']
    desc = request.form['spider_desc']
    run_day = request.form['run_day']
    run_hour = request.form['run_hour']
    run_min = request.form['run_min']
    run_sec = request.form['run_sec']
    params = json.dumps(dict(run_day=run_day, run_hour=run_hour, run_min=run_min, run_sec=run_sec))
    spider = Spider.query.filter(Spider.id == int(id)).first()
    if request.files['file_1'] is not None:
        file = request.files['file_1']
        # 拼年月日时分秒微秒作为文件名称
        ftime = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        # 获取上传文件的扩展名
        ext = file.filename.split(".")[-1]
        filename = ftime + "." + ext
        basedir = os.getcwd()
        upload_path = basedir + "\\IREngine\\spider\\" + filename
        file.save(upload_path)
        spider.file_name = filename
    spider.name = name
    spider.description = desc
    spider.type = True
    spider.params = params
    spider.is_error = False
    spider.enabled = True
    db.session.commit()
    add_task(str(spider.id), spider.type, spider.file_name, spider.params)
    return 'sucess'
