import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from datetime import datetime, timedelta



class datacenter:

  def __init__(self, path):

    self.path = path
    self.url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    if not os.path.exists(path):
      os.makedirs(path)

  def get_common_data(self, url, params, fields):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    page = 1
    columns = ','.join(list(fields.keys()))
    while 1:
        param_temp = (('pageNumber', page), ('columns', columns)) + params
        response = get_common_json_nohead(url, param_temp)
        if bar is None:
            pages = jsonpath(response, '$..pages')

            if pages and pages[0] != 1:
                total = pages[0]
                bar = tqdm(total=int(total))
        if bar is not None:
            bar.update()

        items = jsonpath(response, '$..data[:]')
        if not items:
          break
        page += 1
        df = pd.DataFrame(items).rename(columns=fields)[fields.values()]
        dfs.append(df)

    if(len(dfs) > 0):
     df = pd.concat(dfs, ignore_index=True)
    return df

  def get_north_acc_net_buy(self, filename = 'nort_acc.csv'):

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {"TRADE_DATE": "date","HNETBUY": "sh_north","SNETBUY":"sz_north","NETBUY": "total"}
    columns = ','.join(list(fields.keys()))

#            ('columns', columns),
    params = (
            ('reportName', 'RPT_NORTH_NETBUY'),
            ('filter', f'(DATE_TYPE_CODE="001")'),
            ('pageSize', '500'),
            ('sortTypes', '-1'),
            ('source', 'WEB'),
            ('client', 'WEB'),
            ('sortColumns', 'TRADE_DATE')
    )
    dfs = self.get_common_data(url, params, fields)

    if len(dfs) > 0:
      dfs.to_csv(os.path.join(self.path, filename), encoding='gbk', index=False)



  def get_north_stock_status(self, date='2022-10-17', filename = 'north_stock_status_2022-10-17.csv'):

    mode = 'auto'
    if date is None:
      today = datetime.today().date()
      date = str(today)

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
        "SECUCODE":"stock_code",
        "SECURITY_NAME":"stock_name",
        'CLOSE_PRICE': 'close_price',
        'CHANGE_RATE': 'price_ratio',
        'HOLD_SHARES': 'hold_shares',
        'HOLD_MARKET_CAP': 'hold_market_cap',
        'FREE_SHARES_RATIO': 'free_shares_ratio',
        'TOTAL_SHARES_RATIO': 'total_shares_ratio',
        'ADD_SHARES_REPAIR': 'shares_inc',
        'ADD_MARKET_CAP': 'market_inc',
        'ADD_SHARES_AMP': 'free_shares_inc_ratio',
        'FREECAP_RATIO_CHG': 'free_cap_inc_ratio',
        'TOTAL_RATIO_CHG': 'total_cap_inc_ratio'
      }
    params = (
          ('sortColumns', 'ADD_MARKET_CAP'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('reportName', 'RPT_MUTUAL_STOCK_NORTHSTA'),
          ('source', 'WEB'),
          ('client', 'WEB'),
          ('filter',
             f"(TRADE_DATE='{date}')(INTERVAL_TYPE=1)"),
      )

    dfs = self.get_common_data(url, params, fields)

    if len(dfs) > 0:
      dfs.to_csv(os.path.join(self.path, filename), encoding='gbk', index=False)

  def get_north_stock_daily_trade(self, stock_code='600519', filename = 'north_SH600519.csv'):

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
      "SECUCODE":"stock_code",
      "SECURITY_NAME":"stock_name",
      "TRADE_DATE": "date",
      "CLOSE_PRICE": "close_price",
      "CHANGE_RATE": "price_ratio",
      "HOLD_SHARES": "hold_shares",
      "HOLD_MARKET_CAP": "hold_market_cap",
      "HOLD_SHARES_RATIO": "hold_share_ratio",
      "HOLD_MARKETCAP_CHG1": "1day_cap_change",
      "HOLD_MARKETCAP_CHG5": "5days_cap_change",
      "HOLD_MARKETCAP_CHG10": "10days_cap_change"
      }
    params = (
          ('sortColumns', 'TRADE_DATE'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('reportName', 'RPT_MUTUAL_HOLDSTOCKNORTH_STA'),
          ('source', 'WEB'),
          ('client', 'WEB'),
          ('filter',
            f" (SECURITY_CODE={stock_code})(TRADE_DATE>='2022-07-16')"),
      )

    dfs = self.get_common_data(url, params, fields)

    if len(dfs) > 0:
      dfs.to_csv(os.path.join(self.path, filename), encoding='gbk', index=False)
