import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter = ef.stock.us_finance_getter()
# 
# sym = datacenter.get_secucode("AAPL")
# sym = datacenter.get_secucode("CI")
# sym = datacenter.get_secucode("JPM")
sym = datacenter.get_secucode("MSFT")
# sym = datacenter.get_secucode("MMM")
data = datacenter.xq_get_income(symbol = sym)
print(data)
data = datacenter.xq_get_cash(symbol = sym)
print(data)
data = datacenter.xq_get_balance(symbol = sym)
print(data)

data = datacenter.xq_get_indicator(symbol = sym)
print(data)
