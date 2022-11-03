import os
from jsonpath import jsonpath
from tqdm import tqdm
import pandas as pd
from ..common import get_common_json_nohead

def datacenter_get_data(url, params, fields):

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