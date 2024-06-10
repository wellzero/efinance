import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


datacenter = ef.stock.finance_getter()
sym = datacenter.get_secucode("MMM")
# data = datacenter.get_us_finance_cash(symbol = "AAPL.O")
# data = datacenter.get_us_finance_balance(symbol = "AAPL.O")
# data = datacenter.get_us_finance_income(symbol = "AAPL.O")
# data = datacenter.get_us_finance_income(symbol = "MMM.N")
data = datacenter.get_us_finance_main_factor(symbol = sym)
print(data)
