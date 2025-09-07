import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_xq = ef.stock.us_finance_xq_getter()
# 

etf, data_json = datacenter_xq.get_cn_fund_list()
print("fund:", etf)

sym = "SH518660"
data = datacenter_xq.xq_get_kline(symbol = sym)
# data = datacenter_xq.xq_get_cash(symbol = sym)
print(data)

