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

def get_cookies():
  print("getting cookies....")
  from selenium import webdriver
  from selenium.webdriver.chrome.service import Service
  from selenium.webdriver.chrome.options import Options
  from webdriver_manager.chrome import ChromeDriverManager

  import os
  os.environ.pop('HTTP_PROXY', None)
  os.environ.pop('HTTPS_PROXY', None)
  os.environ.pop('http_proxy', None)
  os.environ.pop('https_proxy', None)

   
  # Set up the Chrome driver
  options = Options()
  options.add_argument('--headless')
  options.add_argument('--no-sandbox')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument("--disable-gpu")

  # Set binary location to Chrome executable
  options.binary_location = '/opt/google/chrome/chrome'  # Adjust if the file is named differently (e.g., google-chrome)

  print("Setting up Chrome driver...")
  try:
      # Use specific chromedriver path
      service = Service('/opt/chromedriver/chromedriver')
      driver = webdriver.Chrome(service=service, options=options)
      print("Chrome driver setup successful.")
  except Exception as e:
      print(f"Error setting up driver: {e}")
      exit()
      
  # Navigate to the website
  print("Navigating to xueqiu.com...")
  driver.get("https://xueqiu.com/")

  # Print the page title
  print(driver.title)

  # Get the page source
  page_source = driver.page_source

  # Get cookies
  print("Getting cookies...")
  cookies = driver.get_cookies()
  print("Cookies:", cookies)
  cookie_str = str()
  for cookie in cookies:
      cookie_str += cookie['name']
      cookie_str +='='
      cookie_str += cookie['value']
      cookie_str +='; '
      print(cookie)

  # Close the browser
  driver.close()
  print(cookie_str)
  return cookie_str

headers = {'Host': 'stock.xueqiu.com',
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

class us_finance_xq_getter:

  def __init__(self, market = "us") -> None:
    self.market = market
    return

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
    print("Downloading url", url, "params", param_temp)
    response = get_common_json(url, param_temp, head = headers)

    data = jsonpath(response, '$..list[:]')
    df = pd.DataFrame(data)

    if(len(df) > 0):
      if 'report_date' not in df.columns:
        return df, response
      else:
        df['report_date'] = pd.to_datetime(df['report_date'], unit='ms')
        return df, response
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame(), response

  def xq_get_cash(self, symbol):
# symbol: AAPL
# type: all
# is_detail: true
# count: 50000
# timestamp: 1719231792501
    url = f'https://stock.xueqiu.com/v5/stock/finance/{self.market}/cash_flow.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df, data_json = self.get_data_1(url, params)
    return df, data_json
  
  def xq_get_balance(self, symbol):
    url = f'https://stock.xueqiu.com/v5/stock/finance/{self.market}/balance.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df, data_json = self.get_data_1(url, params)
    return df, data_json

  def xq_get_income(self, symbol):
    url = f'https://stock.xueqiu.com/v5/stock/finance/{self.market}/income.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df, data_json = self.get_data_1(url, params)
    return df, data_json
  
  def xq_get_indicator(self, symbol):
    url = f'https://stock.xueqiu.com/v5/stock/finance/{self.market}/indicator.json'
    params = [
            ('symbol', f'{symbol}'),
            ('type', 'all'),
            ('is_detail', 'true'),
            ('count', '5000')
    ]
    df, data_json = self.get_data_1(url, params)
    return df, data_json

  def xq_get_kline(self, symbol):
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

  def get_cn_fund_list(self, type = 18):
      """
      Fetch fund list data from Xueqiu API.
      
      type: int
      分级基金 11
      货币型 12
      股票型 13
      债券型 14
      混合型 15
      QDII基金 16
      指数型基金 17
      ETF 18
      LOF 19
      FOF 20
      场外基金 21
      
      Returns:
      - DataFrame containing fund list data.
      """
      url = 'https://stock.xueqiu.com/v5/stock/screener/fund/list.json'
      params = [
          ('page', 1),
          ('size', 3000),
          ('order', 'desc'),          # Order by descending
          ('order_by', 'percent'),    # Order by percentage
          ('type', type),             # Type of fund
          ('parent_type', '1')        # Parent type
      ]
      df, data_json = self.get_data_1(url, params)
      return df, data_json

# https://stock.xueqiu.com/v5/stock/chart/kline.json
# symbol SZ980023
# begin 1749823680535
# period day
# type before
# count -284
# indicator kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance