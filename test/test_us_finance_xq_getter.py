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
sym = "MSFT"
data = datacenter_xq.get_us_finance_daily_trade(symbol = sym)
# data = datacenter_xq.get_us_finance_cash(symbol = sym)
print(data)
data = datacenter_xq.get_us_finance_income(symbol = sym)
print(data)
data = datacenter_xq.get_us_finance_balance(symbol = sym)
print(data)

data = datacenter_xq.get_us_finance_main_factor(symbol = sym)
print(data)
