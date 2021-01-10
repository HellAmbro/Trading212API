from pytrading212 import Trading212, Mode
import pytrading212.order as o


trading212 = Trading212('your_email', 'password', mode=Mode.DEMO, save_cookies=True)

market_order = trading212.execute_order(o.MarketOrder(instrument_code="AMZN_US_EQ", quantity=2))

limit_order = trading212.execute_order(
    o.LimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, time_validity=o.TimeValidity.DAY))

stop_order = trading212.execute_order(
    o.StopOrder(instrument_code="AMZN_US_EQ", quantity=2, stop_price=4000,
                time_validity=o.TimeValidity.GOOD_TILL_CANCEL))

stop_limit = trading212.execute_order(
    o.StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, stop_price=4000,
                     time_validity=o.TimeValidity.GOOD_TILL_CANCEL))

trading212.get_funds()
trading212.get_orders()
trading212.cancel_order(14238041)
