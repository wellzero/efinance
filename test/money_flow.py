import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


data_download = ef.stock.money_flow_getter.money_flow()

data = data_download.get_shsz_big_bill()
print(data)