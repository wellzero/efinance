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


  def get_data_1(self, url, params,  title_name):

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
      pivot_df['ITEM_NAME'] = pd.Categorical(pivot_df['ITEM_NAME'], categories=list(title_name.keys()), ordered=True)
      df_sorted = pivot_df.sort_values(by='ITEM_NAME')
      # Transpose the DataFrame
      df_transposed = df_sorted.transpose()

      # Set the first row as the column names
      df_transposed.columns = df_transposed.iloc[0]

      # Remove the first row
      df_transposed = df_transposed.iloc[1:]

      df_transposed.columns = list(title_name.values())
      # df_transposed.reset_index(drop=True, inplace=True)
      return df_transposed
    else:
      print("download url", url, "param ", param_temp, "failed, pls check it!")
      return pd.DataFrame()
      # exit(-1)

  def get_us_finance_common(self, symbol, title_name, reportName = 'RPT_USSK_FN_CASHFLOW', REPORT_TYPE = "年报"):

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

    df = self.get_data_1(url, params, title_name)
    return df

  def get_us_finance_cash(self, symbol, REPORT_TYPE = "年报"):
  
    cash_name = {
    '净利润': 'net_profit',
    '折旧及摊销': 'depreciation_and_amortization',
    '基于股票的补偿费': 'stock_based_compensation',
    '减值及拨备': 'impairment_and_provisions',
    '递延所得税': 'deferred_income_tax',
    '资产处置损益': 'gains_and_losses_on_disposal_of_assets',
    '养老及退休福利': 'pension_and_retirement_benefits',
    '经营业务调整其他项目': 'other_adjustments_to_operating_activities',
    '应收账款及票据': 'accounts_receivable_and_notes',
    '存货': 'inventory',
    '预付款项及其他应收款': 'prepayments_and_other_receivables',
    '应付账款及票据': 'accounts_payable_and_notes',
    '应付税项': 'taxes_payable',
    '其他经营活动产生的现金流量总额': 'total_cash_flow_from_other_operating_activities',
    '经营业务其他项目': 'other_operating_activities',
    '经营活动产生的现金流量净额': 'net_cash_flow_from_operating_activities',
    '购买固定资产': 'purchase_of_fixed_assets',
    '处置固定资产': 'disposal_of_fixed_assets',
    '购建无形资产及其他资产': 'acquisition_and_construction_of_intangible_assets_and_other_assets',
    '处置无形资产及其他资产': 'disposal_of_intangible_assets_and_other_assets',
    '投资支付现金': 'cash_paid_for_investments',
    '出售附属公司': 'sale_of_subsidiaries',
    '收购附属公司': 'acquisition_of_subsidiaries',
    '其他投资活动产生的现金流量净额': 'net_cash_flow_from_other_investment_activities',
    '投资业务其他项目': 'other_investment_activities',
    '投资活动产生的现金流量净额': 'net_cash_flow_from_investment_activities',
    '发行股份': 'issuance_of_shares',
    '回购股份': 'share_repurchase',
    '赎回债券': 'redemption_of_bonds',
    '股息支付': 'dividend_payments',
    '新增借款': 'new_borrowings',
    '现金及权益增加(减少)': 'increase_decrease_in_cash_and_equity',
    '贷款收益': 'interest_income_from_loans',
    '超额税收优惠': 'excess_tax_benefits',
    '其他筹资活动产生的现金流量净额': 'net_cash_flow_from_other_financing_activities',
    '筹资业务其他项目': 'other_financing_activities',
    '筹资活动产生的现金流量净额': 'net_cash_flow_from_financing_activities',
    '汇率变动影响': 'effect_of_exchange_rate_changes',
    '现金及现金等价物增加(减少)额': 'net_increase_decrease_in_cash_and_cash_equivalents',
    '现金及现金等价物期初余额': 'cash_and_cash_equivalents_at_beginning_of_period',
    '现金及现金等价物期末余额': 'cash_and_cash_equivalents_at_end_of_period'
    }
    df = self.get_us_finance_common(symbol, cash_name, reportName = 'RPT_USSK_FN_CASHFLOW')
    return df
  
  def get_us_finance_balance(self, symbol, REPORT_TYPE = "年报"):
    balance_name = {
    '现金及现金等价物': 'cash_and_cash_equivalents',
    '短期投资': 'short_term_investments',
    '应收账款': 'accounts_receivable',
    '存货': 'inventory',
    '递延所得税资产(流动)': 'deferred_income_tax_assets_current',
    '预付款项(流动)': 'prepaid_expenses_current',
    '其他流动资产': 'other_current_assets',
    '有价证券投资(流动)': 'marketable_securities_investments_current',
    '流动资产合计': 'total_current_assets',
    '物业、厂房及设备': 'property_plant_and_equipment',
    '固定资产': 'fixed_assets',
    '无形资产': 'intangible_assets',
    '商誉': 'goodwill',
    '长期投资': 'long_term_investments',
    '递延所得税资产(非流动)': 'deferred_income_tax_assets_non_current',
    '其他投资': 'other_investments',
    '预付款项(非流动)': 'prepaid_expenses_non_current',
    '其他非流动资产': 'other_non_current_assets',
    '有价证券投资(非流动)': 'marketable_securities_investments_non_current',
    '非流动资产其他项目': 'other_non_current_assets_items',
    '非流动资产合计': 'total_non_current_assets',
    '总资产': 'total_assets',
    '应付账款': 'accounts_payable',
    '应付票据(流动)': 'notes_payable_current',
    '应付税项(流动)': 'taxes_payable_current',
    '短期债务': 'short_term_debt',
    '长期负债(本期部分)': 'current_portion_of_long_term_debt',
    '递延收入(流动)': 'deferred_revenue_current',
    '其他流动负债': 'other_current_liabilities',
    '应付薪酬和福利': 'accrued_compensation_and_benefits',
    '资本租赁债务(流动)': 'current_portion_of_capital_lease_obligations',
    '流动负债合计': 'total_current_liabilities',
    '递延所得税负债(非流动)': 'deferred_income_tax_liabilities_non_current',
    '递延收入(非流动)': 'deferred_revenue_non_current',
    '长期负债': 'long_term_debt',
    '其他非流动负债': 'other_non_current_liabilities',
    '资本租赁债务(非流动)': 'non_current_portion_of_capital_lease_obligations',
    '退休福利和雇员其他补偿': 'retirement_benefits_and_employee_compensation',
    '非流动负债其他项目': 'other_non_current_liabilities_items',
    '非流动负债合计': 'total_non_current_liabilities',
    '总负债': 'total_liabilities',
    '普通股': 'common_stock',
    '优先股': 'preferred_stock',
    '库存股': 'treasury_stock',
    '留存收益': 'retained_earnings',
    '股本溢价': 'additional_paid_in_capital',
    '其他综合收益': 'other_comprehensive_income',
    '归属于母公司股东权益其他项目': 'other_equity_items_attributable_to_parent_company_shareholders',
    '归属于母公司股东权益': 'equity_attributable_to_parent_company_shareholders',
    '少数股东权益': 'minority_interests',
    '股东权益合计其他项目': 'total_shareholders_equity_other_items',
    '股东权益合计': 'total_shareholders_equity',
    '负债及股东权益合计': 'total_liabilities_and_shareholders_equity',
    '非运算项目': 'non_operating_items'
    }

    df = self.get_us_finance_common(symbol, balance_name, reportName = 'RPT_USF10_FN_BALANCE')
    return df

  def get_us_finance_income(self, symbol, REPORT_TYPE = "年报"):
    income_name = {
    '主营收入': 'main_revenue',
    '营业收入': 'operating_revenue',
    '主营成本': 'main_cost',
    '营业成本': 'operating_cost',
    '毛利': 'gross_profit',
    '研发费用': 'research_and_development_expenses',
    '营销费用': 'selling_and_marketing_expenses',
    '减值及拨备': 'impairment_and_provisions',
    '其他营业费用': 'other_operating_expenses',
    '营业费用': 'operating_expenses',
    '营业利润': 'operating_profit',
    '利息收入': 'interest_income',
    '利息支出': 'interest_expenses',
    '其他收入(支出)': 'other_income_expenses',
    '税前利润其他项目': 'profit_before_tax_and_other_items',
    '持续经营税前利润': 'profit_before_tax_from_continuing_operations',
    '所得税': 'income_tax',
    '持续经营净利润': 'net_profit_from_continuing_operations',
    '已终止或非持续经营净利润': 'net_profit_from_discontinued_or_non_continuing_operations',
    '税后利润其他项目': 'profit_after_tax_and_other_items',
    '净利润': 'net_profit',
    '少数股东损益': 'minority_interest',
    '归属于优先股净利润及其他项': 'net_profit_attributable_to_preference_shareholders_and_others',
    '归属于普通股股东净利润': 'net_profit_attributable_to_common_shareholders',
    '归属于母公司股东净利润': 'net_profit_attributable_to_parent_company_shareholders',
    '每股股息-普通股': 'dividends_per_share_common_stock',
    '基本每股收益-普通股': 'basic_earnings_per_share_common_stock',
    '摊薄每股收益-普通股': 'diluted_earnings_per_share_common_stock',
    '基本加权平均股数-普通股': 'basic_weighted_average_shares_common_stock',
    '摊薄加权平均股数-普通股': 'diluted_weighted_average_shares_common_stock',
    '本公司拥有人占全面收益总额': 'total_comprehensive_income_attributable_to_owners_of_the_parent',
    '非控股权益占全面收益总额': 'total_comprehensive_income_attributable_to_non_controlling_interests',
    '其他全面收益其他项目': 'other_comprehensive_income_other_items',
    '其他全面收益合计项': 'total_other_comprehensive_income',
    '全面收益总额': 'total_comprehensive_income',
    '非运算项目': 'non_operating_items'
    }
    df = self.get_us_finance_common(symbol, income_name, reportName = 'RPT_USF10_FN_INCOME')
    return df

  def get_data(self, url, title_name, params):

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
      df.columns = list(title_name.values())
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
            ('columns',  (main_name.keys())),
            ('filter', f'(SECUCODE="{symbol}")'),
            ('sortTypes', '-1'),
            ('pageSize', '500'),
            ('source', 'SECURITIES'),
            ('client', 'PC'),
            ('sortColumns', 'REPORT_DATE')
    ]

    df = self.get_data(url, main_name, params)
    return df
