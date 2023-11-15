import configparser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from pytrading212 import CFD, CFDMarketOrder, CFDLimitStopOrder, CFDOCOOrder
from pytrading212 import Mode

config = configparser.ConfigParser()
config.read('../config.ini')

driver = webdriver.Chrome(service=Service())
cfd = CFD(email=config['ACCOUNT']['email'], password=config['ACCOUNT']['password'], driver=driver, mode=Mode.DEMO)

# Instrument code
instrument_code = "AAPL"

# Market Orders
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.1,  # Buy (quantity is positive)
                           target_price=cfd.get_current_price(instrument_code=instrument_code))
print(cfd.execute_order(order=cfd_order))

current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           limit_distance=5)
print(cfd.execute_order(cfd_order))

current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           stop_distance=2.0)
print(cfd.execute_order(cfd_order))

current_price = cfd.get_current_price(instrument_code=instrument_code)
cfd_order = CFDMarketOrder(instrument_code=instrument_code,
                           quantity=0.5,
                           target_price=current_price,
                           limit_distance=4.0,
                           stop_distance=2.0,
                           )
print(cfd.execute_order(cfd_order))

# Limit Stop Order (Pending Orders)
target_price = cfd.get_current_price(instrument_code=instrument_code) - 20.0
cfd_limit_stop_order = CFDLimitStopOrder(instrument_code=instrument_code,
                                         target_price=target_price,
                                         quantity=1,
                                         take_profit=target_price + 10,
                                         stop_loss=target_price - 10)
print(cfd.execute_order(cfd_limit_stop_order))

# OCO Order (Order Cancel Order)
cfd_oco_order = CFDOCOOrder(instrument_code=instrument_code,
                            order1=CFDOCOOrder.OCOSubOrder(price=150, quantity=1),
                            order2=CFDOCOOrder.OCOSubOrder(price=180.0, quantity=-1))
print(cfd.execute_order(cfd_oco_order))
