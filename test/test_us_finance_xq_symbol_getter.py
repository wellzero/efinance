import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
from time import sleep


datacenter_xq = ef.stock.us_finance_xq_sector_getter()
# 
data = datacenter_xq.get_all_us_symbol()

print(data.shape)
print(data)

