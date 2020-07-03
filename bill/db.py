import pymysql

def get_conn():
    conn = pymysql.connect(
        host='rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com',
        user='xiaozhuang',
        password='zhuangB123',
        port=3306,
        database='life'
    )
    return conn

def get_db():
    conn = pymysql.connect(
        host='rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com',
        user='xiaozhuang',
        password='zhuangB123',
        port=3306,
        database='life'
    )
    cur = conn.cursor()
    return conn, cur