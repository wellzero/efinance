import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


datacenter = ef.stock.push2_98_getter.push2_98('/home/quant_data')
datacenter.get_all_stock_status()
