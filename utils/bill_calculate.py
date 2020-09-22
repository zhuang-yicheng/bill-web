import pandas as pd
from sqlalchemy import create_engine
from utils.db import get_conn
from CONFIG import *

def getIndex(name):
    colDict = alipayColDict
    return colDict[name]['col']

def getAlipayOriginData(path):
    df = pd.read_csv(path, encoding='gbk', header=4).iloc[:-7, :-1]
    df.columns = list(map(lambda x: x.strip(), df.columns.tolist()))
    df.columns = list(map(lambda x: getIndex(x), df.columns))

    for col in df.columns.tolist():
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(lambda x: x.strip())

    df = df.sort_values(by=['created_time']).reset_index(drop=True)
    return df

def writeAllOriginData(df, table_name, if_exists='append'):
    engine = create_engine(
        'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(USER, PASSWORD, HOST, DATABASE)
    )
    df.to_sql(name=table_name, con=engine, if_exists=if_exists, index=False)

def writePartOriginData(df, table_name):
    delete_list = []
    insert_list = []
    conn, cur = get_conn(cursor=True)
    new_transaction_number = df['transaction_number'].unique().tolist().__str__()[1:-1]

    sql = 'select `transaction_number` from {} where `transaction_number` in {}'.format(
        table_name, '(' + new_transaction_number + ')'
    )
    df_existed = pd.read_sql(sql, conn)
    # 在之前数据中，已存在的交易号，标记为yes
    df_existed['existed'] = 'yes'
    df = df.merge(
        df_existed, on = 'transaction_number', how = 'left'
    )
    # 在之前数据中，不存在的交易号，标记为no
    df.loc[df['existed'].isna(), 'existed'] = 'no'


    for i, row in df[df['existed']=='no'].iterrows():
        data_list = row.tolist()

        sql = 'select `transaction_number` from `{}` where `transaction_number` = "{}";'.format(
            table_name, data_list[0]
        )下·
        cur.execute(sql)
        res = cur.fetchone()
        # print(res)
        if res != None:
            delete_list.append(res[0])

        insert_element = eval('(' + str(data_list)[1:-1] + ')')
        insert_list.append(insert_element)

    delete_sql = 'DELETE FROM `{}` WHERE `transaction_number` IN ({});'.format(
        table_name, str(delete_list)[1:-1]
    )
    cur.execute(delete_sql)

    insert_sql = '''
        INSERT INTO `{}`  (`transaction_number`,`merchant_order_number`,`created_time`,`pay_time`,`updated_time`,
            `origin`,`type`,`counter_party`,`commodity`,`amount`,`in_exp`,`status`,`service_charge`,`refund`,`remark`,`fund_status`
        )
        VALUES {};
    '''.format(table_name, str(insert_list)[1:-1])
    cur.execute(insert_sql)
    conn.close()