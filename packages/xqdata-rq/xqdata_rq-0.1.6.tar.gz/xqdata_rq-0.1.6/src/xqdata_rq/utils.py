from typing import List
from xqdata.constant import Exchange
from xqdata_rq.constant import EXCHANGE_XQ2RQ,EXCHANGE_RQ2XQ
import pandas as pd

def to_rq_code(codes: str | List[str]) -> str | List[str]: 
    if isinstance(codes, str):
        codes = [codes]

    rq_codes = []
    for code in codes:
        code,exchange_name = code.split(".")
        rq_exchange = EXCHANGE_XQ2RQ.get(Exchange[exchange_name])
        rq_codes.append(f"{code}.{rq_exchange}")

    if len(rq_codes) == 1:
        return rq_codes[0]
    return rq_codes

def convert_code(rq_codes: pd.Series | pd.Index):
        rq_code_exchange = rq_codes.str.split(".", expand=True)
        code = rq_code_exchange[0]
        rq_exchange = rq_code_exchange[1]
        exchange = rq_exchange.map(EXCHANGE_RQ2XQ)
        exchange_name = exchange.apply(lambda x: x.name)
        return code + "." + exchange_name