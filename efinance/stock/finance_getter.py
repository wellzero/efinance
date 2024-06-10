import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json
from datetime import datetime, timedelta



class finance_getter:


  def get_secucode(self, symbol):

    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'

# reportName: RPT_USF10_INFO_ORGPROFILE
# columns: SECUCODE,SECURITY_CODE,ORG_CODE,SECURITY_INNER_CODE,ORG_NAME,ORG_EN_ABBR,BELONG_INDUSTRY,FOUND_DATE,CHAIRMAN,REG_PLACE,ADDRESS,EMP_NUM,ORG_TEL,ORG_FAX,ORG_EMAIL,ORG_WEB,ORG_PROFILE
# quoteColumns: 
# filter: (SECURITY_CODE="TSLA")
# pageNumber: 1
# pageSize: 200
# sortTypes: 
# sortColumns: 
# source: SECURITIES
# client: PC
# v: 0030591482629004352

    params = [
            ('reportName', 'RPT_USF10_INFO_ORGPROFILE'),
            ('columns',  ('SECUCODE')),
            ('filter', f'(SECURITY_CODE="{symbol}")'),
            ('pageNumber', '1'),
            ('pageSize', '200'),
            ('source', 'SECURITIES'),
            ('client', 'PC')]
    
    response = get_common_json(url, params)
    data = jsonpath(response, '$..data[:]')

    if(len(data) > 0):
      return data[0]['SECUCODE']
    else:
      print("download url", url, "param ", params, "failed, pls check it!")
      return None
      # exit(-1)

  def get_item(self, url, params):

    response = get_common_json(url, params)
    items = jsonpath(response, '$..data[:]')
    if items:
      df = pd.DataFrame(items)
      item_names = df.ITEM_NAME.drop_duplicates().values
      return item_names
    else:
       return None


  def get_data(self, url, params, item_names):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = [('pageNumber', page)] + params
        response = get_common_json(url, param_temp)
        if bar is None:
            pages = jsonpath(response, '$..pages')

            if pages and pages[0] != 1:
                total = pages[0]
                bar = tqdm(total=int(total))
        if bar is not None:
            bar.update()

        data = jsonpath(response, '$..data[:]')
        if not data:
          break
        page += 1
        df = pd.DataFrame(data)
        dfs.append(df)

    if(len(dfs) > 0):

      df = pd.concat(dfs, ignore_index=True)

      # Assuming df is your DataFrame containing the financial data
      # First, let's ensure the 'REPORT' column is of type category to ensure correct ordering
      df['REPORT_DATE'] = pd.Categorical(df['REPORT_DATE'])

      # Now, pivot the DataFrame
      pivot_df = df.pivot_table(index='ITEM_NAME', columns=['REPORT_DATE'], values='AMOUNT', aggfunc='sum')

      # Reset index to make 'ITEM_NAME' a column again if you prefer
      pivot_df.reset_index(inplace=True)

      # Sort the columns by 'REPORT' in ascending order
      pivot_df = pivot_df.sort_values(by='REPORT_DATE', axis=1, ascending=False)


      pivot_df = pivot_df.replace('--', 0)
      pivot_df = pivot_df.replace('_', 0)
      pivot_df = pivot_df.replace('None', 0)
      pivot_df = pivot_df.fillna(0)
      pivot_df['ITEM_NAME'] = pd.Categorical(pivot_df['ITEM_NAME'], categories=item_names, ordered=True)
      df_sorted = pivot_df.sort_values(by='ITEM_NAME')
      df_sorted.reset_index(drop=True, inplace=True)
      return df_sorted
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_us_finance_common(self, symbol, reportName = 'RPT_USSK_FN_CASHFLOW', REPORT_TYPE = "年报"):

    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'


# reportName: RPT_USSK_FN_CASHFLOW
# columns: SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,STD_ITEM_CODE,ITEM_NAME
# quoteColumns: 
# filter: (SECUCODE="AAPL.O")(REPORT_TYPE="年报")
# distinct: STD_ITEM_CODE
# pageNumber: 
# pageSize: 
# sortTypes: 1,-1
# sortColumns: STD_ITEM_CODE,REPORT_DATE
# source: SECURITIES
# client: PC
# v: 010112815550551213

    params = [ 
            ('reportName', f'{reportName}'),
            ('columns', 'SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,STD_ITEM_CODE,ITEM_NAME'),
            ('filter', f'(SECUCODE="{symbol}")'),
            # ('pageSize', '500'),
            ('sortTypes', '1,-1'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'STD_ITEM_CODE,REPORT_DATE')
    ]

    item_names = self.get_item(url, params)

    # print(item_names)

# reportName: RPT_USSK_FN_CASHFLOW
# columns: SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,REPORT,REPORT_DATE,STD_ITEM_CODE,AMOUNT
# quoteColumns: 
# filter: (SECUCODE="AAPL.O")
# pageNumber: 
# pageSize: 
# sortTypes: 1,-1
# sortColumns: STD_ITEM_CODE,REPORT_DATE
# source: SECURITIES
# client: PC
# v: 040908795398770725

    params = [
            ('reportName', f'{reportName}'),
            ('columns', 'SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,REPORT,REPORT_DATE,STD_ITEM_CODE,ITEM_NAME,AMOUNT'),
            ('filter', f'(SECUCODE="{symbol}")'),
            ('sortTypes', '1,-1'),
            ('pageSize', '500'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'STD_ITEM_CODE,REPORT_DATE')
    ]

    df = self.get_data(url, params, item_names)
    return df

  def get_us_finance_cash(self, symbol, REPORT_TYPE = "年报"):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USSK_FN_CASHFLOW')
    return df
  
  def get_us_finance_balance(self, symbol, REPORT_TYPE = "年报"):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USF10_FN_BALANCE')
    return df

  def get_us_finance_income(self, symbol, REPORT_TYPE = "年报"):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USF10_FN_INCOME')
    return df

  def get_data(self, url, params):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = [('pageNumber', page)] + params
        response = get_common_json(url, param_temp)
        if bar is None:
            pages = jsonpath(response, '$..pages')

            if pages and pages[0] != 1:
                total = pages[0]
                bar = tqdm(total=int(total))
        if bar is not None:
            bar.update()

        data = jsonpath(response, '$..data[:]')
        if not data:
          break
        page += 1
        df = pd.DataFrame(data)
        dfs.append(df)

    if(len(dfs) > 0):

      df = pd.concat(dfs, ignore_index=True)
      df = df.replace('--', 0)
      df = df.replace('_', 0)
      df = df.replace('None', 0)
      df = df.fillna(0)

      return df
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_us_finance_main_factor(self, symbol):

    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'

# reportName: RPT_USF10_FN_GMAININDICATOR
# columns: USF10_FN_GMAININDICATOR
# quoteColumns: 
# filter: (SECUCODE="AAPL.O")
# pageNumber: 1
# pageSize: 500
# sortTypes: -1
# sortColumns: REPORT_DATE
# source: SECURITIES
# client: PC
# v: 09027098794059687

    reportName = 'RPT_USF10_FN_GMAININDICATOR'
    # reportName = 'RPT_USF10_FN_BMAININDICATOR'

    params = [
            ('reportName', f'{reportName}'),
            ('columns',  (
       'REPORT_DATE', 'STD_REPORT_DATE',
       'REPORT_DATA_TYPE', 'REPORT_TYPE', 'OPERATE_INCOME', 'OPERATE_INCOME_YOY',
       'GROSS_PROFIT', 'GROSS_PROFIT_YOY', 'PARENT_HOLDER_NETPROFIT',
       'PARENT_HOLDER_NETPROFIT_YOY', 'BASIC_EPS', 'DILUTED_EPS',
       'GROSS_PROFIT_RATIO', 'NET_PROFIT_RATIO', 'ACCOUNTS_RECE_TR',
       'INVENTORY_TR', 'TOTAL_ASSETS_TR', 'ACCOUNTS_RECE_TDAYS',
       'INVENTORY_TDAYS', 'TOTAL_ASSETS_TDAYS', 'ROE_AVG', 'ROA',
       'CURRENT_RATIO', 'SPEED_RATIO', 'OCF_LIQDEBT', 'DEBT_ASSET_RATIO',
       'EQUITY_RATIO', 'BASIC_EPS_YOY', 'GROSS_PROFIT_RATIO_YOY',
       'NET_PROFIT_RATIO_YOY', 'ROE_AVG_YOY', 'ROA_YOY',
       'DEBT_ASSET_RATIO_YOY', 'CURRENT_RATIO_YOY', 'SPEED_RATIO_YOY')),
            ('filter', f'(SECUCODE="{symbol}")'),
            ('sortTypes', '-1'),
            ('pageSize', '500'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'REPORT_DATE')
    ]

    df = self.get_data(url, params)
    return df
