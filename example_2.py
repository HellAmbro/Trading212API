import sys

from selenium import webdriver

from pytrading212 import *

if __name__ == "__main__":
    # python example_2 'my_email' 'mypassword'
    email = sys.argv[1]
    password = sys.argv[2]
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    with Trading212(email, password, driver, mode=Mode.DEMO) as trading212:
        market_order = trading212.execute_order(
            MarketOrder(instrument_code="AMZN_US_EQ", quantity=2)
        )

        limit_order = trading212.execute_order(
            LimitOrder(
                instrument_code="AMZN_US_EQ",
                quantity=2,
                limit_price=3000,
                time_validity=TimeValidity.DAY,
            )
        )

        stop_order = trading212.execute_order(
            StopOrder(
                instrument_code="AMZN_US_EQ",
                quantity=2,
                stop_price=4000,
                time_validity=TimeValidity.GOOD_TILL_CANCEL,
            )
        )

        stop_limit = trading212.execute_order(
            StopLimitOrder(
                instrument_code="AMZN_US_EQ",
                quantity=2,
                limit_price=3000,
                stop_price=4000,
                time_validity=TimeValidity.GOOD_TILL_CANCEL,
            )
        )

        quantity_order = trading212.execute_order(
            EquityOrder(
                "AMZN_US_EQ",
                quantity=2,
                limit_price=3000,
                stop_price=4000,
                time_validity=TimeValidity.GOOD_TILL_CANCEL,
            )
        )

        value_order = trading212.execute_value_order(ValueOrder("AMZN_US_EQ", value=100))

        # sell an equity that you own

        value_sell_order = trading212.execute_value_order(
            ValueOrder("AMZN_US_EQ", value=-100)
        )

        sell_limit = trading212.execute_order(
            LimitOrder(
                instrument_code="AMZN_US_EQ",
                quantity=-2,
                limit_price=4000,
                time_validity=TimeValidity.GOOD_TILL_CANCEL,
            )
        )