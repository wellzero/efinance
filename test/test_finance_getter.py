import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


datacenter = ef.stock.finance_getter()
sym = datacenter.get_secucode("AAPL")
data = datacenter.get_us_finance_cash(symbol = sym)
data = datacenter.get_us_finance_balance(symbol = sym)
data = datacenter.get_us_finance_income(symbol = sym)
# data = datacenter.get_us_finance_main_factor(symbol = sym)
print(data)
