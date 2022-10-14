import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
# 股票代码

indexs_codes = ef.stock.get_indexs_codes()
print(indexs_codes)
blocks_codes = ef.stock.get_blocks_codes()
print(blocks_codes)