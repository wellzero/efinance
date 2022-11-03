from .utils import *

class north_south:

  def north_south_history(self, filter = '001'):

    url = 'https://datacenter-web.eastmoney.com/api/data/v1/get'
    fields = {"TRADE_DATE":"date",
              "NET_DEAL_AMT":"当日成交净买入(亿元)",
              "BUY_AMT":"买入成交额(亿元)",
              "SELL_AMT":"卖出成交额(亿元)",
              "ACCUM_DEAL_AMT":"历史累计净买额(亿元)",
              "FUND_INFLOW":"当日资金流入(亿元)",
              "QUOTA_BALANCE":"当日余额(亿元)",
              "LEAD_STOCKS_NAME":"领涨股",
              "LEAD_STOCKS_CODE": "领涨股代码",
              "LS_CHANGE_RATE":"领涨股涨跌幅",
              "INDEX_CLOSE_PRICE":"上证指数",
              "INDEX_CHANGE_RATE":"涨跌幅"}

    params = (
            ('reportName', 'RPT_MUTUAL_DEAL_HISTORY'),
            ('pageSize', '500'),
            ('sortTypes', '-1'),
            ('source', 'WEB'),
            ('client', 'WEB'),
            ('sortColumns', 'TRADE_DATE'),
            ('filter', f"(MUTUAL_TYPE={filter})")
    )

    df = datacenter_get_data(url, params, fields)
    df.iloc[:, 1:6] = df.iloc[:, 1:6].applymap(lambda x: x/100)

    if len(df):
      df = df.sort_values(by=['date'], ascending=False)
      df['date'] = df['date'].apply(lambda x : x[0:10])
    return df