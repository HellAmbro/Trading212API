from pytrading212 import constants, utils


class Order:
    """Base Order"""

    def to_json(self):
        out = self.__dict__  # Convert order in dictionary
        # Replace ' with " for Trading212 compatibility
        return dict((utils.to_camel_case(key), value) for (key, value) in out.items()).__str__().replace("'", '"')


class EquityOrder(Order):
    """Base Equity Oder"""

    def __init__(self,
                 instrument_code: str,
                 order_type: constants.OrderType,
                 **kwargs):
        self.instrument_code = instrument_code
        self.order_type = order_type.name

        for key, value in kwargs.items():
            setattr(self, key, value)

        if not (hasattr(self, 'quantity') or hasattr(self, 'value')):
            raise Exception("'value' or 'quantity' parameter must be be provided.")

        if hasattr(self, 'quantity') and hasattr(self, 'value'):
            raise Exception("'value' or 'quantity' both provided, only one is allowed.")

    def is_value_order(self):
        return hasattr(self, 'value')

    def is_quantity_order(self):
        return hasattr(self, 'quantity')


class MarketOrder(EquityOrder):
    """Market Order Wrapper."""

    def __init__(self, instrument_code: str, quantity: float):
        super().__init__(instrument_code=instrument_code,
                         order_type=constants.OrderType.MARKET,
                         quantity=quantity)


class LimitOrder(EquityOrder):
    """Limit Order Wrapper."""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            limit_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(instrument_code=instrument_code,
                         order_type=constants.OrderType.LIMIT,
                         quantity=quantity,
                         limit_price=limit_price,
                         time_validity=time_validity.name)


class StopOrder(EquityOrder):
    """Stop Order Wrapper."""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            stop_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(instrument_code=instrument_code, order_type=constants.OrderType.STOP,
                         quantity=quantity,
                         stop_price=stop_price,
                         time_validity=time_validity.name
                         )


class StopLimitOrder(EquityOrder):
    """Stop/Limit Order Wrapper."""

    def __init__(
            self,
            instrument_code: str,
            quantity: float,
            limit_price: float,
            stop_price: float,
            time_validity: constants.TimeValidity,
    ):
        super().__init__(instrument_code=instrument_code,
                         order_type=constants.OrderType.STOP_LIMIT, quantity=quantity, limit_price=limit_price,
                         stop_price=stop_price, time_validity=time_validity.name
                         )


class ValueOrder(EquityOrder):
    """Value Order Wrapper."""

    def __init__(self, instrument_code: str, value: float):
        super().__init__(instrument_code=instrument_code,
                         order_type=constants.OrderType.MARKET,
                         value=value)


class CFDOrder(Order):
    """Base CFD Oder"""

    def __init__(self, instrument_code: str, quantity: float, **kwargs):
        self.instrument_code = instrument_code
        self.quantity = quantity
        self.notify = "NONE"

        for key, value in kwargs.items():
            setattr(self, key, value)


class CFDMarketOrder(CFDOrder):
    def __init__(self, instrument_code: str, target_price: float, quantity: float):
        super().__init__(instrument_code)

        # required by Trading212
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
        super.target_price = target_price
        super.quantity = quantity


class CFDLimitStopOrder(CFDOrder):
    """todo"""

    def __init__(self,
                 instrument_code: str,
                 quantity: float,
                 target_price: float,
                 take_profit: float,
                 stop_loss: float,
                 ):
        super().__init__(instrument_code)
        super.quantity = quantity
        super.target_price = target_price,
        super.take_profit = take_profit,
        super.stop_loss = stop_loss
