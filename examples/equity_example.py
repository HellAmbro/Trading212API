import configparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pytrading212 import Equity
from pytrading212 import Mode, EquityOrder, OrderType

config = configparser.ConfigParser()
config.read('../config.ini')

driver = webdriver.Chrome(service=Service())
equity = Equity(email=config['ACCOUNT']['email'], password=config['ACCOUNT']['password'], driver=driver, mode=Mode.DEMO)

# Invalid order: voluntary typo-error in instrument code
order = EquityOrder(instrument_code="AAPLL_US_EQ", order_type=OrderType.MARKET, quantity=1)
is_valid, reason = equity.check_order(order)
if is_valid:
    print("Your order is valid, can be executed.")
else:
    print("Your order is not valid. The reason is: ", reason)

# Valid order
order = EquityOrder(instrument_code="AAPL_US_EQ", order_type=OrderType.MARKET, quantity=2)

# Check order validity (recommended)
if equity.check_order(order)[0]:
    # Review order (recommended)
    print(equity.review_order(order))
    # Execute order
    print(equity.execute_order(order))
