import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead
from datetime import datetime, timedelta



class datacenter:

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
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)


  def get_north_acc_net_buy(self):

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
    return self.get_common_data(url, params, fields)

  def get_north_stock_status(self, date='2022-10-17'):

    mode = 'auto'
    if date is None:
      today = datetime.today().date()
      date = str(today)

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
        "TRADE_DATE":'date',
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
          ('reportName', 'RPT_MUTUAL_STOCK_NORTHSTA'),
          ('sortColumns', 'ADD_MARKET_CAP'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('source', 'WEB'),
          ('client', 'WEB'),
          ('filter',
             f"(TRADE_DATE='{date}')(INTERVAL_TYPE=1)"),
      )

    df = self.get_common_data(url, params, fields)
    if len(df):
      df[fields["TRADE_DATE"]] = df[fields["TRADE_DATE"]].apply(lambda x : x[0:10])
    return df

  def get_north_stock_daily_trade(self, stock_code='600519'):

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
          ('reportName', 'RPT_MUTUAL_HOLDSTOCKNORTH_STA'),
          ('sortColumns', 'TRADE_DATE'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('source', 'WEB'),
          ('client', 'WEB'),
          ('filter',
            f" (SECURITY_CODE={stock_code})(TRADE_DATE>='2022-07-16')"),
      )

    return self.get_common_data(url, params, fields)

  def get_north_stock_index(self, date = '2022-10-17'):

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
        "SECURITY_CODE": "stock_code",
        "BOARD_NAME":  "stock_name",
        "TRADE_DATE":  "date",
        "INDEX_CHANGE_RATIO":  "price_ratio",
        "COMPOSITION_QUANTITY": "composition_num",
        "HK_VALUE":  "hk_market_value",
        "HK_BOARD_RATIO":  "hk_borad_ratio",
        "BOARD_HK_RATIO":  "nort_money_ratio",
        "COMPOSITION_QUANTITY_ADD": "add_composition_quantity",
        "ADD_MARKET_CAP":  "add_market_cap",
        "ADD_RATIO":  "add_market_ratio",
        "ADD_BOARD_RATIO": "add_board_ratio",
        "ADD_HK_RATIO": "add_north_money_ratio"
      }
    params = (
      ("sortColumns", "ADD_MARKET_CAP"),
      ('sortTypes', '-1'),
      ('pageSize', '500'),
      ('reportName', 'RPT_MUTUAL_BOARD_HOLDRANK_WEB'),
      # ('quoteColumns', 'SECURITY_CODE'),
      ('quoteColumns', 'f3\~05\~SECURITY_CODE\~INDEX_CHANGE_RATIO'),
      ('quoteType', '0'),
      ('source', 'WEB'),
      ('client', 'WEB'),
      ('filter',
             f"((BOARD_TYPE=5)(TRADE_DATE='{date}')(INTERVAL_TYPE=1))")
    )

    df = self.get_common_data(url, params, fields)

    if len(df):
      df[fields["TRADE_DATE"]] = df[fields["TRADE_DATE"]].apply(lambda x : x[0:10])
    return df

  def get_margin_short_stock_status(self, date='2022-10-17'):

    mode = 'auto'
    if date is None:
      today = datetime.today().date()
      date = str(today)

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
        "SECUCODE":"stock_code",
        "SECNAME":"stock_name",
        "SPJ":"price_close",
        "ZDF":"price_ratio",
        "RZYE":"RZ余额(元)",
        "RZYEZB":"RZ余额占流通市值比",
        "RZMRE":"RZ买入额(元)",
        "RZCHE":"RZ偿还额(元)",
        "RZJME":"RZ净买入(元)",
        "RQYE":"RQ余额(元",
        "RQYL":"RQ余量(股)",
        "RQMCL":"RQ卖出量(股)",
        "RQCHL":"RQ偿还量(股)",
        "RQJMG":"RQ净卖出(股)",
        "RZRQYE":"RQ融资融券余额(元)",
        "RZRQYECZ":"RQ融资融券余额差值(元)"
      }
    params = (
          ('reportName', 'RPTA_WEB_RZRQ_GGMX'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('sortColumns', 'RZJME'),
          ('source', 'WEB'),
          ('filter',
             f"(date='{date}')"),
      )

    return self.get_common_data(url, params, fields)

  def get_margin_short_stock(self, stock_code='600519'):

    url = 'http://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
        "SECUCODE":"stock_code",
        "SECNAME":"stock_name",
        "DATE": "date",
        "SPJ":"price_close",
        "ZDF":"price_ratio",
        "RZYE":"RZ余额(元)",
        "RZYEZB":"RZ余额占流通市值比",
        "RZMRE":"RZ买入额(元)",
        "RZCHE":"RZ偿还额(元)",
        "RZJME":"RZ净买入(元)",
        "RQYE":"RQ余额(元",
        "RQYL":"RQ余量(股)",
        "RQMCL":"RQ卖出量(股)",
        "RQCHL":"RQ偿还量(股)",
        "RQJMG":"RQ净卖出(股)",
        "RZRQYE":"RQ融资融券余额(元)",
        "RZRQYECZ":"RQ融资融券余额差值(元)"
      }
    params = (
          ('reportName', 'RPTA_WEB_RZRQ_GGMX'),
          ('sortTypes', '-1'),
          ('pageSize', '500'),
          ('sortColumns', 'DATE'),
          ('source', 'WEB'),
          ('filter',
             f"(scode={stock_code})"),
      )
    df = self.get_common_data(url, params, fields)

    df[fields["DATE"]] = df[fields["DATE"]].apply(lambda x : x[0:10])
    return df

  def get_stock_big_deal(self, stock_code='600519'):
    
    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {
      "TRADE_DATE":"date",
      "SECUCODE":"stock_code",
      "SECURITY_NAME_ABBR":"stock_name",
      "CHANGE_RATE": "涨跌幅(0.xx)",
      "CLOSE_PRICE":"收盘价",
      "DEAL_PRICE":"成交价",
      "PREMIUM_RATIO":"折溢率(0.xx)",
      "DEAL_VOLUME":"成交量(股)",
      "DISCOUNT_TURNOVER":"成交额",
      "FREE_SHARES_RATIO":"成交额ratio",
      "CHANGE_RATE_1DAYS":"1日",
      "CHANGE_RATE_5DAYS":"5日",
      "CHANGE_RATE_10DAYS":"10日",
      "CHANGE_RATE_20DAYS":"20日"}
    params = (
          ('reportName', 'RPT_DATA_BLOCKTRADE'),
          ('sortTypes', '-1,-1'),
          ('pageSize', '500'),
          ('sortColumns', 'TRADE_DATE,DEAL_AMT'),
          ('source', 'WEB'),
          ('client', 'WEB'),
          ('filter',
             f"(SECURITY_CODE={stock_code})"),
      )
    df = self.get_common_data(url, params, fields)
    if len(df):
      df[fields["TRADE_DATE"]] = df[fields["TRADE_DATE"]].apply(lambda x : x[0:10])
    return df