import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
# 股票代码
stock_code = '000001'
print(ef.stock.get_quote_history(stock_code))