import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_xq = ef.stock.us_finance_xq_getter()
# 
# sym = datacenter.get_secucode("AAPL")
# sym = datacenter.get_secucode("CI")
# sym = datacenter.get_secucode("JPM")
# sym = datacenter.get_secucode("MSFT")
# sym = datacenter.get_secucode("MMM")

sym = "SH600519"
sym = "sz980035"
sym = "SH518660"
data = datacenter_xq.xq_get_kline(symbol = sym)
# data = datacenter_xq.xq_get_cash(symbol = sym)
print(data)
data = datacenter_xq.xq_get_income(symbol = sym)
print(data)
data = datacenter_xq.xq_get_balance(symbol = sym)
print(data)

data = datacenter_xq.xq_get_indicator(symbol = sym)
print(data)
