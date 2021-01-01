# -*- coding: utf-8 -*-
import pymysql, time
#output = open('error_db.txt','a+',encoding='utf-8')
class db_tools():
    conn = None

    def connect(self):
        # 进行数据库的连接
        # self.conn=pymysql.connect("localhost","root","root","DbName" )
        self.conn = pymysql.connect(host = 'localhost',port = 3306,user = 'root',passwd = '123456',db = 'ir_system',charset = 'utf8')


    def query(self, link, table_name):
        cursor = self.conn.cursor()
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("SELECT url from %s where url ='%s'" % (table_name, link))
        # 使用 rowcount() 方法获取数据行数.
        num = cursor.rowcount
        cursor.close()
        return num

    # def query_id(self, term_name, term_content, table_name):
    #     cursor = self.conn.cursor()
    #     cursor.execute("SELECT id from %s where %s ='%s'" % (table_name, term_name, term_content ))
    #     r = cursor.fetchone()
    #     return r[0]

    def read_all(self, table_name):
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, content from " + table_name)
        content = cursor.fetchall()
        return content

    def read_table(self,table_name):
        cursor=self.conn.cursor()
        cursor.execute("SELECT * from " + table_name)
        content=cursor.fetchall()
        return content

    def read_t_and_id(self, term_name, table_name):
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT %s , id from %s " % (term_name, table_name))
        content = cursor.fetchall()

        return content
        #返回二维矩阵
    def query_elems(self, elem, term_name, term_content, table_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT %s from %s where %s ='%s'" % (elem, table_name, term_name, term_content))
        content = cursor.fetchall()
        return content

    
    def query_res(self, ids):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from news_data WHERE id in %s" % (ids))

        content = cursor.fetchall()
        return content
    #def query_scores(self,elem1,elem2,)
        # try:
        #     cursor = self.conn.cursor()
        #     cursor.execute("SELECT %s from %s where %s ='%s'" % (elem, table_name, term_name, term_content))
        #     content = cursor.fetchall()
        #     return content
        # except BaseException as e:
        #     print("except:"+str(e))
        
        #返回二维矩阵

    def query_elem(self, elem, term_name, term_content, table_name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT %s from %s where %s ='%s'" % (elem, table_name, term_name, term_content ))
        r = cursor.fetchone()
        return r[0]
        
        # try:
        #     cursor = self.conn.cursor()
        #     cursor.execute("SELECT %s from %s where %s ='%s'" % (elem, table_name, term_name, term_content ))
        #     r = cursor.fetchone()
        #     return r[0]
        # except BaseException as e:
        #     print("except:"+str(e))
        

    def read_line(self, table_name, line):
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT content from " + table_name + " where id ='%s'" % str(line))
        content = cursor.fetchone()
        return content[0]

    def count(self,  table_name):
        cursor = self.conn.cursor()
        # 使用 execute()  方法执行 SQL 查询 
        cursor.execute("SELECT count(1) from %s" % (table_name))
        num = cursor.fetchone()
        cursor.close()
        return num[0]
        #return int of count.

    
    def insert(self, item, table_name):
        try:
            """
            id
            url
            content
            source
            collect_time
            publish_time

            """
            cursor = self.conn.cursor()

            # 生成sql插入语句
            rowstr = ''
            keystr = ''
            for key in item.keys():
                rowstr += ("'%s' ,") % (item[key])
                keystr += ('%s,') % (str(key))
            sql = ('INSERT INTO %s (' % table_name) + keystr[:-1] + ') VALUES (%s)' % (rowstr[:-1])
            # print(sql)
            # 使用 execute()  方法执行 SQL 查询 

            cursor.execute(sql)

            # 使用 rowcount() 方法获取数据行数.
            num = cursor.rowcount

            # 进行提交
            self.conn.commit()
            cursor.close()

        except BaseException  as e:
            print('except:'+ str(e))
            num = 0

        return num
    def insert_multi(self, elem_name, elems, table_name):
        try:
            """
            id
            url
            content
            source
            collect_time
            publish_time

            """
            cursor = self.conn.cursor()

            sql = 'INSERT INTO %s %s VALUES %s ' %( table_name, elem_name, elems)
            print(sql)
            cursor.execute(sql)


            # elem_name (elem_name1, elem_name2, ...) elems (elem1, elem2, ...),(elem1, elem2, ...)
            self.conn.commit()
            cursor.close()

        except BaseException  as e:
            print('except:'+ str(e))

    def close(self):
        self.conn.close()
#output.close()