import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_longport = ef.stock.us_equity_longport_getter()
# 
# sym = datacenter.get_secucode("AAPL")
# sym = datacenter.get_secucode("CI")
# sym = datacenter.get_secucode("JPM")
# sym = datacenter.get_secucode("MSFT")
# sym = datacenter.get_secucode("MMM")
sym = "MSFT"
data = datacenter_longport.get_us_equity_block_info(symbol = sym)
# data = datacenter_xq.get_us_finance_cash(symbol = sym)
print(data)

