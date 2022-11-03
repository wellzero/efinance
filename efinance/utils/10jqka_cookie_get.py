
from py_mini_racer import py_mini_racer
from importlib import resources
import pathlib


class get_cookie:


  def get_ths_js(file: str = "10jqka.js") -> pathlib.Path:
      """Get path to data "ths.js" text file.

      Returns
      -------
      pathlib.PosixPath
          Path to file.

      References
      ----------
      .. [1] E.A.Abbott, ”Flatland”, Seeley & Co., 1884.
      """
      with resources.path("akshare.data", file) as f:
          data_file_path = f
          return data_file_path

  def _get_file_content_ths(file: str = "ths.js") -> str:
      """
      获取 JS 文件的内容
      :param file:  JS 文件名
      :type file: str
      :return: 文件内容
      :rtype: str
      """
      setting_file_path = get_ths_js(file)
      with open(setting_file_path) as f:
          file_data = f.read()
      return file_data

  from tqdm import tqdm
  import sys
  sys.path.append(r'/home/akshare')

  from akshare.datasets import get_ths_js


  def _get_file_content_ths(file: str = "ths.js") -> str:
      """
      获取 JS 文件的内容
      :param file:  JS 文件名
      :type file: str
      :return: 文件内容
      :rtype: str
      """
      setting_file_path = get_ths_js(file)
      with open(setting_file_path) as f:
          file_data = f.read()
      return file_data


  def stock_fund_flow_individual(symbol: str = "即时") -> pd.DataFrame:
      """
      同花顺-数据中心-资金流向-个股资金流
      http://data.10jqka.com.cn/funds/ggzjl/#refCountId=data_55f13c2c_254
      :param symbol: choice of {“即时”, "3日排行", "5日排行", "10日排行", "20日排行"}
      :type symbol: str
      :return: 个股资金流
      :rtype: pandas.DataFrame
      """
      js_code = py_mini_racer.MiniRacer()
      js_content = _get_file_content_ths("ths.js")
      js_code.eval(js_content)
      v_code = js_code.call("v")
      print(v_code)