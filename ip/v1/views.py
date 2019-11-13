from django.shortcuts import render
# Create your views here.
import pymysql.cursors
import pymysql
import pandas as pd

#连接配置信息
config = {
          'host':'127.0.0.1',
          'port':3306,#MySQL默认端口
          'user':'root',#mysql默认用户名
          'password':'1234',
          'db':'house',#数据库
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }

# 创建连接
con= pymysql.connect(**config)
# 执行sql语句
try:
    with con.cursor() as cursor:
        sql="select * from community_view"
        cursor.execute(sql)
        result=cursor.fetchall()
finally:
    con.close();
df=pd.DataFrame(result)#转换成DataFrame格式
df.head()




