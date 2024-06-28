import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json
from datetime import datetime, timedelta


# headers = {
# ':authority':
# 'stock.xueqiu.com',
# ':method':
# 'GET',
# ':path':
# '/v5/stock/finance/us/cash_flow.json?symbol=AAPL&type=all&is_detail=true&count=50000',
# ':scheme':
# 'https',
# 'Accept':
# 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# 'Accept-Encoding':
# 'gzip, deflate, br, zstd',
# 'Accept-Language':
# 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
# 'Cache-Control':
# 'max-age=0',
# 'Cookie':
# 'xq_a_token=483932c5fb313ca4c93e7165a31f179fb71e1804',
# 'Priority':
# 'u=0, i',
# 'Sec-Ch-Ua':
# '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
# 'Sec-Ch-Ua-Mobile':
# '?0',
# 'Sec-Ch-Ua-Platform':
# "Windows",
# 'Sec-Fetch-Dest':
# 'document',
# 'Sec-Fetch-Mode':
# 'navigate',
# 'Sec-Fetch-Site':
# 'none',
# 'Sec-Fetch-User':
# '?1',
# 'Upgrade-Insecure-Requests':
# '1',
# 'User-Agent':
# 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
# }



headers = {'Host': 'stock.xueqiu.com',
            'Accept': 'application/json',
            'Cookie': 'xq_a_token=483932c5fb313ca4c93e7165a31f179fb71e1804',
            'User-Agent': 'Xueqiu iPhone 11.8',
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'br, gzip, deflate',
            'Connection': 'keep-alive'}

class us_finance_xq_getter:

  def get_data_daily_data(self, url, params):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    param_temp = params
    response = get_common_json(url, param_temp, headers)

    data = jsonpath(response, '$..item[:]')
    df = pd.DataFrame(data)

    if(len(df) > 0):

      df.columns = response['data']['column']
      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
      return df
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_data_1(self, url, params):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    param_temp = params
    response = get_common_json(url, param_temp, head = headers)

    data = jsonpath(response, '$..list[:]')
    df = pd.DataFrame(data)

    if(len(df) > 0):

      df['report_date'] = pd.to_datetime(df['report_date'], unit='ms')
      return df
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_us_finance_cash(self, symbol):
# symbol: AAPL
# type: all
# is_detail: true
# count: 50000
# timestamp: 1719231792501
    url = 'https://stock.xueqiu.com/v5/stock/finance/us/cash_flow.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df = self.get_data_1(url, params)
    return df
  
  def get_us_finance_balance(self, symbol):
    url = 'https://stock.xueqiu.com/v5/stock/finance/us/balance.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df = self.get_data_1(url, params)
    return df

  def get_us_finance_income(self, symbol):
    url = 'https://stock.xueqiu.com/v5/stock/finance/us/income.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df = self.get_data_1(url, params)
    return df
  
  def get_us_finance_main_factor(self, symbol):
    url = 'https://stock.xueqiu.com/v5/stock/finance/us/indicator.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df = self.get_data_1(url, params)
    return df

  def get_us_finance_daily_trade(self, symbol):
    url = 'https://stock.xueqiu.com/v5/stock/chart/kline.json'
#     symbol: NVDA
# begin: 1719615730587
# period: day
# type: before
# count: -90000
# indicator: kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance
    import datetime

    def get_current_timestamp_ms():
      """Function to get current timestamp in milliseconds using datetime."""
      current_timestamp = datetime.datetime.now()
      # Convert timestamp to epoch time in seconds
      epoch_time = current_timestamp.timestamp()
      # Convert epoch time to milliseconds (multiply by 1000)
      current_time_ms = epoch_time * 1000
      return int(current_time_ms)

    # Call the function and print the result
    timestamp = get_current_timestamp_ms()
    # timestamp = 1719615730587

    params = [
            ('symbol', f'{symbol}'),
            ('begin', f'{timestamp}'),
            ('period', 'day'),
            ('type', 'before'),
            ('indicator', 'kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'),
            ('count', '-1000000')
    ]
    df = self.get_data_daily_data(url, params)
    return df