class Company:
    """Company Wrapper"""

    def __init__(self, instrument_code: str, isin: str):
        self.instrument_code = instrument_code
        self.isin = isin


class CFDInstrument:
    def __init__(self, name: str, ticker: str, sell_price: float, buy_price: float):
        self.name = name
        self.ticker = ticker
        self.sell_price = sell_price
        self.buy_price = buy_price
