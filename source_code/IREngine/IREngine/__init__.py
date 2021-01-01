# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from IREngine.tools.jieba_ir import init

scheduler = APScheduler()
app = Flask(__name__)
scheduler.init_app(app=app)
scheduler.start()

# 加载配置文件内容
app.config.from_object('IREngine.setting')  # 模块下的setting文件名，不用加py后缀

# 创建数据库对象
db = SQLAlchemy(app)

from IREngine.model import ErrLog, news_data, Spider
from IREngine.controller import admin, html_page, query, spider_manager

print("jieba init...")
init()
