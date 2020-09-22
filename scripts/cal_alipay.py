from utils.bill_calculate import getAlipayOriginData, writeAllOriginData
from CONFIG import *

# 庄
path = DATA_PATH + 'alipay_record_20200921_1351_1.csv'
df = getAlipayOriginData(path)
writeAllOriginData(df, 'alipay_origin_zhuangyc')