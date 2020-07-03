from flask import Flask, escape, render_template, request, redirect, url_for
from .db import get_db, get_conn
import pandas as pd

def create_app():
    app = Flask(__name__)

    #app.config.from_mapping(test_config)

    @app.route('/')
    def hello():
        return render_template('HelloWorld.html')

    # 注册
    @app.route('/registered', methods=['GET'])
    def registered():
        if request.method == 'GET':
            try:
                sql = 'INSERT INTO `account` (`account`, `password`) VALUES ("{}", "{}")'.format(
                    request.args['account'],
                    request.args['password']
                )
            except Exception as e:
                print(e)
                return "未能正确获取账号密码，请重试"
            try:
                conn, cur = get_db()
            except Exception as e:
                print(e)
                return "数据库连接失败，请检查网络情况并重试"
            try:
                cur.execute(sql)
                conn.commit()
                return "注册成功"
                #return redirect(url_for('/'))
            except:
                print(e)
                return "注册失败"
            finally:
                conn.close()

    @app.route('/getdata', methods=['GET'])
    def get_data():
        if request.method == 'GET':
            sql = 'SELECT * FROM bill WHERE pay_date = "{}"'.format(request.args['date'])
            conn = get_conn()
            df = pd.read_sql(sql, conn)
            conn.close()
            return df.to_json()
    # 填写账单信息
    #@app.route('/fillin_bill', methods=['POST'])
    #def fiillin_bill():
    #    if request.method == 'POST':
    #        try:
    #            sql = '''INSERT INTO bill (member_id, action, price, classification1, classification2, pay_date, method, remark) VALUES
    #                    ({}, {}, {}, {}, {}, {}, {}, {})'''.format(
    #                        member_id, action, price, classification1, classification2, pay_date, method, remark
    #                    )
    #        except:
    #            return "未能正确获取账单信息，请重试"
    #        try:
    #            conn = get_conn()
    #        except:
    #            return "数据库连接失败，请检查网络情况并重试"
    #        try:
    #            pd.read_sql(sql, conn)
    #            return {"res": "账单信息写入成功"}
    #        except:
    #            return "未能正确填写账单信息，请重试"
    #        finally:
    #            conn.close()

    return app