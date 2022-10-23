import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


datacenter = ef.stock.datacenter_getter.datacenter()


big_deal = datacenter.get_stock_big_deal()
print(big_deal)

north_stock_index = datacenter.get_north_stock_index()
print(north_stock_index)
north_acc_net = datacenter.get_north_acc_net_buy()
print(north_acc_net)
north_stock_status = datacenter.get_north_stock_status()
print(north_stock_status)
north_stock_daily = datacenter.get_north_stock_daily_trade()
print(north_stock_daily)


margin_short_stock_status = datacenter.get_margin_short_stock_status()
print(margin_short_stock_status)
margin_short_stock = datacenter.get_margin_short_stock()
print(margin_short_stock)