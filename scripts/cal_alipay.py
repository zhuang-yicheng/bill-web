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
    '交易号': {'col': 'transaction_number', 'index': 0}  # 0
    , '商家订单号': {'col': 'merchant_order_number', 'index': 1}  # 1
    , '交易创建时间': {'col': 'created_time', 'index': 2}  # 2
    , '付款时间': {'col': 'pay_time', 'index': 3}  # 3
    , '最近修改时间': {'col': 'updated_time', 'index': 4}  # 4
    , '交易来源地': {'col': 'origin', 'index': 5}  # 5
    , '类型': {'col': 'type', 'index': 6}  # 6
    , '交易对方': {'col': 'counter_party', 'index': 7}  # 7
    , '商品名称': {'col': 'commodity', 'index': 8}  # 8
    , '金额（元）': {'col': 'amount', 'index': 9}  # 9
    , '收/支': {'col': 'in_exp', 'index': 10}  # 10
    , '交易状态': {'col': 'status', 'index': 11}  # 11
    , '服务费（元）': {'col': 'service_charge', 'index': 12}  # 12
    , '成功退款（元）': {'col': 'refund', 'index': 13}  # 13
    , '备注': {'col': 'remark', 'index': 14}  # 14
    , '资金状态': {'col': 'fund_status', 'index': 15}  # 15
}


def getIndex(name):
    return colDict[name]['index']


def getAlipayOriginData(path):
    df = pd.read_csv(path, encoding='gbk', header=4).iloc[:-7, :-1]
    df.columns = list(map(lambda x: x.strip(), df.columns.tolist()))
    df.columns = list(map(lambda x: colDict[x]['col'], df.columns))

    for col in df.columns.tolist():
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(lambda x: x.strip())

    df = df.sort_values(by=['created_time']).reset_index(drop=True)
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

########################
# 庄
path = 'D:/program/MyBill/bill_details/alipay_record_20200913_1536_1.csv'
df = getAlipayOriginData(path)
writeAllOriginData(df, 'alipay_origin_zhuangyc')

path = 'D:/program/MyBill/bill_details/alipay_record_20200913_1449_1.csv'
df = getAlipayOriginData(path)
writePartOriginData(df, 'alipay_origin_zhuangyc')
#########################
# 龚
path = 'D:/program/MyBill/bill_details/alipay_record_20200909_1307_1.csv'
df = getAlipayOriginData(path)
writeAllOriginData(df, 'alipay_origin_gonghj')
#########################
dfz = pd.read_sql('select * from alipay_origin_zhuangyc', conn)
dfg = pd.read_sql('select * from alipay_origin_gonghj', conn)
#########################
# 找到：小龚小庄之间的转账、红包记录
df_transaction_number = pd.merge(dfz, dfg, on='transaction_number')[['transaction_number']]
df_transaction_number['is_cal'] = '0'
#########################
# 剔除：小龚小庄之间的转账、红包记录
dfz = dfz.merge(df_transaction_number, on='transaction_number', how='left')
# 剔除：支出后又重新退款的记录
refund_list = dfz[dfz['status']=='退款成功']['merchant_order_number'].unique().tolist()
dfz.loc[dfz['merchant_order_number'].isin(refund_list),'is_cal'] = '0'
# 剔除：下的订单，钱还没支出就关闭的交易记录
dfz.loc[(dfz['status']=='交易关闭') & (dfz['in_exp']==''),'is_cal'] = '0'
# 剔除：余额宝、余额之间的转换记录
dfz.loc[(dfz['in_exp']=='') & (dfz['commodity'].isin(['余额宝-自动转入','余额宝-转出到余额'])), 'is_cal'] = '0'
# 剔除：淘宝上没有“支出、收入”的记录
dfz.loc[(dfz['in_exp']=='') & (dfz['origin']=='淘宝'), 'is_cal'] = '0'
dfz.loc[dfz['is_cal'].isna(),'is_cal'] = '1'
dfz.loc[(dfz['in_exp']=='支出') & (dfz['commodity'].str[0:4]=='蚂蚁财富'), 'in_exp']='基金购买'
dfz.loc[(dfz['in_exp']=='支出') & (dfz['commodity'].str[0:4]=='理财买入'), 'in_exp']='理财购买'
dfz.loc[(dfz['in_exp']=='收入') & (dfz['commodity'].str[0:4]=='理财赎回'), 'in_exp']='理财赎回'
dfz = dfz[['created_time','origin','counter_party','commodity','amount','in_exp','is_cal']]

engine = create_engine('mysql+pymysql://xiaozhuang:zhuangB123@rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com/life?charset=utf8')
dfz.to_sql(name='alipay_zhuangyc', con=engine, if_exists='append', index=False)
##########################
dfg = dfg.merge(df_transaction_number, on='transaction_number', how='left')
refund_list = dfg[dfg['status']=='退款成功']['merchant_order_number'].unique().tolist()
dfg.loc[dfg['merchant_order_number'].isin(refund_list),'is_cal'] = '0'
dfg.loc[(dfg['status']=='交易关闭') & (dfg['in_exp']==''),'is_cal'] = '0'
dfg.loc[(dfg['in_exp']=='') & (dfg['commodity'].isin(['余额宝-自动转入','余额宝-转出到余额'])), 'is_cal'] = '0'
dfg.loc[(dfg['in_exp']=='') & (dfg['origin']=='淘宝'), 'is_cal'] = '0'
dfg.loc[dfg['is_cal'].isna(),'is_cal'] = '1'
dfg.loc[(dfg['in_exp']=='支出') & (dfg['commodity'].str[0:4]=='蚂蚁财富'), 'in_exp']='基金购买'
dfg.loc[(dfg['in_exp']=='支出') & (dfg['commodity'].str[0:4]=='理财买入'), 'in_exp']='理财购买'
dfg.loc[(dfg['in_exp']=='收入') & (dfg['commodity'].str[0:4]=='理财赎回'), 'in_exp']='理财赎回'
dfg = dfg[['created_time','origin','counter_party','commodity','amount','in_exp','is_cal']]

engine = create_engine('mysql+pymysql://xiaozhuang:zhuangB123@rm-8vb3bu8i5z7pv11uqqo.mysql.zhangbei.rds.aliyuncs.com/life?charset=utf8')
dfg.to_sql(name='alipay_gonghj', con=engine, if_exists='append', index=False)
##########################
conn.close()