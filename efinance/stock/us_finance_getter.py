import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json
from datetime import datetime, timedelta



class us_finance_getter:


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


  def get_data_1(self, url, params):

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
      REPORT_DATE = 'REPORT'  # 'REPORT_DATE' 'REPORT'
      df[REPORT_DATE] = pd.Categorical(df[REPORT_DATE])

      # Now, pivot the DataFrame
      # pivot_df = df.pivot_table(index='ITEM_NAME', columns=[REPORT_DATE], values='AMOUNT', aggfunc='sum')

      pivot_df = df.pivot_table(values='AMOUNT', 
                            index=['REPORT', 'REPORT_DATE', 'SECUCODE'], 
                            columns=['ITEM_NAME'], 
                            aggfunc='first')

      # Reset index to make 'ITEM_NAME' a column again if you prefer
      # pivot_df.reset_index(inplace=True)

      # Sort the columns by 'REPORT' in ascending order
      # pivot_df = pivot_df.sort_values(by=REPORT_DATE, axis=1, ascending=False)


      pivot_df = pivot_df.replace('--', 0)
      pivot_df = pivot_df.replace('_', 0)
      pivot_df = pivot_df.replace('None', 0)
      pivot_df = pivot_df.fillna(0)
      # pivot_df['ITEM_NAME'] = pd.Categorical(pivot_df['ITEM_NAME'], categories=title_name, ordered=True)
      # df_sorted = pivot_df.sort_values(by='ITEM_NAME')
      # Transpose the DataFrame
      # df_transposed = pivot_df.transpose()

      # Set the first row as the column names
      # df_transposed.columns = df_transposed.iloc[0]

      # Remove the first row
      # df_transposed = df_transposed.iloc[1:]

      # df_transposed = df_transposed.loc[:,title_name.keys()]

      # df_transposed.columns = list(title_name.values())
      # df_transposed.reset_index(drop=True, inplace=True)
      return pivot_df
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

    selected_dict = self.get_item(url, params)


    # selected_dict = {key: title_name[key] for key in item_names if key in title_name}

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

    df = self.get_data_1(url, params)
    return df

  def get_us_finance_cash(self, symbol):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USSK_FN_CASHFLOW')
    return df
  
  def get_us_finance_balance(self, symbol):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USF10_FN_BALANCE')
    return df

  def get_us_finance_income(self, symbol):
    df = self.get_us_finance_common(symbol, reportName = 'RPT_USF10_FN_INCOME')
    return df

  def get_data(self, url, params):

    bar: tqdm = None
    dfs: List[pd.DataFrame] = []

    page = 1
    while 1:
        param_temp = params + [('pageNumber', page)] 
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
      # df.columns = list(title_name.values())
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
    main_name = {
        'REPORT_DATE': 'report_date',
        'STD_REPORT_DATE': 'std_report_date',
        'REPORT_DATA_TYPE': 'report_data_type',
        'REPORT_TYPE': 'report_type',
        'OPERATE_INCOME': 'operate_income',
        'OPERATE_INCOME_YOY': 'operate_income_yoy',
        'GROSS_PROFIT': 'gross_profit',
        'GROSS_PROFIT_YOY': 'gross_profit_yoy',
        'PARENT_HOLDER_NETPROFIT': 'parent_holder_netprofit',
        'PARENT_HOLDER_NETPROFIT_YOY': 'parent_holder_netprofit_yoy',
        'BASIC_EPS': 'basic_eps',
        'DILUTED_EPS': 'diluted_eps',
        'GROSS_PROFIT_RATIO': 'gross_profit_ratio',
        'NET_PROFIT_RATIO': 'net_profit_ratio',
        'ACCOUNTS_RECE_TR': 'accounts_rece_tr',
        'INVENTORY_TR': 'inventory_tr',
        'TOTAL_ASSETS_TR': 'total_assets_tr',
        'ACCOUNTS_RECE_TDAYS': 'accounts_rece_tdays',
        'INVENTORY_TDAYS': 'inventory_tdays',
        'TOTAL_ASSETS_TDAYS': 'total_assets_tdays',
        'ROE_AVG': 'roe_avg',
        'ROA': 'roa',
        'CURRENT_RATIO': 'current_ratio',
        'SPEED_RATIO': 'speed_ratio',
        'OCF_LIQDEBT': 'ocf_liqdebt',
        'DEBT_ASSET_RATIO': 'debt_asset_ratio',
        'EQUITY_RATIO': 'equity_ratio',
        'BASIC_EPS_YOY': 'basic_eps_yoy',
        'GROSS_PROFIT_RATIO_YOY': 'gross_profit_ratio_yoy',
        'NET_PROFIT_RATIO_YOY': 'net_profit_ratio_yoy',
        'ROE_AVG_YOY': 'roe_avg_yoy',
        'ROA_YOY': 'roa_yoy',
        'DEBT_ASSET_RATIO_YOY': 'debt_asset_ratio_yoy',
        'CURRENT_RATIO_YOY': 'current_ratio_yoy',
        'SPEED_RATIO_YOY': 'speed_ratio_yoy'
    }


    params = [
            ('reportName', f'{reportName}'),
            ('columns',  list(main_name.keys())),
            ('filter', f'(SECUCODE="{symbol}")'),
            ('sortTypes', '-1'),
            ('pageSize', '500'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'REPORT_DATE')
    ]

    df = self.get_data(url, params)

    if df.empty:
      main_name = {
    'ORG_CODE': 'org_code',
    'SECURITY_CODE': 'security_code',
    'SECURITY_NAME_ABBR': 'security_name_abbr',
    'SECUCODE': 'secucode',
    'SECURITY_INNER_CODE': 'security_inner_code',
    'REPORT_DATE': 'report_date',
    'STD_REPORT_DATE': 'std_report_date',
    'START_DATE': 'start_date',
    'NOTICE_DATE': 'notice_date',
    'DATE_TYPE': 'date_type',
    'DATE_TYPE_CODE': 'date_type_code',
    'REPORT_TYPE': 'report_type',
    'REPORT_DATA_TYPE': 'report_data_type',
    'FINANCIAL_DATE': 'financial_date',
    'CURRENCY': 'currency',
    'CURRENCY_NAME': 'currency_name',
    'ACCOUNT_STANDARD': 'account_standard',
    'ACCOUNT_STANDARD_NAME': 'account_standard_name',
    'ORGTYPE': 'orgtype',
    'TOTAL_INCOME': 'total_income',
    'TOTAL_INCOME_YOY': 'total_income_yoy',
    'NET_INTEREST_INCOME': 'net_interest_income',
    'NET_INTEREST_INCOME_YOY': 'net_interest_income_yoy',
    'PARENT_HOLDER_NETPROFIT': 'parent_holder_netprofit',
    'PARENT_HOLDER_NETPROFIT_YOY': 'parent_holder_netprofit_yoy',
    'BASIC_EPS_CS': 'basic_eps_cs',
    'BASIC_EPS_CS_YOY': 'basic_eps_cs_yoy',
    'DILUTED_EPS_CS': 'diluted_eps_cs',
    'DILUTED_EPS_CS_YOY': 'diluted_eps_cs_yoy',
    'LOAN_LOSS_PROVISION': 'loan_loss_provision',
    'LOAN_LOSS_PROVISION_YOY': 'loan_loss_provision_yoy',
    'LOAN_DEPOSIT': 'loan_deposit',
    'LOAN_EQUITY': 'loan_equity',
    'LOAN_ASSETS': 'loan_assets',
    'DEPOSIT_EQUITY': 'deposit_equity',
    'DEPOSIT_ASSETS': 'deposit_assets',
    'ROL': 'rol',
    'ROD': 'rod',
    'ROE': 'roe',
    'ROE_YOY': 'roe_yoy',
    'ROA': 'roa',
    'ROA_YOY': 'roa_yoy',
}
      params[0] = ('reportName', 'RPT_USF10_FN_BMAININDICATOR')
      params[1] = ('columns',  list(main_name.keys()))
      df = self.get_data(url, params)
    if df.empty:
      main_name = {
    'ORG_CODE': 'org_code',
    'SECURITY_CODE': 'security_code',
    'SECUCODE': 'secucode',
    'SECURITY_NAME_ABBR': 'security_name_abbr',
    'SECURITY_INNER_CODE': 'security_inner_code',
    'STD_REPORT_DATE': 'std_report_date',
    'REPORT_DATE': 'report_date',
    'DATE_TYPE': 'date_type',
    'DATE_TYPE_CODE': 'date_type_code',
    'REPORT_TYPE': 'report_type',
    'REPORT_DATA_TYPE': 'report_data_type',
    'FISCAL_YEAR': 'fiscal_year',
    'START_DATE': 'start_date',
    'NOTICE_DATE': 'notice_date',
    'ACCOUNT_STANDARD': 'account_standard',
    'ACCOUNT_STANDARD_NAME': 'account_standard_name',
    'CURRENCY': 'currency',
    'CURRENCY_NAME': 'currency_name',
    'ORGTYPE': 'orgtype',
    'TOTAL_INCOME': 'total_income',
    'TOTAL_INCOME_YOY': 'total_income_yoy',
    'PREMIUM_INCOME': 'premium_income',
    'PREMIUM_INCOME_YOY': 'premium_income_yoy',
    'PARENT_HOLDER_NETPROFIT': 'parent_holder_netprofit',
    'PARENT_HOLDER_NETPROFIT_YOY': 'parent_holder_netprofit_yoy',
    'BASIC_EPS_CS': 'basic_eps_cs',
    'BASIC_EPS_CS_YOY': 'basic_eps_cs_yoy',
    'DILUTED_EPS_CS': 'diluted_eps_cs',
    'PAYOUT_RATIO': 'payout_ratio',
    'CAPITIAL_RATIO': 'capitial_ratio',
    'ROE': 'roe',
    'ROE_YOY': 'roe_yoy',
    'ROA': 'roa',
    'ROA_YOY': 'roa_yoy',
    'DEBT_RATIO': 'debt_ratio',
    'DEBT_RATIO_YOY': 'debt_ratio_yoy',
    'EQUITY_RATIO': 'equity_ratio',
}
      params[0] = ('reportName', 'RPT_USF10_FN_IMAININDICATOR')
      params[1] = ('columns',  list(main_name.keys()))
      df = self.get_data(url, params)

    return df
