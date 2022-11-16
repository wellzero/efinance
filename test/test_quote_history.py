import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef
# 股票代码
stock_code = '000001'
df = ef.stock.get_quote_history(stock_code)
print(df)
print(df['日期'].values)
