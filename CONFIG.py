# 数据库
HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = 'root'
DATABASE = 'life'

DATA_PATH = 'D:/programe/bill-web/bill_details/'

# 支付宝账单字段列表
alipayColDict = {
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
# 微信账单字段列表
wechatpayColDict = {
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