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
sym = datacenter.get_secucode("TEAM")
# sym = datacenter.get_secucode("MMM")
data = datacenter.get_us_finance_income(symbol = sym)
print(data)
data = datacenter.get_us_finance_cash(symbol = sym)
print(data)
data = datacenter.get_us_finance_balance(symbol = sym)
print(data)

data = datacenter.get_us_finance_main_factor(symbol = sym)
print(data)
