import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter = ef.stock.us_equity_getter()
# 
sym = datacenter.get_secucode("AAPL")
# sym = datacenter.get_secucode("CI")
# sym = datacenter.get_secucode("JPM")
# sym = datacenter.get_secucode("JPM")
# sym = datacenter.get_secucode("NVDA")

data = datacenter.get_us_equity_info(symbol = sym)
print(data)
