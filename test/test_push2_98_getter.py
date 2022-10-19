import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


push2_98 = ef.stock.push2_98_getter.push2_98()
all_stock_status = push2_98.get_all_stock_status()
print(all_stock_status)