import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from ..utils import to_numeric
import numpy as np


class push2his:
  def __init__(self, path = '/tmp/finance_data'):
    self.path = path
    if not os.path.exists(path):
      os.makedirs(path)

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

    df = pd.DataFrame(data=np.array(rows).squeeze(), columns=fields2.values())

    return df

  def get_sourth_acc_buy(self, filename = 'stock_status.csv'):
    url = 'https://push2his.eastmoney.com/api/qt/kamt.kline/get'
    fields1 = {
      "f6":"n2s"
    }
    fields2 = {
      "f51":"date",
      "f52":"flow_in(万)",
      "f53":"flow_margin(万)",
      "f54":"acc_flow_in(万)",
    }
    params = (
      ('ut', 'b2884a393a59ad64002292a3e90d46a5'),
      ('klt', '101')
      )
    df = self.get_common(url, params, fields1, fields2, fields1['f6'])

    if len(df) > 0:
      df = df[~df.isin(['-'])].dropna()
      df = df.sort_values(by=['date'], ascending=False)
    else:
      print("download ", filename, "failed, pls check it!")
      df = pd.DataFram()
    
    return df

  # def get_block_daily_trade(self, block_code):
  #   url = 'https://18.push2his.eastmoney.com/api/qt/stock/kline/get'
  #   fields1 = {
  #     "f1":"n2s",
  #     "f2":"n2s",
  #     "f3":"n2s",
  #     "f4":"n2s",
  #     "f5":"n2s",
  #     "f6":"n2s"
  #   }
  #   fields2 = {
  #     "f51":"date",
  #     "f52":"flow_in(万)",
  #     "f53":"flow_margin(万)",
  #     "f54":"acc_flow_in(万)",
  #     "f55":"acc_flow_in(万)",
  #     "f56":"acc_flow_in(万)",
  #     "f57":"acc_flow_in(万)",
  #     "f58":"acc_flow_in(万)",
  #     "f59":"acc_flow_in(万)",
  #     "f60":"acc_flow_in(万)",
  #     "f61":"acc_flow_in(万)",
  #   }
  #   params = (
  #     ('ut', 'b2884a393a59ad64002292a3e90d46a5'),
  #     ('klt', '101')
  #     )
  #   df = self.get_common(url, params, fields1, fields2, fields1['f6'])

  #   if len(df) > 0:
  #     df = df[~df.isin(['-'])].dropna()
  #     df = df.sort_values(by=['date'], ascending=False)
  #   else:
  #     print("download ", filename, "failed, pls check it!")
  #     df = pd.DataFram()
    
  #   return df