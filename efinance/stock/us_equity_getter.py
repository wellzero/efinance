import os
import time
from jsonpath import jsonpath
import os
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json
from datetime import datetime, timedelta



class us_equity_getter:


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

  def get_data(self, url, title_name, params):

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
      df.columns = list(title_name.values())
      return df
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_us_equity_info(self, symbol):

    url = 'https://datacenter.eastmoney.com/securities/api/data/v1/get'
    reportName = 'RPT_US10_INFO_EQUITY'
    columns = ['SECUCODE','SECURITY_CODE','SECURITY_NAME_ABBR','SECURITY_INNER_CODE','ORG_CODE','CHANGE_DATE','ISSUED_COMMON_SHARES','ISSUED_PREFERRED_SHARES','CHANGE_REASON']

    # Creating the dictionary with uppercase keys and lowercase values
    main_name = {field: field.lower() for field in columns}
# 2 requests
# 3.1 kB transferred
# 34.9 kB resources
# Finish: 110 ms
# DOMContentLoaded: 56 ms
# reportName: RPT_US10_INFO_EQUITY
# columns: SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,SECURITY_INNER_CODE,ORG_CODE,CHANGE_DATE,ISSUED_COMMON_SHARES,ISSUED_PREFERRED_SHARES,CHANGE_REASON
# quoteColumns: 
# filter: (SECUCODE="NVDA.O")
# pageNumber: 1
# pageSize: 200
# sortTypes: -1
# sortColumns: CHANGE_DATE
# source: SECURITIES
# client: PC
# v: 06467591502558883

    params = [
            ('reportName', f'{reportName}'),
            ('columns',  list(main_name.keys())),
            ('filter', f'(SECUCODE="{symbol}")'),
            ('sortTypes', '-1'),
            ('pageSize', '500'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'CHANGE_DATE')
    ]

    df = self.get_data(url, main_name, params)

    return df
