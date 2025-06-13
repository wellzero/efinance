import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_xq = ef.stock.us_finance_xq_getter()
# 

etf = datacenter_xq.get_cn_fund_list()
print(etf)

sym = "SH518660"
data = datacenter_xq.get_us_finance_daily_trade(symbol = sym)
# data = datacenter_xq.get_us_finance_cash(symbol = sym)
print(data)

