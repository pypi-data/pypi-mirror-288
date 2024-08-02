import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_common.api.ths.self_choose.ths_self_choose_api as ths_self_choose_api
import mns_common.constant.db_name_constant as db_name_constant
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.api.ths.zt.ths_stock_zt_pool_api as ths_stock_zt_pool_api
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_common.component.trade_date.trade_date_common_service_api as trade_date_common_service_api
from datetime import datetime
import mns_common.utils.data_frame_util as data_frame_util
from functools import lru_cache
mongodb_util = MongodbUtil('27017')

# 固定的选择
fixed_optional_list = ['USDCNH', 'XAUUSD',
                       '881279',
                       '886054', '881153', '881157', '881155',
                       '885736', '881124', '886078',
                       '881145', '886073', '881160', '885730',
                       '886076', '883418', '881169', '885530',
                       '510300', '512100',
                       'CN0Y',
                       '1B0888',
                       '1A0001',
                       '399001',
                       '399006',
                       '1B0688',
                       '899050',
                       'HSI',
                       'HS2083',
                       ]

@lru_cache()
def get_ths_cookie():
    query = {"type": "ths_cookie"}
    stock_account_info = mongodb_util.find_query_data(db_name_constant.STOCK_ACCOUNT_INFO, query)
    ths_cookie = list(stock_account_info['cookie'])[0]
    return ths_cookie


def add_fixed_optional():
    ths_cookie = get_ths_cookie()
    for symbol in fixed_optional_list:
        ths_self_choose_api.add_stock_to_account(symbol, ths_cookie)


def delete_all_self_choose_stocks():
    ths_cookie = get_ths_cookie()
    all_self_choose_stock_list = ths_self_choose_api.get_all_self_choose_stock_list(ths_cookie)
    for stock_one in all_self_choose_stock_list.itertuples():
        symbol = stock_one.code
        ths_self_choose_api.del_stock_from_account(symbol, ths_cookie)


def add_self_choose_local():
    now_date = datetime.now()
    str_day = now_date.strftime('%Y-%m-%d')
    last_trade_day = trade_date_common_service_api.get_last_trade_day(str_day)
    query = {"$and": [{"str_day": {"$gte": last_trade_day}}, {"str_day": {"$lte": str_day}}]}
    trade_stocks_df = mongodb_util.find_query_data(db_name_constant.BUY_STOCK_NAME, query)
    ths_cookie = get_ths_cookie()
    if data_frame_util.is_not_empty(trade_stocks_df):
        for stock_one in trade_stocks_df.itertuples():
            ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)


# 添加连板到自选
def add_continue_boards_zt_stocks():
    ths_cookie = get_ths_cookie()
    ths_stock_zt_pool_df = ths_stock_zt_pool_api.get_zt_reason(None)
    ths_stock_zt_pool_df = ths_stock_zt_pool_df.loc[ths_stock_zt_pool_df['connected_boards_numbers'] > 1]
    ths_stock_zt_pool_df = common_service_fun_api.exclude_st_symbol(ths_stock_zt_pool_df)
    ths_stock_zt_pool_df = ths_stock_zt_pool_df.sort_values(by=['connected_boards_numbers'], ascending=False)
    for stock_one in ths_stock_zt_pool_df.itertuples():
        ths_self_choose_api.add_stock_to_account(stock_one.symbol, ths_cookie)


# 自选股操作 删除当天自选股 增加新的连板股票  添加固定选择自选
def self_choose_stock_handle():
    delete_all_self_choose_stocks()
    add_self_choose_local()
    add_continue_boards_zt_stocks()
    add_fixed_optional()


if __name__ == '__main__':
    self_choose_stock_handle()
