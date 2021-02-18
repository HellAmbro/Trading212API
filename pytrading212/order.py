from enum import Enum


class TimeValidity(Enum):
    DAY = 0,
    GOOD_TILL_CANCEL = 1,


class _Order:

    def __init__(self, instrument_code, order_type, quantity):
        self.instrumentCode = instrument_code
        self.orderType = order_type
        self.quantity = float(quantity)

    def to_json(self):
        # replace ' with " for Trading212 compatibility
        return self.__dict__.__str__().replace("'", "\"")


class MarketOrder(_Order):
    """Market Order: buy or sell a security at the best available price"""

    def __init__(self, instrument_code, quantity):
        super().__init__(instrument_code, "MARKET", quantity)


class LimitOrder(_Order):
    """Limit Order: purchase or sell a security at a specified price or better."""

    def __init__(self, instrument_code, quantity, limit_price, time_validity: TimeValidity):
        super().__init__(instrument_code, "LIMIT", quantity)
        self.limitPrice = float(limit_price)
        self.timeValidity = time_validity.name


class StopOrder(_Order):
    """Stop Order: buy or sell a security when its price moves past a particular point"""

    def __init__(self, instrument_code, quantity, stop_price, time_validity: TimeValidity):
        super().__init__(instrument_code, "STOP", quantity)
        self.stop_price = float(stop_price)
        self.time_validity = time_validity.name


class StopLimitOrder(_Order):
    """Stop Limit Order: buy or sell a stock that combines the features of a stop order and a limit order"""
    def __init__(self, instrument_code, quantity, limit_price, stop_price, time_validity: TimeValidity):
        super().__init__(instrument_code, "STOP_LIMIT", quantity)
        self.limit_price = float(limit_price)
        self.stopPrice = float(stop_price)
        self.timeValidity = time_validity.name
