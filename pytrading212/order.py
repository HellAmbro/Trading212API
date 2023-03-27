from pytrading212 import constants


class Order:
    def __init__(self, instrument_code):
        self.instrumentCode = instrument_code

    def to_json(self):
        # replace ' with " for Trading212 compatibility
        return self.__dict__.__str__().replace("'", '"')


""" EQUITY """


class MarketOrder(Order):
    """Market Order: buy or sell a security at the best available price"""

    def __init__(self, instrument_code, quantity):
        super().__init__(instrument_code)
        self.quantity = quantity
        self.orderType = "MARKET"


class LimitOrder(Order):
    """Limit Order: purchase or sell a security at a specified price or better."""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            limit_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(
            instrument_code,
        )
        self.quantity = quantity
        self.limitPrice = limit_price
        self.orderType = constants.OrderType.LIMIT
        self.timeValidity = time_validity.name


class StopOrder(Order):
    """Stop Order: buy or sell a security when its price moves past a particular point"""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            stop_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(instrument_code)
        self.quantity = quantity
        self.stopPrice = stop_price
        self.orderType = constants.OrderType.STOP
        self.timeValidity = time_validity.name


class StopLimitOrder(Order):
    """Stop/Limit Order: buy or sell a stock that combines the features of a stop order and a limit order"""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            limit_price: float,
            stop_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(instrument_code)
        self.quantity = quantity
        self.limitPrice = limit_price
        self.stopPrice = stop_price
        self.orderType = constants.OrderType.STOP_LIMIT
        self.timeValidity = time_validity.name


class EquityOrder(Order):
    """Create a generic order, limit, stop_limit, market, stop"""

    def __init__(
            self,
            instrument_code,
            quantity,
            limit_price,
            stop_price,
            time_validity: constants.TimeValidity
    ):
        super().__init__(instrument_code)

        # todo validate data, stop < limit etc...
        # Data Validation

        # Notice: camelCase for Trading212 json format
        self.instrumentCode = instrument_code
        self.quantity = quantity

        if stop_price and limit_price:
            self.limitPrice = limit_price
            self.stopPrice = stop_price
            self.orderType = constants.OrderType.STOP_LIMIT
            self.timeValidity = time_validity.name
        elif limit_price:
            self.limitPrice = limit_price
            self.orderType = constants.OrderType.LIMIT
            self.timeValidity = time_validity.name
        elif stop_price:
            self.stopPrice = stop_price
            self.orderType = constants.OrderType.STOP
            self.timeValidity = time_validity.name
        else:
            self.orderType = constants.OrderType.MARKET


class ValueOrder(Order):
    """Buy a stock by value, ex. 100$,1000$"""

    def __init__(self, instrument_code, value):
        super().__init__(instrument_code)
        # Notice: camelCase for Trading212 json format
        self.instrumentCode = instrument_code
        self.value = value
        self.orderType = constants.OrderType.MARKET


"""CFD"""


class CFDMarketOrder(Order):
    def __init__(self, instrument_code, target_price, quantity):
        super().__init__(instrument_code)
        self.notify = "NONE"  # required by Trading212
        # todo: try to fix this
        # fixme: IMPORTANT! SINCE I'M NOT ABLE TO GET TARGET PRICE FROM TRADING212
        #  TO EXECUTE MARKET ORDERS
        # SELL OR BUY YOU NEED TO PASS A DUMMY TARGET PRICE WHICH MUST BE:
        # > TO REAL BUY PRICE FOR BUY ORDERS,
        # < TO REAL SELL PRICE FOR SELL ORDERS,
        # EXAMPLE: COMPANY 'X' BUY: 100$, SELL: 99$,
        # I WANT TO BUY, I SET target_price to 1000$, THE ORDER IS EXECUTED WITH THE BEST AVAILABLE PRICE, SO 100$,
        # I WANT TO SELL, I SET target_price to 1$, THE ORDER IS EXECUTED WITH THE BEST AVAILABLE PRICE, SO 99$
        # TRY IT YOURSELF IN DEMO MODE!
        self.targetPrice = target_price
        self.quantity = quantity
