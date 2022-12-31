import sys

from selenium import webdriver

from pytrading212 import *

if __name__ == "__main__":
    # python example_2 'my_email' 'mypassword'
    email = sys.argv[1]
    password = sys.argv[2]
    driver = webdriver.Chrome(executable_path='chromedriver.exe')

    cfd = CFD(email, password, driver, mode=Mode.DEMO)
    order = CFDMarketOrder(instrument_code='EURGBP', target_price=10.0, quantity=500)
    cfd_order_outcome = cfd.execute_order(order)
    print(cfd_order_outcome)
