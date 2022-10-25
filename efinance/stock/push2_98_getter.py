import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from ..utils import to_numeric, add_stock_sh_sz_bj
from datetime import datetime, timedelta
import numpy as np


class push2_98:

  @to_numeric
  def get_common(self, url, params, fields):

    fields_value = ','.join(fields.keys())
    params_temp = (('pz', 5000000), ('fields', fields_value)) + params

    json_response = get_common_json_nohead(url,
                                params=params_temp)
    datas = json_response['data']['diff']
    keys = datas[1].keys()
    rows = []
    [rows.append([list(data.values())]) for data in datas]

    df = pd.DataFrame(data=np.array(rows).squeeze(), columns=keys)

    columns = fields.values()
    df = df.loc[:, fields.keys()]
    df.columns = columns

    return df


  def get_all_stock_status(self, filename = 'stock_status.csv'):
    url = 'http://98.push2.eastmoney.com/api/qt/clist/get'
    fields = {
      "f12":"stock_code",
      "f14":"stock_name",
      "f2":"price_close",
      "f3":"price_ratio",
      "f4":"price_amp",
      "f5":"amount(hand)",
      "f6":"amount(yuan)",
      "f7":"low_high_ratio",
      "f15":"high_price",
      "f16":"low_price",
      "f17":"today_open_price",
      "f18":"yes_close_price",
      "f8":"exchange_ratio",
      "f9":"pe",
      "f23":"pb",
      "f20":"market_price"
    }
    params = (
      ('pn', 1),
      ('po', 1),
      ('np', 1),
      ('ut', 'bd1d9ddb04089700cf9c27f6f7426281'),
      ('fltt', 2),
      ('invt', 2),
      ('wbp2u', '5490045128715900|0|1|0|web'),
      ('fid', 'f20'),
      ('fs', 'm:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048')
      )
    df = self.get_common(url, params, fields)

    if len(df) > 0:
      df.loc[:,'stock_code'] = df.loc[:,'stock_code'].apply(lambda x: add_stock_sh_sz_bj(x))
      df = df[~df.isin(['-'])].dropna()
    else:
      print("download ", filename, "failed, pls check it!")
      df = pd.DataFrame()
    
    return df


  # @to_numeric
  def get_index_codes(self, index: str):
  # index
  # SH index
  #http://8.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+s:2&fields=f12,f14
  #SZ index
  #http://8.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:5&fields=f12,f14
  # index member
  #http://8.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:1+s:3,m:0+t:5&fields=f12,f14
  # china index
  #http://8.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:2&fields=f12,f14
    url = 'http://98.push2.eastmoney.com/api/qt/clist/get'
    fields = { 'f12': 'stock_code', 'f14': 'stock_name'}
    fs_dict = {'sh': 'm:1+s:2', 'sz': 'm:0+t:5', 'sh_sz': 'm:1+s:3,m:0+t:5', 'cn': 'm:2'}
    params = (
      ('fs', fs_dict[index]),
      ('invt', 2),
      ('fltt', 2),
      ('np', 1),
      ('po', 1),
      ('pz', 2000000),
      ('pn', 1)
    )
    df = self.get_common(url, params, fields)
    return df

  # @to_numeric
  def get_block_codes(self, block: str):
  # block
  # province
  #http://98.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:1+f:!50&fields=f12,f14
  #indurstry
  #http://98.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000000&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f12,f14
  #concept 
  #http://98.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000000&po=1&np=1fltt=2&invt=2&fid=f3&fs=m:90+t:3+f:!50&fields=f12,f14
    url = 'http://98.push2.eastmoney.com/api/qt/clist/get'
    fields = { 'f12': 'stock_code', 'f14': 'stock_name'}
    fs_dict = {'province': 'm:90+t:1+f:!50', 'indurstry': 'm:90+t:2+f:!50', 'concept': 'm:90+t:3+f:!50'}
    params = (
      ('fs', fs_dict[block]),
      ('invt', 2),
      ('fltt', 2),
      ('np', 1),
      ('po', 1),
      ('pz', 2000000),
      ('pn', 1)
      )
    df = self.get_common(url, params, fields)
    return df