import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pytrading212 import Equity
from pytrading212 import Mode, EquityOrder, OrderType

if __name__ == "__main__":
    email = sys.argv[1]
    password = sys.argv[2]

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    equity = Equity(email=email, password=password, driver=driver, mode=Mode.DEMO)

    # Invalid order: voluntary typo-error in instrument code
    order = EquityOrder(instrument_code="AAPLL_US_EQ", order_type=OrderType.MARKET, quantity=1)
    is_valid, reason = equity.check_order(order)
    if is_valid:
        print("Your order is valid, can be executed")
    else:
        print("The reason is: ", reason)

    # Valid order
    order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=2)

    # Check order validity (recommended)
    if equity.check_order(order)[0]:
        # Review order (recommended)
        print(equity.review_order(order))
        # Execute order
        print(equity.execute_order(order))
