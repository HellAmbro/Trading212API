# from pytrading212.order import TimeValidity, StopLimitOrder, StopOrder, LimitOrder
#
# from pytrading212 import Trading212, Mode, MarketOrder
# from pytrading212.trading212 import Period
#
# trading212 = Trading212('your_email', 'password', mode=Mode.DEMO)
#
# market_order = trading212.execute_order(MarketOrder(instrument_code="AMZN_US_EQ", quantity=2))
#
# limit_order = trading212.execute_order(
#     LimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, time_validity=TimeValidity.DAY))
#
# stop_order = trading212.execute_order(
#     StopOrder(instrument_code="AMZN_US_EQ", quantity=2, stop_price=4000, time_validity=TimeValidity.GOOD_TILL_CANCEL))
#
# stop_limit = trading212.execute_order(
#     StopLimitOrder(instrument_code="AMZN_US_EQ", quantity=2, limit_price=3000, stop_price=4000,
#                    time_validity=TimeValidity.GOOD_TILL_CANCEL))
#
# funds = trading212.get_funds()
# orders = trading212.get_orders()
#
# portfolio = trading212.get_portfolio_composition()
# performance = trading212.get_portfolio_performance(Period.LAST_DAY)
#
# trading212.finish()
from selenium import webdriver
from selenium import webdriver

# executor_url = driver.command_executor._url
# session_id = driver.session_id
#
# print(session_id)
# print(executor_url)
#
# driver.get("http://tarunlalwani.com")

driver = webdriver.Remote(command_executor='http://127.0.0.1:36205', desired_capabilities={'headless':True})
driver.close() # close dummy driver
driver.session_id = '182ab254a4bd9a0ff45614721cc6f5b9'
driver.get('https://www.cicalzoo.com')
