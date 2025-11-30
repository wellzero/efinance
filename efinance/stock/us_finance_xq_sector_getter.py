import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json , get_cookies
from datetime import datetime, timedelta
from typing import List, Dict


class us_finance_xq_sector_getter:

  def __init__(self, market = 'us') -> None:
    self.market = market
    self.headers = {'Host': 'stock.xueqiu.com',
            'Accept': 'application/json',
            # 'Cookie': 'xq_a_token=483932c5fb313ca4c93e7165a31f179fb71e1804',
            #'Cookie': 'cookiesu=531719230521675; u=531719230521675; s=aw11i3jexw; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xqat=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIxMzAzODc3ODI2LCJjaWQiOiJkOWQwbjRBWnVwIn0.W1EszHcxZpR0MCqxRnEe2QYODoSUnHpuHOcrXtUPU-J3QEQPGntLAJieDZhp0mqZItfz9vgITM69xY75tII3XIso5UVdgyUKX3hc8AcMB9u6tjT-4X1MRHDTuB5545BskeAesimngXtOw53gSnDSZEaup6qE8jBflLhIXE4abemcDu6ISZ2acynDOlMWqnRZy8HhOyFl090Zu2wMZT7sFE9X0vSB7uba1ZHc8-SusZzb8iFWxR4So9d4rxmWyGBM8_V0pmvrpNZlfJvNYIzMtA7O0pxIpFzw_MZFKeHIO4mO6XGMHIXDlCyktUf2WIZ-jf8nSrj-QGFoMbaPktj8pw',
            # 'Cookie': 'cookiesu=531719230521675; s=aw11i3jexw; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; remember=1; xq_a_token=36bfacac6733f24e0f13ee61ae1ae23e15f69dfb; xqat=36bfacac6733f24e0f13ee61ae1ae23e15f69dfb; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMDgyMzU2MjUsImlzcyI6InVjIiwiZXhwIjoxNzIzOTkwNTcyLCJjdG0iOjE3MjEzOTg1NzI4NjAsImNpZCI6ImQ5ZDBuNEFadXAifQ.DI4I0CJ6smktf8vHkAlGHO1ob_RRAdSqhKi_NVb6OdQPmWVEMa9SVeRciDVW1mk_jR4CTJqH52EoM-ATSx7MCGClu3ETzcrY8uhsCoRaqIBN7uvU6JglkSDb_OmyxQoOjuZtUGB7XhLTe4kaIBCz0R8eJ3q-C61F09D8Em2RUKdFur-UwoQlEGTQIvP53Du4YxaOFz9Z8SOTjJe7euJ6fw01D_78gWIURCDl2M8Mo6Kgmg7_2P7zaLThEIBm__9HTudohFhejdb6hiJ00MjIz1iWV903xUFwxq7ENsSjTpj51a_EXM3i6CHbnR7UOQ8GPaWWxiBHeD2dIWyGRFaRMQ; xq_r_token=2d2587f07afff72365fe1734213973fa972add19; xq_is_login=1; u=2108235625; bid=64962f574c50e4102beda34ebbf3b7fa_lyssda5l',
            # 'Cookie': "cookiesu=531719230521675; s=aw11i3jexw; smidV2=20240624200205d213f6a0e7652dfa4334aa89f64719fa008f269a3b4714a60; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; remember=1; xq_is_login=1; u=2108235625; bid=64962f574c50e4102beda34ebbf3b7fa_lyssda5l; xq_a_token=e4692eaf9e6ce577d7266ec07a1cc839ed893132; xqat=e4692eaf9e6ce577d7266ec07a1cc839ed893132; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMDgyMzU2MjUsImlzcyI6InVjIiwiZXhwIjoxNzI1NTMyMTk0LCJjdG0iOjE3MjI5NDAxOTQxODYsImNpZCI6ImQ5ZDBuNEFadXAifQ.Of0zM9HlXrNqqB2Jcu4w6ZGmWxSP3zl4hndXzNChsINUa3RoPL4uLOtp5vc14Cd-ueegKZlW9LYcBQm_EDnfrp0EBXBFn0AAPzmms9v2zmo9cpjHidB6cqmnOK9408dTtNOSee8jZyu9AuFuknKytHrhWihRWIEqMO29Qdrp0qbnvqN11xSojPQfYky6kiv76eFC66KqfOe79SsPFNKHztHQL_H_zwdc2fjibDPTCjPchLJVohtlSEiwnhzhZ0G3rFWLLSTEtC2MYlL6ASxrSLT5cAsN-0UzVl_XS1Fc4jw0Rgs3TCQVzD4FBzB41qUjVIEPZk5ydfQP_t7TbtLf0w; xq_r_token=20eabc7bc990b46a874d842efc2e799360e9e4e7; acw_tc=276077b617229457595536837e4e95562520474140ab829df822c99dc8acba; is_overseas=0; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=QPwunCEEpTOFJYEDJ0cCF7NFNp5bamQ8R36FnaGfyS12pk5t1EsfyfCdJLqvpKgOIPe41AS6rvwgUI486fqgOA%3D%3D; ssxmod_itna=euGQBKejxfr5GHPGdD7IPBYaDgDAhgGELj447IjxD/K7GD3q0=GFDf473ASNDCtaAbxKa70GarWbCW2cvNtoB2P+Fc304LKYDU4i8uWx25eDxx0oD5xGoDPxDeDADYEODAdKD9D04CMgEvCDYPDEDy=DGeDexv8DY5DhxDCDG9HDQKDuxv44=HPDGHPmFx3UOFP5UBHNKqIyhR+eD5D9EoDs2DUaDymgUkP/6AjeWYdfx0koq0OSPusuGgeuxBzP325jW05ieWOY=D3qBqYIfiy5e+ra70oolx3Q7PQrC+ZDDcBzLhDD; ssxmod_itna2=euGQBKejxfr5GHPGdD7IPBYaDgDAhgGELj447I4G9FqO7DBw0D7pqnfSHOGF3ixDv8Si=Y9XGS3+4gGNdLhfONkap/oI+8qmf7Kw8hPtqa6tbkFA9cx3tQTHX6A/UUyvn2RyuQ3Bl6KWM29xbaiQy=nW27FNKIqhaae+tUp41QT=LripkUK3O1P47he1W+W7PnprY=WxwoSLgPONf43CB6omz4nhofufbarQQjKjV/WzPig3DQK2DjKD+ahDD===",
            'Cookie': get_cookies(),
            'User-Agent': 'Xueqiu iPhone 11.8',
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive'}
    return

  def get_data_1(self, url, params):


    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = [('page', page)] + params
        print(f"page {page}")
        response = get_common_json(url, param_temp, self.headers)

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
  def get_data_2(self, url, params):


    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = [('page', page)] + params
        print(f"page {page}")
        response = get_common_json(url, param_temp, self.headers)

        data = jsonpath(response, '$..items[:]')
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
            ('market', self.market.upper())
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

    url = 'https://stock.xueqiu.com/v5/stock/preipo/us/list.json'
    # https://stock.xueqiu.com/v5/stock/preipo/us/list.json?page=1&size=30&order=desc&order_by=list_date&market=US&type=listed

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

    df = self.get_data_2(url, params)
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
            ('category', self.market)
    ]
    response = get_common_json(url, params, self.headers)

    industries = jsonpath(response, '$..industries[:]')

    df_industries = pd.DataFrame(industries)

    return df_industries

  def get_all_us_symbol(self):
    url = 'https://stock.xueqiu.com/v5/stock/screener/quote/list.json'

    if self.market == 'us':
      type = 'us'
    elif self.market == 'cn':
      type = 'sh_sz'
    elif self.market == 'hk':
      type = 'hk'
    else:
        raise ValueError(f"Unsupported market: {self.market}")

    params = [ 
            ('size', 90),
            ('order', 'desc'),
            ('order_by', 'market_capital'),
            ('type', type),
            ('market', self.market.upper())
    ]

    df = self.get_data_1(url, params)
    return df