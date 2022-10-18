import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


datacenter = ef.stock.datacenter_getter.datacenter('/home/quant_data')
datacenter.get_north_acc_net_buy()
datacenter.get_north_stock_status()
datacenter.get_north_stock_daily_trade()


datacenter.get_margin_short_stock_status()
datacenter.get_margin_short_stock()