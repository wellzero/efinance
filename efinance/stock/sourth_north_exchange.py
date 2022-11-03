

class sourth_north_exchange:

  def stock_rank_cxfl_ths() -> pd.DataFrame:
    """
    同花顺-数据中心-技术选股-持续放量
    http://data.10jqka.com.cn/rank/cxfl/
    :return: 持续放量
    :rtype: pandas.DataFrame
    """
    js_code = py_mini_racer.MiniRacer()
    js_content = _get_file_content_ths("ths.js")
    js_code.eval(js_content)
    v_code = js_code.call("v")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Cookie": f"v={v_code}",
    }
    url = f"http://data.10jqka.com.cn/rank/cxfl/field/count/order/desc/ajax/1/free/1/page/1/free/1/"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    try:
        total_page = soup.find(
            "span", attrs={"class": "page_info"}
        ).text.split("/")[1]
    except AttributeError as e:
        total_page = 1
    big_df = pd.DataFrame()
    for page in tqdm(range(1, int(total_page) + 1), leave=False):
        v_code = js_code.call("v")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Cookie": f"v={v_code}",
        }
        url = f"http://data.10jqka.com.cn/rank/cxfl/field/count/order/desc/ajax/1/free/1/page/{page}/free/1/"
        r = requests.get(url, headers=headers)
        temp_df = pd.read_html(r.text, converters={"股票代码": str})[0]
        big_df = pd.concat([big_df, temp_df], ignore_index=True)
    big_df.columns = [
        "序号",
        "股票代码",
        "股票简称",
        "涨跌幅",
        "最新价",
        "成交量",
        "基准日成交量",
        "放量天数",
        "阶段涨跌幅",
        "所属行业",
    ]
    big_df["股票代码"] = big_df["股票代码"].astype(str).str.zfill(6)
    big_df["涨跌幅"] = big_df["涨跌幅"].astype(str).str.strip("%")
    big_df["阶段涨跌幅"] = big_df["阶段涨跌幅"].astype(str).str.strip("%")
    big_df["涨跌幅"] = pd.to_numeric(big_df["涨跌幅"])
    big_df["阶段涨跌幅"] = pd.to_numeric(big_df["阶段涨跌幅"])
    big_df["最新价"] = pd.to_numeric(big_df["最新价"])
    big_df["放量天数"] = pd.to_numeric(big_df["放量天数"])
    return big_df