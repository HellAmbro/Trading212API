from enum import Enum


class TimeValidity(Enum):
    DAY = 0,
    GOOD_TILL_CANCEL = 1,


class _Order:

    def __init__(self, instrument_code, order_type):
        self.instrumentCode = instrument_code
        self.orderType = order_type

    def to_json(self):
        # replace ' with " for Trading212 compatibility
        return self.__dict__.__str__().replace("'", "\"")


class MarketOrder(_Order):
    """Market Order: buy or sell a security at the best available price"""

    def __init__(self, instrument_code, quantity):
        super().__init__(instrument_code, "MARKET")
        self.quantity = quantity


class LimitOrder(_Order):
    """Limit Order: purchase or sell a security at a specified price or better."""

    def __init__(self, instrument_code: str, quantity: float, limit_price: float, time_validity: TimeValidity):
        super().__init__(instrument_code, "LIMIT")
        self.quantity = quantity
        self.limitPrice = limit_price
        self.timeValidity = time_validity.name


class StopOrder(_Order):
    """Stop Order: buy or sell a security when its price moves past a particular point"""

    def __init__(self, instrument_code: str, quantity: float, stop_price: float, time_validity: TimeValidity):
        super().__init__(instrument_code, "STOP")
        self.quantity = quantity
        self.stopPrice = stop_price
        self.timeValidity = time_validity.name


class StopLimitOrder(_Order):
    """Stop Limit Order: buy or sell a stock that combines the features of a stop order and a limit order"""

    def __init__(self, instrument_code: str, quantity: float, limit_price: float, stop_price: float,
                 time_validity: TimeValidity):
        super().__init__(instrument_code, "STOP_LIMIT")
        self.quantity = quantity
        self.limitPrice = limit_price
        self.stopPrice = stop_price
        self.timeValidity = time_validity.name


class EquityOrder:
    """Create a generic order, limit, stop_limit, market, stop"""

    def __init__(self, instrument_code, quantity, limit_price=0.0, stop_price=0.0,
                 time_validity: TimeValidity = TimeValidity.DAY):
        # todo validate data, stop < limit etc...

        # Notice: camelCase for Trading212 json format
        self.instrumentCode = instrument_code
        self.quantity = quantity

        if stop_price and limit_price:
            self.limitPrice = limit_price
            self.stopPrice = stop_price
            self.orderType = "STOP_LIMIT"
            self.timeValidity = time_validity.name
        elif limit_price:
            self.limitPrice = limit_price
            self.orderType = "LIMIT"
            self.timeValidity = time_validity.name
        elif stop_price:
            self.stopPrice = stop_price
            self.orderType = "STOP"
            self.timeValidity = time_validity.name
        else:
            self.orderType = "MARKET"

    # todo fix this repetition
    def to_json(self):
        # replace ' with " for Trading212 compatibility
        return self.__dict__.__str__().replace("'", "\"")


class ValueOrder(_Order):
    """Buy a stock by value,ex. 100$,1000$"""

    def __init__(self, instrument_code, value):
        super().__init__(instrument_code, "MARKET")
        # Notice: camelCase for Trading212 json format
        self.instrumentCode = instrument_code
        self.value = value
