import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_xq = ef.stock.us_finance_xq_sector_getter()
# 
# get sector name encode
data = datacenter_xq.get_all_us_sector_name()
# get all the equity
data = datacenter_xq.get_all_us_equity()
# get one sector equity
data = datacenter_xq.get_all_us_equity(101010)
print(data)

