# -*- coding: utf-8 -*-
"""
Created on 2020年2月7日14:12:57

@author: Administrator
@e-mail: liuty66@163.com
@introduction:
            使用xpaw框架测试。
            获取评审结果
"""

import json
import random
from xpaw import Spider, HttpRequest, Selector, run_spider
import re

class TestSpider(Spider):
    ip = ""
    headers = {'Host': 'xwb.hebtu.edu.cn',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'
               }
    def start_requests(self):

        yield HttpRequest('http://www.baidu.com', headers = self.headers, callback=self.login)


    def login(self, response):
        try:
            self.headers['Cookie'] = response.headers['Set-Cookie'].split(";")[0]
            print(self.headers)
        except Exception as e:
            print("<error>" + str(e) + "</error>")


    def parse_html(self, response):
        pass
        # try:
        #     html = response.text
        #     print(html)
        #     res = re.findall("论文外审结果.*?</td>",html)
        #     if "待专家评审" not in res[0]:
        #         print("出结果了。。。")
        #     else:
        #         print("还没结果")
        #     # raise Exception("test")
        # except Exception as e:
        #     print("<error>" + str(e) + "</error>")

    def close(self):
        print("<acq_num>" + str(int(random.random()*100)) + "</acq_num>")


if __name__ == '__main__':
    run_spider(TestSpider, log_level='INFO')

