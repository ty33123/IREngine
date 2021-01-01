# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 11:30:15 2018
Modify on 2020年2月26日10:39:20
@author: Administrator
@e-mail: liuty66@163.com
@introduction:
                进行数据库操作的工具！
"""


import pymysql,time


class db_tools():
    conn = None
    def connect(self):
        # 进行数据库的连接
        #self.conn=pymysql.connect("localhost","root","root","DbName" )
        self.conn=pymysql.connect("127.0.0.1","root","123456","ir_system" )
        print(self.conn)
    
    def query(self,link,table_name):
        cursor = self.conn.cursor()
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("SELECT url from %s where url ='%s'" % (table_name,link))
        # 使用 rowcount() 方法获取数据行数.
        num = cursor.rowcount
        cursor.close()
        return num
       
    def query_id(self,title,table_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id from "+table_name+" where title ='%s'" % title)
        r=cursor.fetchone()
        return r[0]

    def insert(self,item,table_name):
        try:
            """
                item:应包括如下字段
                      字段说明：
            """
            cursor=self.conn.cursor()
            
            #生成sql插入语句
            rowstr=''
            keystr=''
            for key in item.keys():
                rowstr+=("'%s' ,")%(item[key])
                keystr+=('%s,')%(str(key))
            sql=('INSERT INTO %s ('%table_name)+keystr[:-1]+') VALUES (%s)' % (rowstr[:-1])
            #print(sql)
            # 使用 execute()  方法执行 SQL 查询 
            
            cursor.execute(sql)
             
            # 使用 rowcount() 方法获取数据行数.
            num = cursor.rowcount
            
            #进行提交
            self.conn.commit()
            cursor.close()
            
        except BaseException  as e:
            print('except:', e)
            num=0
            
        return num
        
    def close(self):
        self.conn.close()

    


