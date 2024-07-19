import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json
from datetime import datetime, timedelta
from .us_finance_xq_getter import headers



class us_finance_xq_sector_getter:

  def get_data_1(self, url, params):


    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = [('page', page)] + params
        print(f"page {page}")
        response = get_common_json(url, param_temp, headers)

        data = jsonpath(response, '$..list[:]')
        if not data:
          break
        page += 1
        df = pd.DataFrame(data)
        dfs.append(df)

    if(len(dfs) > 0):

      df = pd.concat(dfs, ignore_index=True)

      df = df.replace('--', 0)
      df = df.replace('_', 0)
      df = df.replace('None', 0)
      df = df.fillna(0)

      return df
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_all_us_equity(self, encode = None):

    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'

# page: 1
# size: 90
# order: desc
# order_by: percent
# market: US
# type: us

    params = [ 
            ('size', 90),
            ('order', 'desc'),
            ('order_by', 'percent'),
            ('market', 'US')
    ]

    if encode != None:
      params.append(('ind_code', encode))

    df = self.get_data_1(url, params)
    return df
  
  def get_all_us_star_equity(self, encode = None):

    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'

# page: 1
# size: 30
# order: desc
# order_by: percent
# market: US
# type: us_star

    params = [ 
            ('size', 90),
            ('order', 'desc'),
            ('order_by', 'percent'),
            ('market', 'US'),
            ('type', 'us_star')
    ]

    df = self.get_data_1(url, params)
    return df
  
  def get_all_us_listed_equity(self, encode = None):

    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'

# page: 1
# size: 90
# order: desc
# order_by: list_date
# market: US
# type: listed

    params = [ 
            ('size', 90),
            ('order', 'desc'),
            ('order_by', 'list_date'),
            ('market', 'US'),
            ('type', 'listed')
    ]

    df = self.get_data_1(url, params)
    return df
  
  def get_all_us_us_china_equity(self, encode = None):

    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'

# page: 1
# size: 30
# order: desc
# order_by: percent
# market: US
# type: us_china

    params = [ 
            ('size', 90),
            ('order', 'desc'),
            ('order_by', 'percent'),
            ('market', 'US'),
            ('type', 'us_china')
    ]

    df = self.get_data_1(url, params)
    return df

  def get_all_us_sector_name(self):
    url = 'https://stock.xueqiu.com/v5/stock/screener/industries.json'

    params = [ 
            ('category', 'us')
    ]
    response = get_common_json(url, params, headers)

    industries = jsonpath(response, '$..industries[:]')

    df_industries = pd.DataFrame(industries)

    return df_industries