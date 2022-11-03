import sys
sys.path.append(r'../')
sys.path.append(r'./')

import efinance as ef


north_south = ef.stock.north_south_getter.north_south()

data = north_south.north_south_history('001')
print(data)
data = north_south.north_south_history('002')
print(data)
data = north_south.north_south_history('003')
print(data)
data = north_south.north_south_history('004')
print(data)