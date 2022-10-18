import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from datetime import datetime, timedelta
import numpy as np


class push2_98:
  def __init__(self, path):
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)

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
      "f12":"code",
      "f14":"name",
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
    df = self.get_common(url, params, fields, filename)

    if len(df) > 0:
      df.loc[:,'code'].apply(lambda x: "'" + x)
      df.to_csv(os.path.join(self.path, filename), encoding='gbk', index=False)
    else:
      print("download ", filename, "failed, pls check it!")
      exit(-1)
