from datetime import datetime
from typing import Dict
import pandas as pd
from xqdata.constant import Exchange, Frequency, SecuType

EXCHANGE_RQ2XQ: Dict = {
    "XSHG": Exchange.SSE,
    "XSHE": Exchange.SZSE,
    "CFFEX": Exchange.CFFEX,
    "SHFE": Exchange.SHFE,
    "DCE": Exchange.DCE,
    "CZCE": Exchange.CZCE,
    "INE": Exchange.INE,
    "GFEX": Exchange.GFEX,
    "BJSE": Exchange.BJSE,
    "INDX": Exchange.OF,
    "RI":Exchange.RQ,
}

EXCHANGE_XQ2RQ: Dict = {v: k for k, v in EXCHANGE_RQ2XQ.items()}

FREQ_XQ2JQ: Dict = {
    Frequency.MINUTE: "1m",
    Frequency.DAILY: "1d",
    Frequency.MONTHLY: "1w",
}

FIELDS_XQ2RQ: Dict = {
    "code": "order_book_id",
    "high_limit": "limit_up",
    "low_limit": "limit_down",
    "amount": "total_turnover",
    "datetime": "date",
    "pre_close":"prev_close",
}
FIELDS_RQ2XQ: Dict = {v: k for k, v in FIELDS_XQ2RQ.items()}

SECUTYPE_XQ2RQ = {
    SecuType.STOCK: "CS",
    SecuType.ETF: "ETF",
    SecuType.LOF: "LOF",
    SecuType.INDEX: "INDX",
    SecuType.FUTURES: "Future",
    SecuType.OPTION: "Option",
    SecuType.CONV: "Convertible",
    SecuType.FUND:"FUND",
}
SECUTYPE_RQ2XQ: Dict = {v: k for k, v in FIELDS_XQ2RQ.items()}
