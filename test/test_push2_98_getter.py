import sys
sys.path.append(r'../')
sys.path.append(r'./')
import efinance as ef

push2_98 = ef.stock.push2_98_getter.push2_98()
all_stock_status = push2_98.get_all_stock_status()
print(all_stock_status)

indexs = ['sh', 'sz', 'sh_sz', 'cn']
blocks = ['indurstry', 'concept', 'province']
for block in blocks:
  code_names = push2_98.get_block_codes(block)
  print(code_names)

for index in indexs:
  code_names = push2_98.get_index_codes(index)
  print(code_names)
