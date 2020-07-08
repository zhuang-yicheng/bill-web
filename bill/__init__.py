from flask import Flask, escape, render_template, request, redirect, url_for
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig
from .db import get_db, get_conn
import pandas as pd
import os
import json

# CurrentConfig，有关【基本使用-全局变量】
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./bill/templates/pyecharts"))

from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.faker import Faker

def create_app():
    app = Flask(__name__, static_folder="./bill/templates")

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

    def last_month_pay() -> Line:
        sql = '''
            SELECT
                pay_date,
                SUM(price)/100 price,
                COUNT(id) orders
            FROM bill
            WHERE pay_date > '2020-06-01'
                AND pay_date < '2020-07-01'
                AND action = '支出'
            GROUP BY 1
        '''
        conn = get_conn()
        df = pd.read_sql(sql, conn)
        bar = (
            Bar()
                .add_xaxis(df['pay_date'].tolist())
                .add_yaxis("支出金额", df['price'].tolist())
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(formatter="{value} 单"),
                        #interval=5
                    )
                )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="上月支出"),
                    yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} 元")),
                )
        )
        line = (
            Line()
                .add_xaxis(df['pay_date'].tolist())
                .add_yaxis("支出笔数", df['orders'].tolist(), yaxis_index=1)
        )
        bar.overlap(line)
        return bar

    @app.route('/test')
    def test():
        c = last_month_pay()
        return Markup(c.render_embed())

    @app.route('/lastMonth_pay')
    def lastMonth_pay():
        sql = '''
                    SELECT
                        substr(pay_date,1,10) pay_date,
                        SUM(price)/100 price,
                        COUNT(id) orders
                    FROM bill
                    WHERE pay_date > '2020-06-01'
                        AND pay_date < '2020-07-01'
                        AND action = '支出'
                    GROUP BY 1
                '''
        conn = get_conn()
        df = pd.read_sql(sql, conn)
        data = {}
        data['pay_date'] = df['pay_date'].tolist()
        data['price'] = df['price'].tolist()
        data['orders'] = df['orders'].tolist()
        print(data)
        return render_template('lastMonth_pay.html', result_json = json.dumps(data))

    return app