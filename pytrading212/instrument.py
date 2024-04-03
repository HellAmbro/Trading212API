import datetime
import json
import typing

import requests


class CandleStick(object):
    """
        The candlestick object is a representaion of the values used in a candlestick
        chart.

        It consists of an opening timestamp opening price, closing price as well
        as a high and low price.

        The trading212 api also gives an int value which seems to be 0 all the
        time which I have not figured out what this is but it is included as
        "unknown"
    """

    opening: float
    closing: float
    high: float
    low: float
    timestamp: datetime.datetime
    unknown: int

    def __init__(self, data: typing.List) -> None:
        self.timestamp, self.high, self.low, self.opening, self.closing, self.unknown = data

    def __repr__(self) -> str:
        return (f"CandleStick(timestamp={self.timestamp}, high={self.high}, low={self.low},"
                f" opening={self.opening}, closing={self.closing}, unknown={self.unknown})")


class Company:
    """Company Wrapper"""

    charting_url: str = "/charting/v3/candles"

    def __init__(self, instrument_code: str, isin: str, language_code: str = 'en'):
        self.instrument_code = instrument_code
        self.isin = isin
        self.language_code = language_code

    def get_pricing_history(
            self,
            interval: str,
            headers: dict,
            trading_instance: 'Trading212'
    ) -> typing.List[CandleStick]:
        ticker_data: str = json.dumps(
            {
                "candles":
                    [
                        {
                            "ticker": self.instrument_code,
                            "useAskPrice": True,
                            "period": interval,
                            "size": 500
                        }
                    ]
            }
        )

        response = requests.put(
            f"{trading_instance.base_url}{self.charting_url}?ticker={self.instrument_code}&languageCode={self.language_code}",
            headers=headers,
            data=ticker_data
        )
        return [
            CandleStick(x) for x in json.loads(
                response.content.decode("utf-8")
            )[0]["response"]["candles"]
        ]


class CFDInstrument:
    def __init__(self, name: str, ticker: str, sell_price: float, buy_price: float):
        self.name = name
        self.ticker = ticker
        self.sell_price = sell_price
        self.buy_price = buy_price
