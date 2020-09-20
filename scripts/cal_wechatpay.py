import pandas as pd
import pymysql
from sqlalchemy import create_engine
from progressbar import progressbar

conn = pymysql.connect(
    host='rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com',
    user='xiaozhuang',
    password='zhuangB123',
    database='life',
    autocommit=True
)
cur = conn.cursor()

colDict = {
    '交易时间': {'col': 'time', 'index': 0}  # 0
    , '交易类型': {'col': 'type', 'index': 1}  # 1
    , '交易对方': {'col': 'counter_party', 'index': 2}  # 2
    , '商品': {'col': 'commodity', 'index': 3}  # 3
    , '收/支': {'col': 'in_exp', 'index': 4}  # 4
    , '金额(元)': {'col': 'amount', 'index': 5}  # 5
    , '支付方式': {'col': 'method', 'index': 6}  # 6
    , '当前状态': {'col': 'status', 'index': 7}  # 7
    , '交易单号': {'col': 'transaction_number', 'index': 8}  # 8
    , '商户单号': {'col': 'merchant_order_number', 'index': 9}  # 9
    , '备注': {'col': 'remark', 'index': 10}  # 10
}

usecols = []
for i in range(len(colDict)):
    usecols.append(i)


class jC_list(list):
    def __init__(self, name):
        super().__init__()  # 继承父类的方法
        self.name = name


def getIndex(name):
    return colDict[name]['index']


def getWeChatpayOriginData(path):
    df = pd.read_csv(path, header=16, usecols=usecols)
    df.columns = list(map(lambda x: x.strip(), df.columns.tolist()))
    df.columns = list(map(lambda x: colDict[x]['col'], df.columns))

    for col in df.columns.tolist():
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(lambda x: x.strip())

    df = df.sort_values(by=['time']).reset_index(drop=True)
    return df


def writeAllOriginData(df, table_name):
    engine = create_engine(
        'mysql+pymysql://xiaozhuang:zhuangB123@rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com/life?charset=utf8')
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


def writePartOriginData(df, table_name):
    delete_list = []
    insert_list = []

    for i, row in df.iterrows():
        data_list = row.tolist()

        sql = 'select `transaction_number` from `{}` where `transaction_number` = "{}";'.format(table_name,
                                                                                                data_list[0])
        cur.execute(sql)
        res = cur.fetchone()
        # print(res)
        if res != None:
            delete_list.append(res[0])

        insert_element = eval('(' + str(data_list)[1:-1] + ')')
        insert_list.append(insert_element)

    delete_sql = 'DELETE FROM `{}` WHERE `transaction_number` IN ({});'.format(table_name, str(delete_list)[1:-1])
    cur.execute(delete_sql)

    insert_sql = '''
        INSERT INTO `{}`  (`transaction_number`,`merchant_order_number`,`created_time`,`pay_time`,`updated_time`,
            `origin`,`type`,`counter_party`,`commodity`,`amount`,`in_exp`,`status`,`service_charge`,`refund`,`remark`,`fund_status`
        )
        VALUES {};
    '''.format(table_name, str(insert_list)[1:-1])
    cur.execute(insert_sql)


######################
path = 'D:/program/MyBill/bill_details/微信支付账单(20200701-20200918).csv'
dfz = getWeChatpayOriginData(path)
path = 'D:/program/MyBill/bill_details/微信支付账单(20200701-20200918)_gong.csv'
dfg = getWeChatpayOriginData(path)
######################
# 找到：小龚小庄之间的转账、红包记录
df_transaction_number1 = pd.merge(dfz, dfg, left_on='transaction_number', right_on='merchant_order_number')[['transaction_number_x']]
df_transaction_number2 = pd.merge(dfz, dfg, left_on='merchant_order_number', right_on='transaction_number')[['transaction_number_y']]
df_transaction_number3 = pd.merge(
    dfz[~dfz['merchant_order_number'].isin(['/',''])],
    dfg[~dfg['merchant_order_number'].isin(['/',''])],
    on='merchant_order_number'
)[['merchant_order_number']]
df_transaction_number1.columns = ['nocal_number']
df_transaction_number2.columns = ['nocal_number']
df_transaction_number3.columns = ['nocal_number']
transfer_record_list = pd.concat([df_transaction_number1,df_transaction_number2,df_transaction_number3])['nocal_number'].unique().tolist()
#######################
# 标记：小龚小庄之间的转账、红包记录
dfg.loc[(dfg['transaction_number'].isin(transfer_record_list)) | (dfg['merchant_order_number'].isin(transfer_record_list)), 'is_cal'] = '0'

# 标记：消费支出退款、红包全额退款、(转账全额退款)
dfg.loc[(dfg['status']=='已全额退款'),'is_cal'] = '0'

# 标记：转账退款（对方拒收）
dfg.loc[(dfg['type']=='转账') & (dfg['status']=='朋友已退还'),'is_cal'] = '0'

# 标记：群红包退款（未被抢完）
dfg.loc[(dfg['type']=='微信红包（群红包）') & (dfg['status'].str.contains('已退款')),'is_cal'] = '0'

# 标记：提现到银行卡？？？
#dfg.loc[(dfg['type']=='零钱提现') & (dfg['status'].str.contains('提现已到账')),'is_cal'] = '0'
########################
dfg['is_cal'] = dfg['is_cal'].fillna('1')
dfg['amount'] = dfg['amount'].apply(lambda x:x[1:])
dfg['name'] = '龚慧珏'
dfg['app'] = '微信'
dfg['origin'] = ''
########################
dfg = dfg[['name','app','time','origin','counter_party','commodity','amount','in_exp','is_cal']]
########################
writeAllOriginData(dfg, 'wechatpay_gonghj')
########################
conn.close()