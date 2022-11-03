import sys
sys.path.append(r'../')
sys.path.append(r'./')
import efinance as ef

push2his = ef.stock.push2his_getter.push2his()
df = push2his.get_sourth_acc_buy()
print(df)