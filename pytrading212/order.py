from pytrading212 import constants, utils


class Order:
    """Base Order"""

    def to_json(self):
        out = self.__dict__  # Convert order in dictionary
        # Replace ' with " for Trading212 compatibility
        return dict((utils.to_camel_case(key), value) for (key, value) in out.items()).__str__() \
            .replace("'", '"')


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

    def __init__(self, instrument_code: str, **kwargs):
        self.notify = "NONE"
        self.instrument_code = instrument_code

        for key, value in kwargs.items():
            setattr(self, key, value)


class CFDMarketOrder(CFDOrder):
    """CFD Market Order"""

    def __init__(self,
                 instrument_code: str,
                 quantity: float,
                 target_price: float,
                 **kwargs):
        super().__init__(instrument_code=instrument_code,
                         quantity=quantity,
                         target_price=target_price,
                         **kwargs)


class CFDLimitStopOrder(CFDOrder):
    """CFD Limit Stop Order (Pending Order)"""

    def __init__(self, instrument_code: str, quantity: float, target_price: float, **kwargs):
        super().__init__(instrument_code=instrument_code,
                         target_price=target_price,
                         quantity=quantity,
                         is_limit_stop=True,
                         **kwargs)

    def to_json(self):
        tmp = self
        delattr(tmp, 'instrument_code')  # Remove instrument code
        delattr(tmp, 'is_limit_stop')  # Remove is_limit_stop flag
        out = CFDOrder.to_json(tmp)
        return out


class CFDOCOOrder(CFDOrder):
    """CFD OCO Order"""

    class OCOSubOrder(Order):
        """CFD OCO Sub Order"""

        def __init__(self, price: float, quantity: float):
            self.price = price
            self.quantity = quantity

        def __repr__(self):
            return Order.to_json(self)

    def __init__(self, instrument_code: str, order1: OCOSubOrder, order2: OCOSubOrder):
        super().__init__(instrument_code=instrument_code,
                         order1=order1,
                         order2=order2,
                         is_oco=True)

    def to_json(self):
        tmp = self
        delattr(tmp, 'instrument_code')  # Remove instrument code
        delattr(tmp, 'is_oco')  # Remove is_oco flag
        out = CFDOrder.to_json(tmp)
        return out
