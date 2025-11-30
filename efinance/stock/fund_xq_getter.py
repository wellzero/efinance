
import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd

from efinance.common.getter import get_driver
from efinance.common import get_common_json , get_cookies
from datetime import datetime, timedelta
from typing import List, Dict

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

headers = {'Host': 'danjuanfunds.com',
            'Accept': 'application/json',
            # 'Cookie': 'xq_a_token=483932c5fb313ca4c93e7165a31f179fb71e1804',
            #'Cookie': 'cookiesu=531719230521675; u=531719230521675; s=aw11i3jexw; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; xq_a_token=64274d77bec17c39d7ef1934b7a3588572463436; xqat=64274d77bec17c39d7ef1934b7a3588572463436; xq_r_token=3f3592acdffbaaee3a7ea110c5d151d2710b7318; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyMjczMjcyOCwiY3RtIjoxNzIxMzAzODc3ODI2LCJjaWQiOiJkOWQwbjRBWnVwIn0.W1EszHcxZpR0MCqxRnEe2QYODoSUnHpuHOcrXtUPU-J3QEQPGntLAJieDZhp0mqZItfz9vgITM69xY75tII3XIso5UVdgyUKX3hc8AcMB9u6tjT-4X1MRHDTuB5545BskeAesimngXtOw53gSnDSZEaup6qE8jBflLhIXE4abemcDu6ISZ2acynDOlMWqnRZy8HhOyFl090Zu2wMZT7sFE9X0vSB7uba1ZHc8-SusZzb8iFWxR4So9d4rxmWyGBM8_V0pmvrpNZlfJvNYIzMtA7O0pxIpFzw_MZFKeHIO4mO6XGMHIXDlCyktUf2WIZ-jf8nSrj-QGFoMbaPktj8pw',
            # 'Cookie': 'cookiesu=531719230521675; s=aw11i3jexw; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; remember=1; xq_a_token=36bfacac6733f24e0f13ee61ae1ae23e15f69dfb; xqat=36bfacac6733f24e0f13ee61ae1ae23e15f69dfb; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMDgyMzU2MjUsImlzcyI6InVjIiwiZXhwIjoxNzIzOTkwNTcyLCJjdG0iOjE3MjEzOTg1NzI4NjAsImNpZCI6ImQ5ZDBuNEFadXAifQ.DI4I0CJ6smktf8vHkAlGHO1ob_RRAdSqhKi_NVb6OdQPmWVEMa9SVeRciDVW1mk_jR4CTJqH52EoM-ATSx7MCGClu3ETzcrY8uhsCoRaqIBN7uvU6JglkSDb_OmyxQoOjuZtUGB7XhLTe4kaIBCz0R8eJ3q-C61F09D8Em2RUKdFur-UwoQlEGTQIvP53Du4YxaOFz9Z8SOTjJe7euJ6fw01D_78gWIURCDl2M8Mo6Kgmg7_2P7zaLThEIBm__9HTudohFhejdb6hiJ00MjIz1iWV903xUFwxq7ENsSjTpj51a_EXM3i6CHbnR7UOQ8GPaWWxiBHeD2dIWyGRFaRMQ; xq_r_token=2d2587f07afff72365fe1734213973fa972add19; xq_is_login=1; u=2108235625; bid=64962f574c50e4102beda34ebbf3b7fa_lyssda5l',
            # 'Cookie': "cookiesu=531719230521675; s=aw11i3jexw; smidV2=20240624200205d213f6a0e7652dfa4334aa89f64719fa008f269a3b4714a60; device_id=af3db6e8ca230ec3802498e50eb0d2c3; Hm_lvt_1db88642e346389874251b5a1eded6e3=1719721306; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1719721310; remember=1; xq_is_login=1; u=2108235625; bid=64962f574c50e4102beda34ebbf3b7fa_lyssda5l; xq_a_token=e4692eaf9e6ce577d7266ec07a1cc839ed893132; xqat=e4692eaf9e6ce577d7266ec07a1cc839ed893132; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOjIxMDgyMzU2MjUsImlzcyI6InVjIiwiZXhwIjoxNzI1NTMyMTk0LCJjdG0iOjE3MjI5NDAxOTQxODYsImNpZCI6ImQ5ZDBuNEFadXAifQ.Of0zM9HlXrNqqB2Jcu4w6ZGmWxSP3zl4hndXzNChsINUa3RoPL4uLOtp5vc14Cd-ueegKZlW9LYcBQm_EDnfrp0EBXBFn0AAPzmms9v2zmo9cpjHidB6cqmnOK9408dTtNOSee8jZyu9AuFuknKytHrhWihRWIEqMO29Qdrp0qbnvqN11xSojPQfYky6kiv76eFC66KqfOe79SsPFNKHztHQL_H_zwdc2fjibDPTCjPchLJVohtlSEiwnhzhZ0G3rFWLLSTEtC2MYlL6ASxrSLT5cAsN-0UzVl_XS1Fc4jw0Rgs3TCQVzD4FBzB41qUjVIEPZk5ydfQP_t7TbtLf0w; xq_r_token=20eabc7bc990b46a874d842efc2e799360e9e4e7; acw_tc=276077b617229457595536837e4e95562520474140ab829df822c99dc8acba; is_overseas=0; .thumbcache_f24b8bbe5a5934237bbc0eda20c1b6e7=QPwunCEEpTOFJYEDJ0cCF7NFNp5bamQ8R36FnaGfyS12pk5t1EsfyfCdJLqvpKgOIPe41AS6rvwgUI486fqgOA%3D%3D; ssxmod_itna=euGQBKejxfr5GHPGdD7IPBYaDgDAhgGELj447IjxD/K7GD3q0=GFDf473ASNDCtaAbxKa70GarWbCW2cvNtoB2P+Fc304LKYDU4i8uWx25eDxx0oD5xGoDPxDeDADYEODAdKD9D04CMgEvCDYPDEDy=DGeDexv8DY5DhxDCDG9HDQKDuxv44=HPDGHPmFx3UOFP5UBHNKqIyhR+eD5D9EoDs2DUaDymgUkP/6AjeWYdfx0koq0OSPusuGgeuxBzP325jW05ieWOY=D3qBqYIfiy5e+ra70oolx3Q7PQrC+ZDDcBzLhDD; ssxmod_itna2=euGQBKejxfr5GHPGdD7IPBYaDgDAhgGELj447I4G9FqO7DBw0D7pqnfSHOGF3ixDv8Si=Y9XGS3+4gGNdLhfONkap/oI+8qmf7Kw8hPtqa6tbkFA9cx3tQTHX6A/UUyvn2RyuQ3Bl6KWM29xbaiQy=nW27FNKIqhaae+tUp41QT=LripkUK3O1P47he1W+W7PnprY=WxwoSLgPONf43CB6omz4nhofufbarQQjKjV/WzPig3DQK2DjKD+ahDD===",
            'Cookie':"xxx",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
            'Accept-Encoding': 'br, gzip, deflate', 
            'Connection': 'keep-alive'}

class fund_xq_getter:

  def __init__(self) -> None:

    self.driver = get_driver()
    self.cookies =  self.get_cookies("https://danjuanfunds.com/")
    # 绕过网站的WebDriver检测
    self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })

    return
  
  def __del__(self):
    """Automatically close the driver when object is destroyed"""
    try:
        if hasattr(self, 'driver'):
            self.driver.quit()
    except:
        pass  # Silently ignore any errors during cleanup
  
  def get_cookies(self, url):
    # Navigate to the website
    driver = self.driver
    print(f"Navigating to {url}...")
    driver.get(url)

    # Print the page title
    print(driver.title)

    print("Getting cookies...")
    cookies = driver.get_cookies()
    # Navigate to the website
    print(f"Navigating to {url}...")
    driver.get(url)

    # Print the page title
    print(driver.title)
    print("Cookies:", cookies)
    cookie_str = str()
    for cookie in cookies:
        cookie_str += cookie['name']
        cookie_str +='='
        cookie_str += cookie['value']
        cookie_str +='; '
        print(cookie)

    print(cookie_str)
    return cookie_str

  def update_cookies_timestamp(self):
    """Update the timestamp in cookies to current time"""
    if not self.cookies:
        return self.cookies
    
    # Parse cookies string into dictionary
    cookies_dict = {}
    for cookie in self.cookies.split(';'):
        cookie = cookie.strip()
        if '=' in cookie:
            key, value = cookie.split('=', 1)
            cookies_dict[key] = value
    
    # Update timestamp with current time in milliseconds
    cookies_dict['timestamp'] = str(int(time.time() * 1000))
    
    # Rebuild cookies string
    updated_cookies = '; '.join([f"{k}={v}" for k, v in cookies_dict.items()])
    return updated_cookies

  def get_data(self, url, params):
    # Update cookies before making request
    updated_cookies = self.update_cookies_timestamp()
    
    # Create headers with updated cookies
    request_headers = headers.copy()
    request_headers['Cookie'] = updated_cookies

    response = get_common_json(url, params, request_headers)

    data = jsonpath(response, '$..items[*]')
    df = pd.DataFrame(data)

    if(len(df) > 0):

      return df, response
    else:
      print("download url", url, "param ", params, "failed, pls check it!")
      return pd.DataFrame(), response
      # exit(-1)

  def xq_get_index_overall(self):
    url = f'https://danjuanfunds.com/djapi/index_eva/dj'
    params = []
    df, data_json = self.get_data(url, params)
    return df, data_json

  def get_ratio_history_data(self, symbol, option = "pe", day="all"):
    # Construct the API URL
    url = f"https://danjuanfunds.com/djapi/index_eva/{option}_history/{symbol}?day={day}"
    
    # Execute JavaScript to fetch the data
    script = f"""
        return fetch('{url}')
            .then(response => response.json())
            .then(data => data)
            .catch(error => console.error('Error:', error));
    """
    
    try:
        # Execute the script and get the JSON data
        result = self.driver.execute_script(script)
        return pd.DataFrame(result['data'][f'index_eva_{option}_growths'])
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
    
  def create_valuation_dataframe(self, symbol, pe_df, roe_df, pb_df):
    """
    Convert PB, PE, and ROE data into a DataFrame with two-level index ['symbol', 'date']
    
    Parameters:
    -----------
    symbol : str
        The symbol name (e.g., "SP500")
    pe_data : dict
        PE ratio data from get_ratio_history_data
    roe_data : dict
        ROE data from get_ratio_history_data
    pb_data : dict
        PB ratio data from get_ratio_history_data
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with multi-index ['symbol', 'date'] and columns ['pe', 'roe', 'pb']
    """
    import pandas as pd
    
    # Rename columns for clarity
    pe_df = pe_df.rename(columns={'ts': 'date', 'pe': 'pe'})
    roe_df = roe_df.rename(columns={'ts': 'date', 'roe': 'roe'})
    pb_df = pb_df.rename(columns={'ts': 'date', 'pb': 'pb'})

    # Convert ROE from decimal to percentage by multiplying by 100
    roe_df['roe'] = roe_df['roe'] * 100

    # Convert timestamp (milliseconds) to date only (YYYY-MM-DD)
    pe_df['date'] = pe_df['date'].apply(lambda ts: datetime.fromtimestamp(ts / 1000.0).date())
    roe_df['date'] = roe_df['date'].apply(lambda ts: datetime.fromtimestamp(ts / 1000.0).date())
    pb_df['date'] = pb_df['date'].apply(lambda ts: datetime.fromtimestamp(ts / 1000.0).date())
    
    
    # Merge all data on date
    merged_df = pd.merge(pe_df, roe_df, on='date', how='outer')
    merged_df = pd.merge(merged_df, pb_df, on='date', how='outer')
    
    # Add symbol column
    merged_df['symbol'] = symbol
    
    # Convert date to datetime and set as index
    merged_df['date'] = pd.to_datetime(merged_df['date'])
    merged_df = merged_df.set_index(['symbol', 'date']).sort_index()
    
    return merged_df
  
  def get_fund_valuation_data(self, symbol: str, day="all"):
    # Get PE, ROE, PB data

    pe_df = self.get_ratio_history_data(symbol, option = "pe", day = day)
    roe_df = self.get_ratio_history_data(symbol, option = "roe", day = day)
    pb_df = self.get_ratio_history_data(symbol, option = "pb", day = day)

    if (len(pe_df) == 0):
       print(f"symbol {symbol} PE records found:  {len(pe_df)}")
    if (len(roe_df) == 0):
       print(f"symbol {symbol} ROE records found:  {len(roe_df)}")
    if (len(pb_df) == 0):
       print(f"symbol {symbol} PB records found:  {len(pb_df)}")
    return self.create_valuation_dataframe(symbol, pe_df, roe_df, pb_df)