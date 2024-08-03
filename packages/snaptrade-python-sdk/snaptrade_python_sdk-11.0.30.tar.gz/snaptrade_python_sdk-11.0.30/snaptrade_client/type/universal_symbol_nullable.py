# coding: utf-8

"""
    SnapTrade

    Connect brokerage accounts to your app for live positions and trading

    The version of the OpenAPI document: 1.0.0
    Contact: api@snaptrade.com
    Created by: https://snaptrade.com/
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING

from snaptrade_client.type.currency import Currency
from snaptrade_client.type.exchange import Exchange
from snaptrade_client.type.figi_instrument_nullable import FigiInstrumentNullable
from snaptrade_client.type.security_type import SecurityType

class RequiredUniversalSymbolNullable(TypedDict):
    id: str

    symbol: str

    raw_symbol: str

    currency: Currency

    type: SecurityType

    currencies: typing.List[Currency]


class OptionalUniversalSymbolNullable(TypedDict, total=False):
    description: typing.Optional[str]

    exchange: Exchange

    figi_code: typing.Optional[str]

    figi_instrument: typing.Optional[FigiInstrumentNullable]

class UniversalSymbolNullable(RequiredUniversalSymbolNullable, OptionalUniversalSymbolNullable):
    pass
