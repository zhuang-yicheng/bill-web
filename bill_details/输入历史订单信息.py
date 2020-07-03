import pandas as pd
import pymysql
from progressbar import progressbar

conn = pymysql.connect(
    host='rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com',
    user='xiaozhuang',
    password='zhuangB123',
    database='life'
)
cur = conn.cursor()

class jC_list(list):
    def __init__(self, name):
        super().__init__()  # 继承父类的方法
        self.name = name

col_list = ['pay_date', 'classification2', 'action', 'price', 'method', 'remark']
for i in col_list:
    name = i + '_list'
    locals()[name] = jC_list(i)

path = 'D:/program/MyBill/bill_details/{}'
file_list = ['202003.txt','202004.txt','202005.txt','202006.txt']

pbar = progressbar.ProgressBar()
for file in pbar(file_list):
    with open(path.format(file), "r", encoding='utf-8') as f:
        for data in f:
            l = []
            if ('支' in data[2:6]) or ('收' in data[2:6]):
                action = '支' if '支' in data[2:6] else '收'

                data = data.split(action,1)
                action = '支出' if action == '支' else '收入'
                classification2, data = data[0], data[1]

                for method in ['支付宝','微信钱包','银行卡','现金']:
                    data_temp = data.split(method)
                    if len(data_temp) == 1:
                        continue
                    price = int(data_temp[0].replace(',','').replace('.','').replace('入收',''))

                    if data_temp[1] == '\n':
                        remark = 'NULL'
                        member_id = 1
                        sql = '''
                            INSERT INTO bill (member_id, pay_date, classification2, action, price, method, remark) VALUES
                            ({},"{}","{}","{}",{},"{}",{});
                        '''.format(member_id, pay_date, classification2, action, price, method, remark)
                    else:
                        remark = data_temp[1].replace('\n','')
                        member_id = 2
                        sql = '''
                            INSERT INTO bill (member_id, pay_date, classification2, action, price, method, remark) VALUES
                            ({}, "{}","{}","{}",{},"{}","{}");
                        '''.format(member_id, pay_date, classification2, action, price, method, remark)
                    #print(pay_date, classification2, action, price, method, remark)
                    #print(sql)
                    cur.execute(sql)
                    conn.commit()
                    break
            if data[2] == '/':
                pay_date = f'{data[6:10]}-{data[3:5]}-{data[0:2]}'
                continue
            for i in col_list:
                eval(i+'_list').append(eval(i))

conn.close()            

data = {}
for i in col_list:
    data[i] = eval(i+'_list')
df = pd.DataFrame(data)