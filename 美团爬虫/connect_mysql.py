
import pymysql

#连接MYSQL数据库
config = {
          'host':'localhost',
          'port':3306,
          'user':'root',
          'password':'wq981019',
          'database':'data',
          'charset':'utf8mb4',
        }
db = pymysql.connect(**config)
cursor = db.cursor()

#在数据库建表
def creat_table():
    cursor.execute("DROP TABLE IF EXISTS meituan")
    sql = '''CREATE TABLE meituan(
            评论店铺  varchar(100),
            评论用户姓名 varchar(100),
            评论用户id varchar(100),
            评论用户星级 varchar(55),
            评论用户菜品 varchar(100),
            评论用户内容 text(5000),
            评论时间 varchar(55)
            );'''
    cursor.execute(sql)
    return

#存储爬取到的数据
def save_data(data_dict):
    sql = '''INSERT INTO meituan(评论店铺, 评论用户姓名, 评论用户id, 评论用户星级, 评论用户菜品, 评论用户内容, 评论时间) VALUES(%s,%s,%s,%s,%s,%s,%s)'''
    value_tup = (data_dict['评论店铺']
                 ,data_dict['评论用户姓名']
                 ,data_dict['评论用户id']
                 ,data_dict['评论用户星级']
                 ,data_dict['评论用户菜品']
                 ,data_dict['评论用户内容']
                 ,data_dict['评论时间']
                )
    try:
        cursor.execute(sql, value_tup)
        db.commit()
    except:
        print('数据库写入失败')
    return

#关闭数据库
def close_sql():
    db.close()