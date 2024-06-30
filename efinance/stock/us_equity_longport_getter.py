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


# :authority:
# api.lbkrs.com
# :method:
# GET
# :path:
# /v2/newmarket/global/industry_chart?market=US&index_key=ETF%2FUS%2FSPY&limit=20
# :scheme:
# https
# Accept:
# */*
# Accept-Encoding:
# gzip, deflate, br, zstd
# Accept-Language:
# en
# Cache-Control:
# no-cache
# Origin:
# https://longportapp.com
# Priority:
# u=1, i
# Referer:
# https://longportapp.com/
# Sec-Ch-Ua:
# "Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"
# Sec-Ch-Ua-Mobile:
# ?0
# Sec-Ch-Ua-Platform:
# "Windows"
# Sec-Fetch-Dest:
# empty
# Sec-Fetch-Mode:
# cors
# Sec-Fetch-Site:
# cross-site
# Uber-Trace-Id:
# 17dd649d362d9ec0:17dd649d362d9ec0:0:1
# User-Agent:
# Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
# X-Api-Key:
# 3be769e834553721c5c8fbc9dcfa8dc3
# X-Api-Signature:
# mPefya6HoUR5oKJBA7gS29h6hvqL+7OkTolt3hrrukg=
# X-Application-Build:
# 652b85af
# X-Application-Version:
# 1.0.0
# X-Bundle-Id:
# global.longbridge.web
# X-Device-Id:
# 90e44d9b0049a878e273e5228ca6bbbc
# X-Engine-Version:
# v0.10.2-alpha.2
# X-Platform:
# web
# X-Request-Id:
# a7f90b705124b5d0ed9dd26ba0928022
# X-Timestamp:
# 1719641259107.000

class us_equity_longport_getter:

  def get_datetime_ms(self):
    """Gets the current date and time in milliseconds.

    Returns:
        int: The current date and time in milliseconds since the epoch.
    """
    now = datetime.now()
    epoch = datetime(year=1970, month=1, day=1)  # Epoch reference
    time_delta = now - epoch
    return int(time_delta.total_seconds() * 1000)

  def get_data(self, url, params):


    #           # '': '',
    # headers = {
    #             # ':authority': 'api.lbkrs.com',
    #             # ':method': 'GET',
    #             # ':scheme': 'https',
    #             # 'Accept':'*/*',
    #             # 'Accept-Encoding':'gzip, deflate, br, zstd',
    #             # 'Accept-Language':'Accept-Language',
    #             'Origin': 'https://longportapp.com/',
    #             'Referer': 'https://longportapp.com/',
    #             'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    #             'Sec-Ch-Ua-Mobile': '?0',
    #             'Sec-Ch-Ua-Platform':'"Windows"',
    #             'Sec-Fetch-Dest':'empty',
    #             'Sec-Fetch-Mode':'cors',
    #             'Sec-Fetch-Site':'cross-site',
    #             'Uber-Trace-Id':'17dd66c7ffa620c0:17dd66c7ffa620c0:0:1',
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    #             'X-Timestamp': '1719641259107.000',
    #             'X-Request-Id': 'a7f90b705124b5d0ed9dd26ba0928022',
    #             'X-Platform': 'web',
    #             'X-Engine-Version': 'v0.10.2-alpha.2',
    #             'X-Device-Id': '90e44d9b0049a878e273e5228ca6bbbc',
    #             'X-Bundle-Id': 'global.longbridge.web',
    #             'X-Application-Version': '1.0.0',
    #             'X-Application-Build': '652b85af',
    #             'X-Api-Signature': '3pTpA/ZhOTlG27Yx/6RsXmJZHzYhntjdPwbolcsDVWM=',
    #             'X-Api-Key': '3be769e834553721c5c8fbc9dcfa8dc3',
    #             # 'X-Timestamp': f'{self.get_datetime_ms()}'
    #             }
    
    headers = {
                # ':authority': 'api.lbkrs.com',
                # ':method': 'GET',
                # ':scheme': 'https',
                # 'Accept':'*/*',
                # 'Accept-Encoding':'gzip, deflate, br, zstd',
                # 'Accept-Language':'Accept-Language',
                # 'Origin': 'https://longportapp.com/',
                # 'Referer': 'https://longportapp.com/',
                # 'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
                # 'Sec-Ch-Ua-Mobile': '?0',
                # 'Sec-Ch-Ua-Platform':'"Windows"',
                # 'Sec-Fetch-Dest':'empty',
                # 'Sec-Fetch-Mode':'cors',
                # 'Sec-Fetch-Site':'cross-site',
                "accept-language": "en",
                # 'Uber-Trace-Id':'17dd66c7ffa620c0:17dd66c7ffa620c0:0:1',
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
                # 'X-Timestamp': '1719641259107.000',
                # 'X-Request-Id': 'a7f90b705124b5d0ed9dd26ba0928022',
                # 'X-Platform': 'web',
                # 'X-Engine-Version': 'v0.10.2-alpha.2',
                # 'X-Device-Id': '90e44d9b0049a878e273e5228ca6bbbc',
                # 'X-Bundle-Id': 'global.longbridge.web',
                'X-Application-Version': '1.0.0',
                # 'X-Application-Build': '652b85af',
                # 'X-Api-Signature': '3pTpA/ZhOTlG27Yx/6RsXmJZHzYhntjdPwbolcsDVWM=',
                'X-Api-Key': '3be769e834553721c5c8fbc9dcfa8dc3',
                # 'X-Timestamp': f'{self.get_datetime_ms()}'
                }
  
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

  def get_us_equity_block_info(self, symbol):
# symbol: AAPL
# type: all
# is_detail: true
# count: 50000
# timestamp: 1719231792501
    url = 'https://api.lbkrs.com/v2/newmarket/global/industry_chart'
    params = [
            ('market', 'US'),
            ('index_key', 'ETF/US/SPY'),
            ('limit', '20')
    ]
    df = self.get_data(url, params)
    return df
