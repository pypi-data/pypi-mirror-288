import pandas as pd
import rqdatac as rq
from typing import List, Literal
from xqdata.constant import Frequency, SecuType
from xqdata_rq.utils import convert_code, to_rq_code
from xqdata_rq.constant import FREQ_XQ2JQ, FIELDS_RQ2XQ, FIELDS_XQ2RQ, SECUTYPE_XQ2RQ


def _get_trading_dates(start_date=None, end_date=None, market="cn"):
    if start_date is None:
        start_date = "1990-01-01"
    if end_date is None:
        end_date = "2100-01-01"
    data = rq.get_trading_dates(start_date, end_date, market=market)
    data = pd.to_datetime(data)
    data.name = "datetime"
    tradeday_df = (
        pd.DataFrame(data=True, index=data, columns=["SSE", "SZSE"])
        .resample("D")
        .last()
        .fillna(0)
    )
    return tradeday_df


def _all_instruments(
    type: Literal[
        SecuType.STOCK,
        SecuType.ETF,
        SecuType.LOF,
        SecuType.CONV,
        SecuType.FUND,
        SecuType.INDEX,
        SecuType.FUTURES,
        SecuType.OPTION,
    ],
    date=None,
):
    rq_type = SECUTYPE_XQ2RQ.get(type)
    data = rq.all_instruments(type=rq_type, date=date)
    # map column names
    data.rename(columns=FIELDS_RQ2XQ, inplace=True)
    if type in (SecuType.FUTURES, SecuType.OPTION):
        data.code = data.code + "." + data.exchange
    # map codes
    data.code = convert_code(data.code)
    # map date
    data["listed_date"] = data["listed_date"].replace("0000-00-00", "1990-01-01")
    data["de_listed_date"] = data["de_listed_date"].replace("0000-00-00", "2100-01-01")
    return data.set_index("code")


def _get_price(
    codes: str | List[str],
    start_date=None,
    end_date=None,
    frequency=Frequency.DAILY,
    fields=None,
    adjust=None,
    skip_suspended=False,
    df=True,
):
    # args map
    rq_codes = to_rq_code(codes)
    rq_frequency = FREQ_XQ2JQ.get(frequency)
    if adjust is None:
        adjust = "none"
    rq_feilds = [FIELDS_XQ2RQ.get(field, field) for field in fields]
    # get_data
    data: pd.DataFrame = rq.get_price(
        order_book_ids=rq_codes,
        start_date=start_date,
        end_date=end_date,
        frequency=rq_frequency,
        fields=rq_feilds,
        adjust_type=adjust,
        skip_suspended=skip_suspended,
        market="cn",
        expect_df=df,
        time_slice=None,
    )
    if data is None:
        return None
    if data.empty:
        return data
    else:
        data = data.reset_index()
    # map column names
    data.rename(columns=FIELDS_RQ2XQ, inplace=True)
    # map codes
    data.code = convert_code(data.code)
    return data.set_index(["datetime", "code"])


def _get_factor(
    codes: str | List[str],
    factors: str | List[str],
    start_date=None,
    end_date=None,
    df=True,
):
    # args map
    rq_codes = to_rq_code(codes)
    if isinstance(factors, str):
        factors = [factors]
    rq_factor = [FIELDS_XQ2RQ.get(factor, factor) for factor in factors]
    # get_data
    data: pd.DataFrame = rq.get_factor(
        order_book_ids=rq_codes,
        factor=rq_factor,
        start_date=start_date,
        end_date=end_date,
        universe=None,
        expect_df=df,
    ).reset_index()
    # map column names
    data.rename(columns=FIELDS_RQ2XQ, inplace=True)
    # map codes
    data.code = convert_code(data.code)
    return data.set_index(["datetime", "code"])


def _is_suspended(codes, start_date=None, end_date=None):
    # args map
    rq_codes = to_rq_code(codes)
    # get_data
    data: pd.DataFrame = rq.is_suspended(
        order_book_ids=rq_codes, start_date=start_date, end_date=end_date, market="cn"
    )
    data = data.stack()
    data.index.names = ["datetime", "code"]
    data.name = "is_paused"
    data = data.reset_index()
    data.code = convert_code(data.code)
    return data.set_index(["datetime", "code"])


def _is_st_stock(codes, start_date=None, end_date=None):
    # args map
    rq_codes = to_rq_code(codes)
    data: pd.DataFrame = rq.is_st_stock(rq_codes, start_date, end_date)
    data = data.stack()
    data.index.names = ["datetime", "code"]
    data.name = "is_st"
    data = data.reset_index()
    data.code = convert_code(data.code)
    return data.set_index(["datetime", "code"])


def _get_instrument_industry(
    codes: str | List[str], source="citics_2019", level=0, date=None
):
    # args map
    if date is not None:
        date = pd.Timestamp(date).date()
    rq_codes = to_rq_code(codes)
    # get_data
    data: pd.DataFrame = rq.get_instrument_industry(
        rq_codes, source=source, level=level, date=date
    ).reset_index()
    # map column names
    MAPPER = {
        "first_industry_code": f"{source}_l1",
        "second_industry_code": f"{source}_l2",
        "third_industry_code": f"{source}_l3",
        "first_industry_name": f"{source}_l1_name",
        "second_industry_name": f"{source}_l2_name",
        "third_industry_name": f"{source}_l3_name",        
    }
    MAPPER.update(FIELDS_RQ2XQ)
    data.rename(columns=MAPPER, inplace=True)
    # map codes
    data.code = convert_code(data.code)
    # fomat data
    if date is None:
        date = pd.Timestamp.today().date()
    data["datetime"] = date
    return data.set_index(["datetime", "code"])