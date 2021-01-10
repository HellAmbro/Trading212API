from enum import Enum


class _OrderType(Enum):
    LIMIT = 0,
    MARKET = 1,
    STOP_LIMIT = 2,
    STOP = 3,


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


# MARKET: {"instrumentCode":"AMZN_US_EQ","orderType":"MARKET","quantity":-0.1}
class MarketOrder(_Order):
    """Market Order: buy or sell a security at the best available price"""

    def __init__(self, instrument_code, quantity):
        super().__init__(instrument_code, _OrderType.MARKET.name, quantity)


# LIMIT ORDER: {"instrumentCode":"AAPL_US_EQ","orderType":"LIMIT","quantity":1,"limitPrice":118,"timeValidity":"DAY"}
class LimitOrder(_Order):
    """Limit Order: purchase or sell a security at a specified price or better."""

    def __init__(self, instrument_code, quantity, limit_price, time_validity):
        super().__init__(instrument_code, _OrderType.LIMIT.name, quantity)
        self.limitPrice = float(limit_price)
        self.timeValidity = TimeValidity(time_validity)


# STOP ORDER:       {"instrumentCode":"AAPL_US_EQ","orderType":"STOP","quantity":2,"stopPrice":118,
# "timeValidity":"GOOD_TILL_CANCEL"}
class StopOrder(_Order):
    """Stop order: buy or sell a security when its price moves past a particular point"""

    def __init__(self, instrument_code, quantity, stop_price, time_validity):
        super().__init__(instrument_code, _OrderType.STOP.name, quantity)
        self.stop_price = float(stop_price)
        self.time_validity = TimeValidity(time_validity)


# STOP-LIMIT ORDER: {"instrumentCode":"AAPL_US_EQ","orderType":"STOP_LIMIT","quantity":1,"limitPrice":118,
# "stopPrice":118.25,"timeValidity":"DAY"}
class StopLimitOrder(_Order):
    def __init__(self, instrument_code, quantity, limit_price, stop_price, time_validity):
        super().__init__(instrument_code, quantity, limit_price)
        self.limit_price = float(limit_price)
        self.stopPrice = float(stop_price)
        self.timeValidity = TimeValidity(time_validity)
