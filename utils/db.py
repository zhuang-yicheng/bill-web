from CONFIG import *
import pymysql

def get_conn(cursor=False, autocommit=True):
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        autocommit=autocommit
    )
    if cursor == True:
        cur = conn.cursor()
        return conn, cur
    return conn
