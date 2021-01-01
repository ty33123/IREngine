# coding=utf-8

from IREngine import db


class Spider(db.Model):
    __tablename__ = 'spider_list'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))  #爬虫名称
    description = db.Column(db.String(255))  #爬虫描述
    type = db.Column(db.Boolean)  #采集类型 0定时采集 1 循环采集
    params = db.Column(db.String(255))  # 爬虫描述
    last_acq_num = db.Column(db.Integer)  #上次采集数量
    acq_num = db.Column(db.Integer)  # 总采集数量
    is_error = db.Column(db.Boolean)  #采集类型 0无异常 1 异常
    last_run_time = db.Column(db.DateTime)  #上次采集时间
    next_run_time = db.Column(db.DateTime)  #下次采集时间
    enabled = db.Column(db.Boolean)  #是否启用 0未启用 1启用
    file_name = db.Column(db.String(255))  #xpaw爬虫文件名
    url = db.Column(db.String(512))  # 公文列表页url

