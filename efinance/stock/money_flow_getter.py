import os
import time
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from ..utils import to_numeric
import numpy as np

class money_flow:

  @to_numeric
  def get_common(self, url, params, fields1, fields2, get_value = 'n2s'):

    fields1_value = ','.join(fields1.keys())
    fields2_value = ','.join(fields2.keys())
    params_temp = (('lmt', 5000000), ('fields1', fields1_value), ('fields2', fields2_value)) + params

    json_response = get_common_json_nohead(url,
                                params=params_temp)
    datas = json_response['data'][get_value]
    # keys = datas[1].keys()
    # rows = []
    # [rows.append([list(data.values())]) for data in datas]
    rows = [data.split(',') for data in datas]

    df = pd.DataFrame(data=np.array(rows).squeeze(), columns=sorted(fields2.keys()))

    columns = fields2.values()
    df = df.loc[:, fields2.keys()]
    df.columns = columns

    return df

  def get_shsz_big_bill(self, filename = 'stock_status.csv'):
    url = "http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    fields1 = {
      "f1":"-",
      "f2":"-",
      "f3":"-",
      "f7":"-"
    }

    fields2 = {
      "f51": "date",
      "f62": "上证-收盘价",
      "f63": "上证-涨跌幅",
      "f64": "深证-收盘价",
      "f65": "深证-涨跌幅",
      "f52": "主力净流入-净额",
      "f57": "主力净流入-净占比",
      "f56": "超大单净流入-净额",
      "f61": "超大单净流入-净占比",
      "f55": "大单净流入-净额",
      "f60": "大单净流入-净占比",
      "f54": "中单净流入-净额",
      "f59": "中单净流入-净占比",
      "f53": "小单净流入-净额",
      "f58": "小单净流入-净占比"
    }

    params = (
        ("lmt", "0"),
        ("klt", "101"),
        ("secid", "1.000001"),
        ("secid2", "0.399001"),
        ("ut", "b2884a393a59ad64002292a3e90d46a5"),
        ("_", int(time.time() * 1000))
      )
    df = self.get_common(url, params, fields1, fields2, "klines")

    if len(df) > 0:
      df = df[~df.isin(['-'])].dropna()
      df = df.sort_values(by=['date'], ascending=False)
      div_columns = ["主力净流入-净额", "小单净流入-净额", "中单净流入-净额", "大单净流入-净额", "超大单净流入-净额"]
      df.loc[:, div_columns] = df.loc[:, div_columns] / 1E8
    else:
      print("download ", filename, "failed, pls check it!")
      df = pd.DataFram()
    
    return df