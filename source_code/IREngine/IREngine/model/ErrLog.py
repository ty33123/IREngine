#-*-coding:utf-8-*-
"""
@File        : ErrLog.py
@Time        : 2020/3/17 11:29
@Author      : liuty
@Email       : liuty66@163.com
@introduction:
              ....
"""
from IREngine import db


class ErrLog(db.Model):
    __tablename__ = 'err_log'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    err_msg = db.Column(db.String(255))  #错误信息
    err_time = db.Column(db.DateTime)  #错误时间
    spider_name = db.Column(db.String(255))  # 爬虫名
    spider_file = db.Column(db.String(255))  # 爬虫文件名
    spider_id = db.Column(db.Integer) #爬虫id
    is_fix = db.Column(db.String(3))  # 是否修复