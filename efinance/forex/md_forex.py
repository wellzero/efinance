import requests
import pandas as pd

def md_forex_real_sina(symbols):
    symbols = [s.lower() for s in symbols]
    url = f'http://hq.sinajs.cn/list={",".join([f"fx_s{s}" for s in symbols])}'
    response = requests.get(url)
    # Assuming read_apidata_sina is implemented elsewhere
    dat = read_apidata_sina(url, symbols, ['time', 'buy', 'sell', 'close_prev', 'volatility', 'open', 'high', 'low', 'close', 'name', 'change_pct', 'change', 'amplitude', 'broker', 'v1', 'v2', 'v3', 'date'])
    dat['date'] = pd.to_datetime(dat['date'])
    dat['name'] = dat['name'].str.replace('\u5373\u671f\u6c47\u7387$', '', regex=True)
    return dat[['symbol', 'name', 'date', 'open', 'high', 'low', 'close', 'close_prev', 'change', 'change_pct', 'volatility', 'amplitude', 'time']]

if __name__ == "__main__":
    print(md_forex_real_sina(["AUDUSD", "USDCNY"]))