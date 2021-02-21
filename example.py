import sys

from pytrading212.trading212 import Period

from pytrading212 import Trading212, Mode
from pytrading212.order import EquityOrder, ValueOrder, TimeValidity, LimitOrder, StopOrder, StopLimitOrder, MarketOrder

if __name__ == "__main__":
    # email and password passed as program arguments, change this with your credentials
    email = sys.argv[1]
    password = sys.argv[2]

    trading212 = Trading212(email, password, mode=Mode.DEMO, headless=False)

    market_order = trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=2))

    limit_order = trading212.execute_order(LimitOrder(instrument_code="AMZN_US_EQ", quantity=2,
                                                      limit_price=3000, time_validity=TimeValidity.DAY))

    stop_order = trading212.execute_order(StopOrder(instrument_code="AMZN_US_EQ", quantity=2, stop_price=4000,
                                                    time_validity=TimeValidity.GOOD_TILL_CANCEL))

    stop_limit = trading212.execute_order(StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000,
                                                         stop_price=4000, time_validity=TimeValidity.GOOD_TILL_CANCEL))

    quantity_order = trading212.execute_order(EquityOrder('AMZN_US_EQ', quantity=2, limit_price=3000, stop_price=4000,
                                                          time_validity=TimeValidity.GOOD_TILL_CANCEL))

    value_order = trading212.execute_value_order(ValueOrder('AMZN_US_EQ', value=100))

    # sell an equity that you own

    value_sell_order = trading212.execute_value_order(ValueOrder('AMZN_US_EQ', value=-100))

    sell_limit = trading212.execute_order(LimitOrder(instrument_code="AMZN_US_EQ", quantity=-2, limit_price=4000,
                                                     time_validity=TimeValidity.GOOD_TILL_CANCEL))

    print(quantity_order)
    print(value_order)

    funds = trading212.get_funds()
    orders = trading212.get_orders()

    print(funds)
    print(orders)

    portfolio = trading212.get_portfolio_composition()
    performance = trading212.get_portfolio_performance(Period.LAST_DAY)

    print(portfolio)
    print(performance)

    trading212.finish()
