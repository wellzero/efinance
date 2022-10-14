import sys
sys.path.append(r'../')
sys.path.append(r'./')

import index_block


inde_block_data = index_block.get_index_block_data('../../../finance_data/index_block_data/')
inde_block_data.get_data()